from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
from app.utils.logger import logger
import uuid
from app.config.arangodb_constants import CollectionNames

class GmailChangeHandler:
    def __init__(self, config_service, arango_service):
        self.config_service = config_service
        self.arango_service = arango_service

    async def process_changes(self, user_service, changes) -> bool:
        """Process changes since last sync time"""
        logger.info("🚀 Processing changes")
        try:
            for change in changes.get('history', []):
                logger.info(f"🚀 Processing change: {change}")

                # Handle message additions
                if 'messagesAdded' in change:
                    for message_added in change['messagesAdded']:
                        message = message_added.get('message', {})
                        message_id = message.get('id')

                        if not message_id:
                            continue

                        # Fetch full message details
                        message_data = await user_service.get_message(message_id)
                        if not message_data:
                            continue

                        # Get attachments for this message
                        attachments = await user_service.list_attachments(message_data)

                        # Extract headers
                        headers = message_data.get('headers', {})

                        # Create message record
                        message_record = {
                            '_key': str(uuid.uuid4()),
                            'externalMessageId': message_id,
                            'threadId': message_data.get('threadId'),
                            'internalDate': message_data.get('internalDate'),
                            'subject': headers.get('Subject', 'No Subject'),
                            'from': headers.get('From'),
                            'to': headers.get('To', '').split(', '),
                            'cc': headers.get('Cc', '').split(', '),
                            'bcc': headers.get('Bcc', '').split(', '),
                            'historyId': message_data.get('historyId'),
                            'labelIds': message_data.get('labelIds', []),
                            'lastSyncTime': int(datetime.now(timezone.utc).timestamp())
                        }

                        # Start transaction
                        txn = self.arango_service.db.begin_transaction(
                            read=[CollectionNames.MAILS.value, CollectionNames.ATTACHMENTS.value, CollectionNames.PERMISSIONS.value],
                            write=[CollectionNames.MAILS.value, CollectionNames.ATTACHMENTS.value, CollectionNames.PERMISSIONS.value]
                        )

                        try:
                            # Store message
                            await self.arango_service.batch_upsert_nodes(
                                [message_record],
                                collection=CollectionNames.MAILS.value,
                                transaction=txn
                            )

                            # Store attachments if any
                            if attachments:
                                attachment_records = []
                                for attachment in attachments:
                                    attachment_record = {
                                        '_key': str(uuid.uuid4()),
                                        'externalAttachmentId': attachment['id'],
                                        'messageId': message_id,
                                        'mimeType': attachment.get('mimeType'),
                                        'filename': attachment.get('filename'),
                                        'size': attachment.get('size'),
                                        'lastSyncTime': int(datetime.now(timezone.utc).timestamp())
                                    }
                                    attachment_records.append(
                                        attachment_record)

                                await self.arango_service.batch_upsert_nodes(
                                    attachment_records,
                                    collection=CollectionNames.ATTACHMENTS.value,
                                    transaction=txn
                                )

                            # Store permissions
                            permission_records = []
                            for email_type in ['from', 'to', 'cc', 'bcc']:
                                emails = message_record.get(email_type, [])
                                if isinstance(emails, str):
                                    emails = [emails]

                                for email in emails:
                                    if not email:
                                        continue

                                    entity_id = await self.arango_service.get_entity_id_by_email(email)
                                    if entity_id:
                                        permission_records.append({
                                            '_from': f'users/{entity_id}',
                                            '_to': f'messages/{message_record["_key"]}',
                                            'relationType': 'HAS_ACCESS',
                                            'role': email_type
                                        })

                            if permission_records:
                                await self.arango_service.batch_create_edges(
                                    permission_records,
                                    collection=CollectionNames.PERMISSIONS.value,
                                    transaction=txn
                                )

                            txn.commit_transaction()

                        except Exception as e:
                            txn.abort_transaction()
                            logger.error(
                                f"❌ Error processing message addition: {str(e)}")
                            continue

                # Handle message deletions
                if 'messagesDeleted' in change:
                    for message_deleted in change['messagesDeleted']:
                        message = message_deleted.get('message', {})
                        message_id = message.get('id')

                        if not message_id:
                            continue

                        try:
                            # Find the message in ArangoDB
                            existing_message = next(self.arango_service.db.aql.execute(
                                'FOR doc IN mails FILTER doc.externalMessageId == @message_id RETURN doc',
                                bind_vars={'message_id': message_id}
                            ), None)

                            if not existing_message:
                                continue

                            # Start transaction
                            txn = self.arango_service.db.begin_transaction(
                                read=[CollectionNames.MAILS.value, CollectionNames.ATTACHMENTS.value, CollectionNames.PERMISSIONS.value],
                                write=[CollectionNames.MAILS.value, CollectionNames.ATTACHMENTS.value, CollectionNames.PERMISSIONS.value]
                            )

                            try:
                                # Delete permissions
                                await self.arango_service.db.aql.execute(
                                    'FOR p IN permissions FILTER p._to == @message_id REMOVE p IN permissions',
                                    bind_vars={
                                        'message_id': f'messages/{existing_message["_key"]}'},
                                    transaction=txn
                                )

                                # Delete attachments
                                await self.arango_service.db.aql.execute(
                                    'FOR a IN attachments FILTER a.messageId == @message_id REMOVE a IN attachments',
                                    bind_vars={'message_id': message_id},
                                    transaction=txn
                                )

                                # Delete message
                                await self.arango_service.db.aql.execute(
                                    'REMOVE @key IN mails',
                                    bind_vars={
                                        'key': existing_message['_key']},
                                    transaction=txn
                                )

                                txn.commit_transaction()

                            except Exception as e:
                                txn.abort_transaction()
                                logger.error(
                                    f"❌ Error processing message deletion: {str(e)}")
                                continue

                        except Exception as e:
                            logger.error(
                                f"❌ Error processing message deletion: {str(e)}")
                            continue
            return True
        except Exception as e:
            logger.error(f"❌ Error processing changes: {str(e)}")
            return False
