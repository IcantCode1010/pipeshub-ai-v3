from typing import Dict
from datetime import datetime, timezone
from app.utils.logger import logger
import uuid
import traceback
from app.config.arangodb_constants import CollectionNames, Connectors, RecordTypes, RecordRelations


class DriveChangeHandler:
    def __init__(self, config_service, arango_service):
        self.config_service = config_service
        self.arango_service = arango_service

    async def process_sync_period_changes(self, start_token: str, user_service) -> bool:
        """Process all changes between start_token and current"""
        try:
            logger.info("🚀 Processing changes since initial sync")

            # Get all changes between start_token and current_token
            changes, new_token = await user_service.get_changes(start_token)

            for change in changes:
                logger.info("🚀 Processing change")
                await self.process_change(change, user_service)

            # Only store the new token if we successfully processed all changes
            if new_token:
                await self.arango_service.store_page_token(
                    channel_id=start_token['channel_id'],
                    resource_id=start_token['resource_id'],
                    user_email=start_token['user_email'],
                    token=new_token
                )
                logger.info("✅ New token stored successfully")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to process sync period changes: {str(e)}")
            return False

    async def process_change(self, change: Dict, user_service):
        """Process a single change with revision checking"""
        txn = None
        try:
            file_id = change.get('fileId')
            if not file_id:
                logger.warning("⚠️ Change missing fileId")
                return

            new_file = await user_service.batch_fetch_metadata_and_permissions([file_id])
            new_file = new_file[0]
            if not new_file:
                logger.warning(f"File not found in database: {file_id}")
                return
            cursor = self.arango_service.db.aql.execute(
                f'FOR doc IN {CollectionNames.RECORDS.value} FILTER doc.externalRecordId == @file_id RETURN doc._key',
                bind_vars={'file_id': file_id}
            )
            file_key = next(cursor, None)
            logger.info(f"🚀 File key: {file_key}")

            if file_key:
                # Retrieve file and record using file_key
                file_query = f"""
                RETURN DOCUMENT({CollectionNames.FILES.value}, @file_key)
                """
                record_query = f"""
                RETURN DOCUMENT({CollectionNames.RECORDS.value}, @file_key)
                """

                file_result = self.arango_service.db.aql.execute(
                    file_query,
                    bind_vars={'file_key': file_key}
                )
                file_result = next(file_result, None)

                record_result = self.arango_service.db.aql.execute(
                    record_query,
                    bind_vars={'file_key': file_key}
                )
                record_result = next(record_result, None)

                db_file = file_result if file_result else None
                db_record = record_result if record_result else None

                if not db_file or not db_record:
                    logger.warning(
                        f"❌ Could not find file or record for key: {file_key}")
                    return

            removed = change.get('removed', False)

            logger.info(f"🚀 New file: {new_file}")
            is_trashed = new_file.get('trashed', False)

            logger.info(f"""
            🔄 Processing change:
            - File ID: {file_id}
            - Name: {new_file.get('name', 'Unknown')}
            """)

            txn = self.arango_service.db.begin_transaction(
                read=[CollectionNames.FILES.value, CollectionNames.RECORDS.value, CollectionNames.RECORD_RELATIONS.value,
                      CollectionNames.USERS.value, CollectionNames.GROUPS.value, CollectionNames.ORGS.value, CollectionNames.ANYONE.value, CollectionNames.PERMISSIONS.value, CollectionNames.BELONGS_TO.value],
                write=[CollectionNames.FILES.value, CollectionNames.RECORDS.value, CollectionNames.RECORD_RELATIONS.value, 
                       CollectionNames.USERS.value, CollectionNames.GROUPS.value, CollectionNames.ORGS.value, CollectionNames.ANYONE.value, CollectionNames.PERMISSIONS.value, CollectionNames.BELONGS_TO.value]
            )

            if not file_key:
                await self.handle_insert(new_file, transaction=txn)
                change = "create"
            else:
                if removed or is_trashed:
                    await self.handle_removal(db_file, db_record, transaction=txn)
                    change = "delete"
                else:
                    if not new_file:
                        return
                    needs_update_var, reindex_var = await self.needs_update(new_file, db_file, db_record, transaction=txn)
                    if needs_update_var:
                        await self.handle_update(new_file, db_file, db_record, transaction=txn)
                        if reindex_var:
                            change = "update"
                        else:
                            change = ""
                    else:
                        logger.info(
                            f"✅ File {file_id} is up to date, skipping update")
                        change = ""

            txn.commit_transaction()
            txn = None
            logger.info("Transaction committed for file: %s", {file_id})

            def parse_timestamp(timestamp_str):
                # Remove the 'Z' and add '+00:00' for UTC
                if timestamp_str.endswith('Z'):
                    timestamp_str = timestamp_str[:-1] + '+00:00'
                return datetime.fromisoformat(timestamp_str)

            # SEND KAFKA EVENT FOR REINDEXING

            file_key = await self.arango_service.get_key_by_external_file_id(file_id)
            record = await self.arango_service.get_document(file_key, CollectionNames.RECORDS.value)
            file = await self.arango_service.get_document(file_key, CollectionNames.FILES.value)

            record_version = 0  # Initial version for new files
            extension = file.get('extension')
            mime_type = file.get('mimeType')

            # INSERTION
            if change == "create":
                reindex_event = {
                    'recordId': file_key,
                    "recordName": record.get('recordName'),
                    "recordVersion": 0,
                    "recordType": record.get('recordType'),
                    'eventType': change,
                    "signedUrlRoute": f"http://localhost:8080/api/v1/drive/record/{file_key}/signedUrl",
                    "metadataRoute": f"/api/v1/drive/files/{file_key}/metadata",
                    "connectorName": Connectors.GOOGLE_DRIVE.value,
                    "origin": OriginTypes.CONNECTOR.value,
                    "extension": extension,
                    "mimeType": mime_type,
                    "createdAtSourceTimestamp": int(parse_timestamp(new_file.get('createdTime')).timestamp()),
                    "modifiedAtSourceTimestamp": int(parse_timestamp(new_file.get('modifiedTime')).timestamp())
                }

            # UPDATION
            elif change == "update":
                reindex_event = {
                    'recordId': file_key,
                    "recordName": record.get('recordName'),
                    'recordVersion': 0,
                    'recordType': record.get('recordType'),
                    'eventType': change,
                    "signedUrlRoute": f"http://localhost:8080/api/v1/drive/record/{file_key}/signedUrl",
                    "metadataRoute": f"/api/v1/drive/files/{file_key}/metadata",
                    "connectorName": Connectors.GOOGLE_DRIVE.value,
                    "origin": OriginTypes.CONNECTOR.value,
                    "extension": new_file.get('extension'),
                    "mimeType": new_file.get('mimeType'),
                    "createdAtSourceTimestamp": int(parse_timestamp(new_file.get('createdTime')).timestamp()),
                    "modifiedAtSourceTimestamp": int(parse_timestamp(new_file.get('modifiedTime')).timestamp())
                }

            # DELETION
            elif change == "delete":
                reindex_event = {
                    'recordId': file_key,
                    "recordName": record.get('recordName'),
                    'recordVersion': 0,
                    'recordType': record.get('recordType'),
                    'eventType': change,
                    "signedUrlRoute": f"http://localhost:8080/api/v1/drive/record/{file_key}/signedUrl",
                    "metadataRoute": f"/api/v1/drive/files/{file_key}/metadata",
                    "connectorName": Connectors.GOOGLE_DRIVE.value,
                    "origin": OriginTypes.CONNECTOR.value,
                    "extension": extension,
                    "mimeType": mime_type,
                    "createdAtSourceTimestamp": int(parse_timestamp(new_file.get('createdTime')).timestamp()),
                    "modifiedAtSourceTimestamp": int(parse_timestamp(new_file.get('modifiedTime')).timestamp()),
                }

            else:
                logger.info("NO CHANGE DETECTED. NO KAFKA EVENT SENT")

            await self.arango_service.kafka_service.send_event_to_kafka(
                reindex_event)
            logger.info("📨 Sent Kafka reindexing event for file %s", file_id)

        except Exception as e:
            if txn:
                txn.abort_transaction()
                txn = None
            logger.error(f"❌ Error processing change: {str(e)}")
            traceback.print_exc()

    async def needs_update(self, updated_file, existing_file, existing_record, transaction) -> bool:
        """Check if file needs update based on revision"""
        try:
            logger.info("🚀 Checking if file needs update %s, %s",
                        updated_file.get('id'), updated_file.get('name'))
            if not existing_file:
                logger.info("🟢 File doesn't exist in DB")
                return True

            # Extract permissions from updated file
            new_permissions = updated_file.get('permissions', [])

            # Get existing permissions from database
            existing_permissions = await self.arango_service.get_file_permissions(existing_file['_key'], transaction)
            existing_permissions = [
                p['permission'] for p in existing_permissions] if existing_permissions else []

            # Compare basic metadata first
            latest_revision_id = updated_file.get('headRevisionId')
            latest_file_name = updated_file.get('name')
            latest_parents = updated_file.get('parents', [])
            latest_modified_at = updated_file.get('modifiedTime')
            db_revision_id = existing_record.get('externalRecordId')
            db_file_name = existing_file.get('fileName')
            db_parents = await self.arango_service.get_file_parents(existing_file['_key'], transaction)
            db_modified_at = existing_record.get('sourceLastModifiedTimestamp')

            logger.info(
                "Latest revision ID: %s, DB revision ID: %s, Latest parents: %s, "
                "DB parents: %s, Latest file name: %s, DB file name: %s, Latest modified at: %s, DB modified at: %s",
                latest_revision_id, db_revision_id, latest_parents, db_parents,
                latest_file_name, db_file_name, latest_modified_at, db_modified_at
            )

            # Check permissions changes
            permissions_changed = False
            if len(new_permissions) != len(existing_permissions):
                logger.info("🟢 Number of permissions changed")
                permissions_changed = True
            else:
                # Compare each permission's key attributes
                for new_perm in new_permissions:
                    matching_perm = next(
                        (p for p in existing_permissions if p['externalPermissionId'] == new_perm['id']),
                        None
                    )
                    if not matching_perm:
                        permissions_changed = True
                        break
                    # Compare relevant permission attributes
                    if (new_perm.get('role') != matching_perm.get('role') or
                        new_perm.get('Type') != matching_perm.get('type') or
                            new_perm.get('emailAddress') != matching_perm.get('emailAddress')):
                        permissions_changed = True
                        break

            fallback = False
            if not latest_revision_id or not db_revision_id:
                logger.info("🟢 No revision found")
                fallback = True
                if not latest_modified_at or not db_modified_at:
                    logger.info("🟢 No modified at found")
                    return True

            if not latest_file_name or not db_file_name:
                logger.info("🟢 No file name found")
                return True

            if not latest_parents or not db_parents:
                logger.info("🟢 No parents found")
                return True

            if fallback:
                needs_update_var = (
                    db_modified_at != latest_modified_at or
                    db_file_name != latest_file_name or
                    db_parents != latest_parents or
                    permissions_changed
                )
                
                reindex_var = (
                    db_modified_at != latest_modified_at
                )
            else:
                needs_update_var = (
                    db_revision_id != latest_revision_id or
                    db_file_name != latest_file_name or
                    db_parents != latest_parents or
                    permissions_changed
                )

                reindex_var = (
                    db_revision_id != latest_revision_id
                )

            if permissions_changed:
                logger.info("🟢 Permissions have changed")


            logger.info("🟢 Needs update: %s", needs_update_var)
            logger.info("🟢 Reindex: %s", reindex_var)
            return needs_update_var, reindex_var

        except Exception as e:
            logger.error("❌ Error comparing updates for file %s: %s",
                         db_file_name, str(e))
            return True

    async def handle_removal(self, existing_file, existing_record, transaction=None):
        """Handle file removal or access loss"""
        try:
            logger.info("🚀 Handling removal of record: %s: %s",
                        existing_record['_key'], existing_record['recordName'])

            db = transaction if transaction else self.arango_service.db

            # Get existing file data before marking as deleted
            if not existing_file:
                logger.warning("File %s not found in database")
                return

            query = """
                FOR a IN anyone
                    FILTER a.file_key == @file_key
                    REMOVE a IN anyone
                """
            db.aql.execute(query, bind_vars={
                           'file_key': existing_file['_key']})
            logger.info("🗑️ Removed 'anyone' permission for file %s",
                        existing_file['_key'])

            existing_permissions = await self.arango_service.get_file_permissions(existing_file['_key'], transaction=transaction)
            logger.info("🚀 Existing permissions: %s", existing_permissions)

            # Remove permissions that no longer exist
            if existing_permissions:
                logger.info("🗑️ Removing %d obsolete permissions",
                            len(existing_permissions))
                for perm in existing_permissions:
                    query_permissions = """
                    FOR p IN permissions
                        FILTER p._key == @perm_key
                        REMOVE p IN permissions
                    """
                    db.aql.execute(
                        query_permissions,
                        bind_vars={'perm_key': perm['_key']}
                    )

            await self.arango_service.delete_records_and_relations(existing_record['_key'], hard_delete=True, transaction=transaction)
            logger.info("✅ Successfully handled removal of file")

        except Exception as e:
            logger.error(
                "❌ Error handling removal of record: %s: %s, %s", existing_record['_key'], existing_record['recordName'], str(e))
            raise

    async def handle_insert(self, file_metadata, transaction):
        """Handle file insert"""
        try:
            logger.info("🚀 Handling insert of file: %s",
                        file_metadata.get('name'))
            permissions = file_metadata.get('permissions', [])
            file_id = file_metadata.get('id')
            existing_files = []

            db = transaction if transaction else self.arango_service.db

            # Check if file already exists in ArangoDB
            existing_file = self.arango_service.db.aql.execute(
                f'FOR doc IN {CollectionNames.RECORDS.value} FILTER doc.externalRecordId == @file_id RETURN doc',
                bind_vars={'file_id': file_id}
            )
            existing = next(existing_file, None)

            def parse_timestamp(timestamp_str):
                # Remove the 'Z' and add '+00:00' for UTC
                if timestamp_str.endswith('Z'):
                    timestamp_str = timestamp_str[:-1] + '+00:00'
                return datetime.fromisoformat(timestamp_str)

            if existing:
                logger.debug(f"File {file_id} already exists in ArangoDB")
                existing_files.append(file_id)

            else:
                file = {
                    '_key': str(uuid.uuid4()),
                    'orgId': await self.config_service.get_config('organization'),
                    'fileName': str(file_metadata.get('name')),
                    'extension': file_metadata.get('fileExtension', None),
                    'mimeType': file_metadata.get('mimeType', None),
                    'sizeInBytes': file_metadata.get('size', None),
                    'isFile': file_metadata.get('mimeType', '') != 'application/vnd.google-apps.folder',
                    'webUrl': file_metadata.get('webViewLink', None),
                    'etag': file_metadata.get('etag', None),
                    'ctag': file_metadata.get('ctag', None),
                    'quickXorHash': file_metadata.get('quickXorHash', None),
                    'crc32Hash': file_metadata.get('crc32Hash', None),
                    'md5Checksum': file_metadata.get('md5Checksum', None),
                    'sha1Hash': file_metadata.get('sha1Checksum', None),
                    'sha256Hash': file_metadata.get('sha256Checksum', None),
                    'path': file_metadata.get('path', None)
                }

                record = {
                    '_key': f'{file["_key"]}',
                    'recordName': f'{file["fileName"]}',
                    'recordType': RecordTypes.FILE.value,
                    'version': 0,
                    'externalRecordId': str(file_metadata.get('id')),
                    "externalRevisionId": file_metadata.get('headRevisionId', None),
                    'createdAtTimestamp': int(datetime.now(timezone.utc).timestamp()),
                    'updatedAtTimestamp': int(datetime.now(timezone.utc).timestamp()),
                    'sourceCreatedAtTimestamp': int(parse_timestamp(file_metadata.get('createdTime')).timestamp()),
                    'sourceLastModifiedTimestamp': int(parse_timestamp(file_metadata.get('modifiedTime')).timestamp()),
                    "origin": OriginTypes.CONNECTOR.value,
                    'connectorName': Connectors.GOOGLE_DRIVE.value,
                    'isArchived': False,
                    'lastSyncTimestamp': int(datetime.now(timezone.utc).timestamp()),
                    'indexingStatus': 'NOT_STARTED',
                    'extractionStatus': 'NOT_STARTED'
                }

                recordRelations = []

                if 'parents' in file_metadata:
                    for parent_id in file_metadata['parents']:
                        parent_cursor = db.aql.execute(
                            f'FOR doc IN {CollectionNames.RECORDS.value} FILTER doc.externalRecordId == @parent_id RETURN doc._key',
                            bind_vars={'parent_id': parent_id}
                        )

                        parent_key = next(parent_cursor, None)
                        file_key = file['_key']
                        logger.info("🚀 Parent key: %s, File key: %s",
                                    parent_key, file_key)

                        if parent_key and file_key:
                            recordRelations.append({
                                '_from': f'{CollectionNames.RECORDS.value}/{parent_key}',
                                '_to': f'{CollectionNames.RECORDS.value}/{file_key}',
                                'relationType': RecordRelations.PARENT_CHILD.value
                            })

                if file:
                    await self.arango_service.batch_upsert_nodes([file], CollectionNames.FILES.value, transaction=transaction)
                if record:
                    await self.arango_service.batch_upsert_nodes([record], CollectionNames.RECORDS.value, transaction=transaction)

                if recordRelations:
                    await self.arango_service.batch_create_edges(
                        recordRelations,
                        collection=CollectionNames.RECORD_RELATIONS.value,
                        transaction=transaction
                    )

                if permissions:
                    await self.arango_service.process_file_permissions(file['_key'], permissions, transaction=transaction)

                logger.info(
                    "✅ Successfully handled insert of file %s", file['_key'])

        except Exception as e:
            logger.error("❌ Error handling insert for file: %s", str(e))
            raise

    async def handle_update(self, updated_file, existing_file, existing_record, transaction):
        """Handle file update or creation"""
        try:
            logger.info("🚀 Handling update of file: %s",
                        updated_file.get('name'))

            def parse_timestamp(timestamp_str):
                # Remove the 'Z' and add '+00:00' for UTC
                if timestamp_str.endswith('Z'):
                    timestamp_str = timestamp_str[:-1] + '+00:00'
                return datetime.fromisoformat(timestamp_str)

            # 2. Extract permissions before storing file metadata
            permissions = updated_file.pop('permissions', [])

            file = {
                '_key': existing_file['_key'],
                'fileName': str(updated_file.get('name')),
                'extension': updated_file.get('fileExtension', None),
                'mimeType': updated_file.get('mimeType', None),
                'sizeInBytes': updated_file.get('size', None),
                'webUrl': updated_file.get('webViewLink', None),
                'etag': updated_file.get('etag', None),
                'ctag': updated_file.get('ctag', None),
                'quickXorHash': updated_file.get('quickXorHash', None),
                'crc32Hash': updated_file.get('crc32Hash', None),
                'md5Checksum': updated_file.get('md5Checksum', None),
                'sha1Hash': updated_file.get('sha1Checksum', None),
                'sha256Hash': updated_file.get('sha256Checksum', None),
                'path': updated_file.get('path', None)
            }

            record = {
                '_key': existing_record['_key'],
                'recordName': f'{file["fileName"]}',
                'recordType': RecordTypes.FILE.value,
                'version': 0,
                'externalRecordId': str(updated_file.get('id')),
                "externalRevisionId": updated_file.get('headRevisionId', None),
                'createdAtTimestamp': existing_record.get('createdAtTimestamp', int(datetime.now(timezone.utc).timestamp())),
                'updatedAtTimestamp': int(datetime.now(timezone.utc).timestamp()),
                'sourceCreatedAtTimestamp': existing_record.get('sourceCreatedAtTimestamp', int(parse_timestamp(updated_file.get('createdTime')).timestamp())),
                'sourceLastModifiedTimestamp': existing_record.get('sourceLastModifiedTimestamp', int(parse_timestamp(updated_file.get('modifiedTime')).timestamp())),
                "origin": OriginTypes.CONNECTOR.value,
                'connectorName': Connectors.GOOGLE_DRIVE.value,
                'isArchived': False,
                'lastSyncTimestamp': int(datetime.now(timezone.utc).timestamp()),
                'indexingStatus': 'NOT_STARTED',
                'extractionStatus': 'NOT_STARTED'
            }

            # 5. Update file and record nodes
            await self.arango_service.batch_upsert_nodes([file], CollectionNames.FILES.value, transaction=transaction)
            await self.arango_service.batch_upsert_nodes([record], CollectionNames.RECORDS.value, transaction=transaction)

            # 6. Handle parent relationships
            await self.update_relationships(existing_file['_key'], updated_file, transaction)

            # 7. Process permissions if they exist
            if permissions:
                await self.arango_service.process_file_permissions(existing_file['_key'], permissions, transaction=transaction)

            logger.info("✅ Successfully updated file %s",
                        existing_file['_key'])

        except Exception as e:
            logger.error(
                "❌ Error handling update for file %s: %s", existing_file['_key'], str(e))
            raise

    async def update_relationships(self, file_key: str, updated_file: Dict, transaction) -> bool:
        """Update PARENT_CHILD relationships for a file

        Args:
            file_key (str): The file's key in ArangoDB
            updated_file (Dict): Updated file metadata from Google Drive
            transaction: ArangoDB transaction object

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("🚀 Updating relationships for file: %s", file_key)

            # Get current parents from database
            current_parents = await self.arango_service.get_file_parents(file_key, transaction)
            # Get new parents from updated file
            new_parents = updated_file.get('parents', [])

            db = transaction if transaction else self.arango_service.db

            logger.info("Current parents: %s, New parents: %s",
                        current_parents, new_parents)

            # Find parents to remove and add
            parents_to_remove = set(current_parents) - set(new_parents)
            parents_to_add = set(new_parents) - set(current_parents)

            if not parents_to_remove and not parents_to_add:
                logger.info("✅ No parent changes needed for file %s", file_key)
                return True

            # Remove old relationships
            if parents_to_remove:
                logger.info(
                    "🗑️ Removing old parent relationships: %s", parents_to_remove)
                for parent_id in parents_to_remove:
                    # Get parent key from external ID
                    # Remove parent relationship for file
                    query = """
                    FOR edge IN @@recordRelations
                        FILTER edge._to == @file_id
                        REMOVE edge IN @@recordRelations
                    """
                    db.aql.execute(
                        query,
                        bind_vars={
                            'file_id': f'{CollectionNames.RECORDS.value}/{file_key}',
                            '@recordRelations': CollectionNames.RECORD_RELATIONS.value
                        }
                    )

            # Add new relationships
            if parents_to_add:
                logger.info(
                    "📝 Adding new parent relationships: %s", parents_to_add)
                new_edges = []

                for parent_id in parents_to_add:
                    # Get parent key from external ID
                    parent_cursor = db.aql.execute(
                        f'FOR doc IN {CollectionNames.RECORDS.value} FILTER doc.externalRecordId == @parent_id RETURN doc._key',
                        bind_vars={'parent_id': parent_id}
                    )
                    parent_key = next(parent_cursor, None)

                    if parent_key:
                        new_edges.append({
                            '_from': f'records/{parent_key}',
                            '_to': f'records/{file_key}',
                            'relationType': RecordRelations.PARENT_CHILD.value
                        })

                if new_edges:
                    await self.arango_service.batch_create_edges(
                        new_edges,
                        collection=CollectionNames.RECORD_RELATIONS.value,
                        transaction=transaction
                    )

            logger.info(
                "✅ Successfully updated relationships for file %s", file_key)
            return True

        except Exception as e:
            logger.error(
                "❌ Failed to update relationships for file %s: %s", file_key, str(e))
            if transaction:
                raise
            return False
