# Project File Tree

```
pipeshub-ai/
├── .claude/
│   └── settings.local.json
├── .github/
│   └── workflows/
│       └── main.yml
├── backend/
│   ├── nodejs/
│   │   ├── apps/
│   │   │   ├── src/
│   │   │   │   ├── libs/
│   │   │   │   │   ├── commands/
│   │   │   │   │   │   ├── ai_service/
│   │   │   │   │   │   │   └── ai.service.command.ts
│   │   │   │   │   │   ├── configuration_manager/
│   │   │   │   │   │   │   └── cm.service.command.ts
│   │   │   │   │   │   ├── iam/
│   │   │   │   │   │   │   └── iam.service.command.ts
│   │   │   │   │   │   ├── storage_service/
│   │   │   │   │   │   │   └── storage.service.command.ts
│   │   │   │   │   │   └── command.interface.ts
│   │   │   │   │   ├── encryptor/
│   │   │   │   │   │   └── encryptor.ts
│   │   │   │   │   ├── enums/
│   │   │   │   │   │   ├── db.enum.ts
│   │   │   │   │   │   ├── http-methods.enum.ts
│   │   │   │   │   │   ├── http-status.enum.ts
│   │   │   │   │   │   └── token-scopes.enum.ts
│   │   │   │   │   ├── errors/
│   │   │   │   │   │   ├── api.errors.ts
│   │   │   │   │   │   ├── base.error.ts
│   │   │   │   │   │   ├── database.errors.ts
│   │   │   │   │   │   ├── encryption.errors.ts
│   │   │   │   │   │   ├── etcd.errors.ts
│   │   │   │   │   │   ├── http.errors.ts
│   │   │   │   │   │   ├── kafka.errors.ts
│   │   │   │   │   │   ├── oauth.errors.ts
│   │   │   │   │   │   ├── redis.errors.ts
│   │   │   │   │   │   ├── serialization.error.ts
│   │   │   │   │   │   ├── storage.errors.ts
│   │   │   │   │   │   ├── token.errors.ts
│   │   │   │   │   │   └── validation.error.ts
│   │   │   │   │   ├── keyValueStore/
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── KeyValueStoreType.ts
│   │   │   │   │   │   ├── providers/
│   │   │   │   │   │   │   ├── Etcd3DistributedKeyValueStore.ts
│   │   │   │   │   │   │   └── InMemoryKeyValueStore.ts
│   │   │   │   │   │   ├── keyValueStore.ts
│   │   │   │   │   │   └── keyValueStoreFactory.ts
│   │   │   │   │   ├── middlewares/
│   │   │   │   │   │   ├── file_processor/
│   │   │   │   │   │   │   ├── fp.constant.ts
│   │   │   │   │   │   │   ├── fp.factory.ts
│   │   │   │   │   │   │   ├── fp.interface.ts
│   │   │   │   │   │   │   ├── fp.middleware.ts
│   │   │   │   │   │   │   └── fp.service.ts
│   │   │   │   │   │   ├── auth.middleware.ts
│   │   │   │   │   │   ├── error.middleware.ts
│   │   │   │   │   │   ├── prometheus.middleware.ts
│   │   │   │   │   │   ├── rate-limit.middleware.ts
│   │   │   │   │   │   ├── request.context.ts
│   │   │   │   │   │   ├── types.ts
│   │   │   │   │   │   └── validation.middleware.ts
│   │   │   │   │   ├── services/
│   │   │   │   │   │   ├── prometheus/
│   │   │   │   │   │   │   ├── constants.ts
│   │   │   │   │   │   │   └── prometheus.service.ts
│   │   │   │   │   │   ├── arango.service.ts
│   │   │   │   │   │   ├── authtoken.service.ts
│   │   │   │   │   │   ├── encryption.service.ts
│   │   │   │   │   │   ├── kafka.service.ts
│   │   │   │   │   │   ├── keyValueStore.service.ts
│   │   │   │   │   │   ├── logger.service.ts
│   │   │   │   │   │   ├── mongo.service.ts
│   │   │   │   │   │   └── redis.service.ts
│   │   │   │   │   ├── types/
│   │   │   │   │   │   ├── container.types.ts
│   │   │   │   │   │   ├── kafka.types.ts
│   │   │   │   │   │   ├── keyValueStore.types.ts
│   │   │   │   │   │   ├── redis.types.ts
│   │   │   │   │   │   └── validation.types.ts
│   │   │   │   │   └── utils/
│   │   │   │   │       ├── address.utils.ts
│   │   │   │   │       ├── createJwt.ts
│   │   │   │   │       ├── juridiction.utils.ts
│   │   │   │   │       ├── password.utils.ts
│   │   │   │   │       ├── userActivities.utils.ts
│   │   │   │   │       └── validation.utils.ts
│   │   │   │   ├── modules/
│   │   │   │   │   ├── auth/
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── authService.container.ts
│   │   │   │   │   │   ├── controller/
│   │   │   │   │   │   │   ├── counters.controller.ts
│   │   │   │   │   │   │   ├── saml.controller.ts
│   │   │   │   │   │   │   └── userAccount.controller.ts
│   │   │   │   │   │   ├── middlewares/
│   │   │   │   │   │   │   ├── attachContainer.middleware.ts
│   │   │   │   │   │   │   ├── types.ts
│   │   │   │   │   │   │   └── userAuthentication.middleware.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   ├── orgAuthConfig.routes.ts
│   │   │   │   │   │   │   ├── saml.routes.ts
│   │   │   │   │   │   │   └── userAccount.routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   ├── counter.schema.ts
│   │   │   │   │   │   │   ├── orgAuthConfiguration.schema.ts
│   │   │   │   │   │   │   ├── userActivities.schema.ts
│   │   │   │   │   │   │   └── userCredentials.schema.ts
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   ├── cm.service.ts
│   │   │   │   │   │   │   ├── iam.service.ts
│   │   │   │   │   │   │   ├── mail.service.ts
│   │   │   │   │   │   │   └── session.service.ts
│   │   │   │   │   │   ├── utils/
│   │   │   │   │   │   │   ├── azureAdTokenValidation.ts
│   │   │   │   │   │   │   ├── emailValidator.ts
│   │   │   │   │   │   │   ├── generateAuthToken.ts
│   │   │   │   │   │   │   ├── generateOtp.ts
│   │   │   │   │   │   │   ├── passwordValidator.ts
│   │   │   │   │   │   │   └── validateJwt.ts
│   │   │   │   │   │   └── README.md
│   │   │   │   │   ├── configuration_manager/
│   │   │   │   │   │   ├── config/
│   │   │   │   │   │   │   └── config.ts
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── cm_container.ts
│   │   │   │   │   │   ├── controller/
│   │   │   │   │   │   │   └── cm_controller.ts
│   │   │   │   │   │   ├── middlewares/
│   │   │   │   │   │   │   └── health.middleware.ts
│   │   │   │   │   │   ├── paths/
│   │   │   │   │   │   │   └── paths.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   └── cm_routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   └── connectors.schema.ts
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   ├── kafka_events.service.ts
│   │   │   │   │   │   │   └── updateConfig.service.ts
│   │   │   │   │   │   └── validator/
│   │   │   │   │   │       └── validators.ts
│   │   │   │   │   ├── crawling_manager/
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── cm_container.ts
│   │   │   │   │   │   ├── controller/
│   │   │   │   │   │   │   └── cm_controller.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   └── cm_routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   ├── connectors/
│   │   │   │   │   │   │   │   ├── base_connector.ts
│   │   │   │   │   │   │   │   ├── google_workspace.ts
│   │   │   │   │   │   │   │   ├── one_drive.ts
│   │   │   │   │   │   │   │   ├── s3.ts
│   │   │   │   │   │   │   │   └── slack.ts
│   │   │   │   │   │   │   ├── scheduler/
│   │   │   │   │   │   │   │   ├── base_scheduler.ts
│   │   │   │   │   │   │   │   └── scheduler.ts
│   │   │   │   │   │   │   ├── enums.ts
│   │   │   │   │   │   │   ├── interface.ts
│   │   │   │   │   │   │   └── schema.ts
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   ├── connectors/
│   │   │   │   │   │   │   │   ├── google_workspace.ts
│   │   │   │   │   │   │   │   ├── s3.ts
│   │   │   │   │   │   │   │   └── slack.ts
│   │   │   │   │   │   │   ├── task/
│   │   │   │   │   │   │   │   ├── crawling_task_service.ts
│   │   │   │   │   │   │   │   └── crawling_task_service_factory.ts
│   │   │   │   │   │   │   ├── crawling_service.ts
│   │   │   │   │   │   │   └── crawling_worker.ts
│   │   │   │   │   │   └── validator/
│   │   │   │   │   │       └── validator.ts
│   │   │   │   │   ├── docs/
│   │   │   │   │   │   └── swagger.container.ts
│   │   │   │   │   ├── enterprise_search/
│   │   │   │   │   │   ├── citations/
│   │   │   │   │   │   │   └── citations.schema.ts
│   │   │   │   │   │   ├── connectors/
│   │   │   │   │   │   │   └── connectors.ts
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── es.container.ts
│   │   │   │   │   │   ├── controller/
│   │   │   │   │   │   │   └── es_controller.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   └── es.routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   ├── citation.schema.ts
│   │   │   │   │   │   │   ├── conversation.schema.ts
│   │   │   │   │   │   │   └── search.schema.ts
│   │   │   │   │   │   ├── types/
│   │   │   │   │   │   │   └── conversation.interfaces.ts
│   │   │   │   │   │   ├── utils/
│   │   │   │   │   │   │   └── utils.ts
│   │   │   │   │   │   └── validators/
│   │   │   │   │   │       └── es_validators.ts
│   │   │   │   │   ├── knowledge_base/
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── record.constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── kb_container.ts
│   │   │   │   │   │   ├── controllers/
│   │   │   │   │   │   │   └── kb_controllers.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   └── kb.routes.ts
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   ├── kb.relation.service.ts
│   │   │   │   │   │   │   ├── records_events.service.ts
│   │   │   │   │   │   │   └── sync_events.service.ts
│   │   │   │   │   │   ├── types/
│   │   │   │   │   │   │   ├── file_record.ts
│   │   │   │   │   │   │   ├── record.ts
│   │   │   │   │   │   │   └── service.records.response.ts
│   │   │   │   │   │   ├── utils/
│   │   │   │   │   │   │   └── utils.ts
│   │   │   │   │   │   └── validators/
│   │   │   │   │   │       └── validators.ts
│   │   │   │   │   ├── mail/
│   │   │   │   │   │   ├── config/
│   │   │   │   │   │   │   └── config.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── mailService.container.ts
│   │   │   │   │   │   ├── controller/
│   │   │   │   │   │   │   └── mail.controller.ts
│   │   │   │   │   │   ├── middlewares/
│   │   │   │   │   │   │   ├── checkSmtpConfig.ts
│   │   │   │   │   │   │   ├── types.ts
│   │   │   │   │   │   │   └── userAuthentication.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   └── mail.routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   └── mailInfo.schema.ts
│   │   │   │   │   │   ├── utils/
│   │   │   │   │   │   │   ├── emailTemplates.ts
│   │   │   │   │   │   │   ├── styling.ts
│   │   │   │   │   │   │   └── validateJwt.ts
│   │   │   │   │   │   └── views/
│   │   │   │   │   │       ├── layouts/
│   │   │   │   │   │       │   ├── appusers/
│   │   │   │   │   │       │   │   └── invite.hbs
│   │   │   │   │   │       │   ├── org/
│   │   │   │   │   │       │   │   └── accountCreation.hbs
│   │   │   │   │   │       │   ├── user/
│   │   │   │   │   │       │   │   ├── login.hbs
│   │   │   │   │   │       │   │   ├── resetPassword.hbs
│   │   │   │   │   │       │   │   └── suspiciousLogin.hbs
│   │   │   │   │   │       │   └── workflows/
│   │   │   │   │   │       │       ├── mentionedInWorkflowActivity.hbs
│   │   │   │   │   │       │       └── reviewerAdded.hbs
│   │   │   │   │   │       └── partials/
│   │   │   │   │   │           ├── footer.hbs
│   │   │   │   │   │           ├── head.hbs
│   │   │   │   │   │           ├── header.hbs
│   │   │   │   │   │           └── taskTable.hbs
│   │   │   │   │   ├── notification/
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── notification.container.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   └── notification.schema.ts
│   │   │   │   │   │   ├── service/
│   │   │   │   │   │   │   ├── notification.consumer.ts
│   │   │   │   │   │   │   ├── notification.producer.ts
│   │   │   │   │   │   │   └── notification.service.ts
│   │   │   │   │   │   └── types/
│   │   │   │   │   │       └── types.ts
│   │   │   │   │   ├── storage/
│   │   │   │   │   │   ├── adapter/
│   │   │   │   │   │   │   └── base-storage.adapter.ts
│   │   │   │   │   │   ├── config/
│   │   │   │   │   │   │   └── storage.config.ts
│   │   │   │   │   │   ├── constants/
│   │   │   │   │   │   │   └── constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── storage.container.ts
│   │   │   │   │   │   ├── controllers/
│   │   │   │   │   │   │   ├── storage.controller.ts
│   │   │   │   │   │   │   └── storage.upload.service.ts
│   │   │   │   │   │   ├── docs/
│   │   │   │   │   │   │   ├── swagger.ts
│   │   │   │   │   │   │   └── swagger.yaml
│   │   │   │   │   │   ├── mimetypes/
│   │   │   │   │   │   │   └── mimetypes.ts
│   │   │   │   │   │   ├── providers/
│   │   │   │   │   │   │   ├── azure.provider.ts
│   │   │   │   │   │   │   ├── local-storage.provider.ts
│   │   │   │   │   │   │   └── s3.provider.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   └── storage.routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   └── document.schema.ts
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   └── storage.service.ts
│   │   │   │   │   │   ├── types/
│   │   │   │   │   │   │   └── storage.service.types.ts
│   │   │   │   │   │   ├── utils/
│   │   │   │   │   │   │   └── utils.ts
│   │   │   │   │   │   ├── validators/
│   │   │   │   │   │   │   └── validators.ts
│   │   │   │   │   │   ├── README.md
│   │   │   │   │   │   └── storage.service.ts
│   │   │   │   │   ├── tokens_manager/
│   │   │   │   │   │   ├── config/
│   │   │   │   │   │   │   └── config.ts
│   │   │   │   │   │   ├── consts/
│   │   │   │   │   │   │   └── constants.ts
│   │   │   │   │   │   ├── container/
│   │   │   │   │   │   │   └── token-manager.container.ts
│   │   │   │   │   │   ├── routes/
│   │   │   │   │   │   │   ├── connectors.routes.ts
│   │   │   │   │   │   │   └── health.routes.ts
│   │   │   │   │   │   ├── schema/
│   │   │   │   │   │   │   └── token-reference.schema.ts
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   ├── cm.service.ts
│   │   │   │   │   │   │   ├── connectors-config.service.ts
│   │   │   │   │   │   │   ├── entity_event.service.ts
│   │   │   │   │   │   │   └── token-event.producer.ts
│   │   │   │   │   │   ├── types/
│   │   │   │   │   │   │   └── connector.types.ts
│   │   │   │   │   │   └── utils/
│   │   │   │   │   │       ├── generateToken.ts
│   │   │   │   │   │       └── verifyToken.ts
│   │   │   │   │   └── user_management/
│   │   │   │   │       ├── constants/
│   │   │   │   │       │   └── constants.ts
│   │   │   │   │       ├── container/
│   │   │   │   │       │   └── userManager.container.ts
│   │   │   │   │       ├── controller/
│   │   │   │   │       │   ├── counters.controller.ts
│   │   │   │   │       │   ├── org.controller.ts
│   │   │   │   │       │   ├── userGroups.controller.ts
│   │   │   │   │       │   └── users.controller.ts
│   │   │   │   │       ├── middlewares/
│   │   │   │   │       │   ├── accountTypeCheck.ts
│   │   │   │   │       │   ├── smtpConfigCheck.ts
│   │   │   │   │       │   ├── userAdminCheck.ts
│   │   │   │   │       │   ├── userAdminOrSelfCheck.ts
│   │   │   │   │       │   └── userExists.ts
│   │   │   │   │       ├── routes/
│   │   │   │   │       │   ├── org.routes.ts
│   │   │   │   │       │   ├── userGroups.routes.ts
│   │   │   │   │       │   └── users.routes.ts
│   │   │   │   │       ├── schema/
│   │   │   │   │       │   ├── counter.schema.ts
│   │   │   │   │       │   ├── org.schema.ts
│   │   │   │   │       │   ├── orgLogo.schema.ts
│   │   │   │   │       │   ├── userDp.schema.ts
│   │   │   │   │       │   ├── userGroup.schema.ts
│   │   │   │   │       │   └── users.schema.ts
│   │   │   │   │       └── services/
│   │   │   │   │           ├── auth.service.ts
│   │   │   │   │           ├── cm.service.ts
│   │   │   │   │           ├── entity_events.service.ts
│   │   │   │   │           └── mail.service.ts
│   │   │   │   ├── app.ts
│   │   │   │   └── index.ts
│   │   │   ├── .env.template
│   │   │   ├── .eslintrc.json
│   │   │   ├── .prettierrc
│   │   │   ├── Dockerfile
│   │   │   ├── env.template
│   │   │   ├── package-lock.json
│   │   │   ├── package.json
│   │   │   └── tsconfig.json
│   │   └── .gitignore
│   ├── python/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── middlewares/
│   │   │   │   │   └── auth.py
│   │   │   │   └── routes/
│   │   │   │       ├── agent.py
│   │   │   │       ├── chatbot.py
│   │   │   │       ├── health.py
│   │   │   │       ├── records.py
│   │   │   │       └── search.py
│   │   │   ├── builders/
│   │   │   │   ├── __init__.py
│   │   │   │   └── records_builder.py
│   │   │   ├── config/
│   │   │   │   ├── constants/
│   │   │   │   │   └── store_type.py
│   │   │   │   ├── encryption/
│   │   │   │   │   └── encryption_service.py
│   │   │   │   ├── providers/
│   │   │   │   │   ├── etcd3_connection_manager.py
│   │   │   │   │   ├── etcd3_store.py
│   │   │   │   │   └── in_memory_store.py
│   │   │   │   ├── utils/
│   │   │   │   │   ├── named_constants/
│   │   │   │   │   │   ├── ai_models_named_constants.py
│   │   │   │   │   │   ├── arangodb_constants.py
│   │   │   │   │   │   └── http_status_code_constants.py
│   │   │   │   │   ├── etcd3_backup.py
│   │   │   │   │   └── retry_policy.py
│   │   │   │   ├── configuration_service.py
│   │   │   │   ├── key_value_store.py
│   │   │   │   └── key_value_store_factory.py
│   │   │   ├── connectors/
│   │   │   │   ├── api/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── middleware.py
│   │   │   │   │   └── router.py
│   │   │   │   ├── core/
│   │   │   │   │   ├── base/
│   │   │   │   │   │   ├── auth/
│   │   │   │   │   │   │   └── authentication_service.py
│   │   │   │   │   │   ├── batch_service/
│   │   │   │   │   │   │   └── batch_service.py
│   │   │   │   │   │   ├── connector/
│   │   │   │   │   │   │   └── connector_service.py
│   │   │   │   │   │   ├── data_service/
│   │   │   │   │   │   │   └── data_service.py
│   │   │   │   │   │   ├── error/
│   │   │   │   │   │   │   └── error.py
│   │   │   │   │   │   ├── event_service/
│   │   │   │   │   │   │   └── event_service.py
│   │   │   │   │   │   ├── sync_service/
│   │   │   │   │   │   │   └── sync_service.py
│   │   │   │   │   │   ├── webhook/
│   │   │   │   │   │   │   └── webhook_service.py
│   │   │   │   │   │   └── __init__.py
│   │   │   │   │   ├── factory/
│   │   │   │   │   │   └── connector_factory.py
│   │   │   │   │   └── interfaces/
│   │   │   │   │       ├── auth/
│   │   │   │   │       │   └── iauth_service.py
│   │   │   │   │       ├── batch_service/
│   │   │   │   │       │   └── ibatch_service.py
│   │   │   │   │       ├── connector/
│   │   │   │   │       │   ├── iconnector_config.py
│   │   │   │   │       │   ├── iconnector_factory.py
│   │   │   │   │       │   └── iconnector_service.py
│   │   │   │   │       ├── data_service/
│   │   │   │   │       │   └── data_service.py
│   │   │   │   │       ├── error/
│   │   │   │   │       │   └── error.py
│   │   │   │   │       ├── event_service/
│   │   │   │   │       │   └── event_service.py
│   │   │   │   │       ├── sync_service/
│   │   │   │   │       │   └── isync_service.py
│   │   │   │   │       ├── webhook/
│   │   │   │   │       │   └── iwebhook.py
│   │   │   │   │       └── __init__.py
│   │   │   │   ├── enums/
│   │   │   │   │   └── enums.py
│   │   │   │   ├── services/
│   │   │   │   │   ├── base_arango_service.py
│   │   │   │   │   ├── base_redis_service.py
│   │   │   │   │   ├── entity_kafka_consumer.py
│   │   │   │   │   ├── kafka_service.py
│   │   │   │   │   └── sync_kafka_consumer.py
│   │   │   │   ├── sources/
│   │   │   │   │   ├── google/
│   │   │   │   │   │   ├── admin/
│   │   │   │   │   │   │   ├── admin_webhook_handler.py
│   │   │   │   │   │   │   └── google_admin_service.py
│   │   │   │   │   │   ├── calendar/
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── gcal_sync_service.py
│   │   │   │   │   │   │   └── gcal_user_service.py
│   │   │   │   │   │   ├── common/
│   │   │   │   │   │   │   ├── arango_service.py
│   │   │   │   │   │   │   ├── connector_google_exceptions.py
│   │   │   │   │   │   │   ├── google_token_handler.py
│   │   │   │   │   │   │   ├── scopes.py
│   │   │   │   │   │   │   └── sync_tasks.py
│   │   │   │   │   │   ├── gmail/
│   │   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   │   ├── gmail_change_handler.py
│   │   │   │   │   │   │   ├── gmail_drive_interface.py
│   │   │   │   │   │   │   ├── gmail_sync_service.py
│   │   │   │   │   │   │   ├── gmail_user_service.py
│   │   │   │   │   │   │   └── gmail_webhook_handler.py
│   │   │   │   │   │   └── google_drive/
│   │   │   │   │   │       ├── README.md
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── drive_change_handler.py
│   │   │   │   │   │       ├── drive_sync_service.py
│   │   │   │   │   │       ├── drive_user_service.py
│   │   │   │   │   │       ├── drive_webhook_handler.py
│   │   │   │   │   │       └── file_processor.py
│   │   │   │   │   └── s3/
│   │   │   │   │       ├── config/
│   │   │   │   │       │   └── config.py
│   │   │   │   │       ├── const/
│   │   │   │   │       │   └── const.py
│   │   │   │   │       ├── factories/
│   │   │   │   │       │   └── connector_factory.py
│   │   │   │   │       └── services/
│   │   │   │   │           ├── authentication_service.py
│   │   │   │   │           ├── connector_service.py
│   │   │   │   │           └── data_service.py
│   │   │   │   └── utils/
│   │   │   │       ├── decorators.py
│   │   │   │       ├── drive_worker.py
│   │   │   │       └── rate_limiter.py
│   │   │   ├── core/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ai_arango_service.py
│   │   │   │   ├── celery_app.py
│   │   │   │   ├── redis_scheduler.py
│   │   │   │   └── signed_url.py
│   │   │   ├── events/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── block_prompts.py
│   │   │   │   ├── events.py
│   │   │   │   └── processor.py
│   │   │   ├── exceptions/
│   │   │   │   ├── embedding_exceptions.py
│   │   │   │   ├── fastapi_responses.py
│   │   │   │   └── indexing_exceptions.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── blocks.py
│   │   │   │   ├── file.py
│   │   │   │   ├── graph.py
│   │   │   │   ├── permission.py
│   │   │   │   └── records.py
│   │   │   ├── modules/
│   │   │   │   ├── agents/
│   │   │   │   │   └── qna/
│   │   │   │   │       ├── chat_state.py
│   │   │   │   │       ├── graph.py
│   │   │   │   │       └── nodes.py
│   │   │   │   ├── extraction/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── domain_extraction.py
│   │   │   │   │   ├── prompt_template.py
│   │   │   │   │   └── run.py
│   │   │   │   ├── indexing/
│   │   │   │   │   ├── README.md
│   │   │   │   │   └── run.py
│   │   │   │   ├── ingestion/
│   │   │   │   │   ├── README.md
│   │   │   │   │   └── run.py
│   │   │   │   ├── parsers/
│   │   │   │   │   ├── csv/
│   │   │   │   │   │   └── csv_parser.py
│   │   │   │   │   ├── docx/
│   │   │   │   │   │   ├── docparser.py
│   │   │   │   │   │   └── docx_parser.py
│   │   │   │   │   ├── excel/
│   │   │   │   │   │   ├── excel_parser.py
│   │   │   │   │   │   ├── prompt_template.py
│   │   │   │   │   │   └── xls_parser.py
│   │   │   │   │   ├── google_files/
│   │   │   │   │   │   ├── google_docs_parser.py
│   │   │   │   │   │   ├── google_sheets_parser.py
│   │   │   │   │   │   ├── google_slides_parser.py
│   │   │   │   │   │   └── parser_user_service.py
│   │   │   │   │   ├── html_parser/
│   │   │   │   │   │   └── html_parser.py
│   │   │   │   │   ├── markdown/
│   │   │   │   │   │   ├── markdown_parser.py
│   │   │   │   │   │   └── mdx_parser.py
│   │   │   │   │   ├── pdf/
│   │   │   │   │   │   ├── azure_document_intelligence_processor.py
│   │   │   │   │   │   ├── ocr_handler.py
│   │   │   │   │   │   └── pymupdf_ocrmypdf_processor.py
│   │   │   │   │   └── pptx/
│   │   │   │   │       ├── ppt_parser.py
│   │   │   │   │       └── pptx_parser.py
│   │   │   │   ├── qna/
│   │   │   │   │   └── prompt_templates.py
│   │   │   │   ├── reranker/
│   │   │   │   │   └── reranker.py
│   │   │   │   ├── retrieval/
│   │   │   │   │   ├── README.md
│   │   │   │   │   ├── retrieval_arango.py
│   │   │   │   │   └── retrieval_service.py
│   │   │   │   ├── streaming/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── streaming_service.py
│   │   │   │   └── __init__.py
│   │   │   ├── schema/
│   │   │   │   └── arango/
│   │   │   │       ├── documents.py
│   │   │   │       └── edges.py
│   │   │   ├── scripts/
│   │   │   │   └── services_linux.sh
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ai_config_handler.py
│   │   │   │   └── kafka_consumer.py
│   │   │   ├── setups/
│   │   │   │   ├── connector_setup.py
│   │   │   │   ├── indexing_setup.py
│   │   │   │   └── query_setup.py
│   │   │   ├── utils/
│   │   │   │   ├── aimodels.py
│   │   │   │   ├── citations.py
│   │   │   │   ├── datetime_utils.py
│   │   │   │   ├── llm.py
│   │   │   │   ├── logger.py
│   │   │   │   ├── mimetype_to_extension.py
│   │   │   │   ├── query_decompose.py
│   │   │   │   ├── query_transform.py
│   │   │   │   ├── streaming.py
│   │   │   │   └── time_conversion.py
│   │   │   ├── __init__.py
│   │   │   ├── connectors_main.py
│   │   │   ├── indexing_main.py
│   │   │   └── query_main.py
│   │   ├── .env.template
│   │   ├── .gitignore
│   │   ├── .python-version
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── env.template
│   │   ├── package-lock.json
│   │   └── pyproject.toml
│   └── env.template
├── deployment/
│   └── docker-compose/
│       ├── scripts/
│       │   └── start-ollama.sh
│       ├── README.md
│       ├── docker-compose.dev.yml
│       ├── docker-compose.ollama-dev.yml
│       ├── docker-compose.prod.yml
│       └── env.template
├── docs/
│   └── README.md
├── frontend/
│   ├── packages/
│   │   └── xlsx-0.20.3.tgz
│   ├── public/
│   │   ├── assets/
│   │   │   ├── icons/
│   │   │   │   ├── home/
│   │   │   │   │   ├── ic-design.svg
│   │   │   │   │   ├── ic-development.svg
│   │   │   │   │   └── ic-make-brand.svg
│   │   │   │   ├── navbar/
│   │   │   │   │   ├── ic-chat.svg
│   │   │   │   │   ├── ic-dashboard.svg
│   │   │   │   │   └── ic-disabled.svg
│   │   │   │   ├── notification/
│   │   │   │   │   ├── ic-chat.svg
│   │   │   │   │   ├── ic-delivery.svg
│   │   │   │   │   ├── ic-mail.svg
│   │   │   │   │   └── ic-order.svg
│   │   │   │   └── platforms/
│   │   │   │       └── ic-jwt.svg
│   │   │   └── illustrations/
│   │   │       └── illustration-dashboard.webp
│   │   ├── fonts/
│   │   │   ├── Roboto-Bold.ttf
│   │   │   └── Roboto-Regular.ttf
│   │   ├── logo/
│   │   │   ├── logo-blue.svg
│   │   │   ├── logo-full.svg
│   │   │   ├── logo-single.jpg
│   │   │   ├── signinpage.png
│   │   │   └── welcomegif.gif
│   │   └── favicon.ico
│   ├── src/
│   │   ├── actions/
│   │   │   └── chat.ts
│   │   ├── assets/
│   │   │   └── data/
│   │   │       ├── countries.ts
│   │   │       └── index.ts
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── form-divider.tsx
│   │   │   │   ├── form-head.tsx
│   │   │   │   ├── form-resend-code.tsx
│   │   │   │   ├── form-return-link.tsx
│   │   │   │   ├── microsoft-login-button.tsx
│   │   │   │   ├── sign-up-terms.tsx
│   │   │   │   └── tab-panel.tsx
│   │   │   ├── context/
│   │   │   │   ├── jwt/
│   │   │   │   │   ├── action.ts
│   │   │   │   │   ├── auth-provider.tsx
│   │   │   │   │   ├── constant.ts
│   │   │   │   │   ├── index.ts
│   │   │   │   │   └── utils.ts
│   │   │   │   └── auth-context.tsx
│   │   │   ├── guard/
│   │   │   │   ├── account-type-gurad.tsx
│   │   │   │   ├── admin-guard.tsx
│   │   │   │   ├── auth-guard.tsx
│   │   │   │   ├── guest-guard.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── role-based-guard.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── index.ts
│   │   │   │   └── use-auth-context.ts
│   │   │   ├── styles/
│   │   │   │   └── auth-styles.ts
│   │   │   ├── types/
│   │   │   │   └── auth.ts
│   │   │   ├── view/
│   │   │   │   ├── auth/
│   │   │   │   │   ├── account-setup.tsx
│   │   │   │   │   ├── authentication-view.tsx
│   │   │   │   │   ├── azure-sign-in.tsx
│   │   │   │   │   ├── google-sign-in.tsx
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── microsoft-sign-in.tsx
│   │   │   │   │   ├── oauth-callback.tsx
│   │   │   │   │   ├── oauth-sign-in.tsx
│   │   │   │   │   ├── otp-sign-in.tsx
│   │   │   │   │   ├── password-sign-in.tsx
│   │   │   │   │   ├── reset-password.tsx
│   │   │   │   │   ├── saml-sign-in.tsx
│   │   │   │   │   └── saml-sso-success.tsx
│   │   │   │   └── jwt/
│   │   │   │       ├── jwt-forgot-password.tsx
│   │   │   │       ├── jwt-sign-in-with-otp.tsx
│   │   │   │       ├── jwt-sign-in-with-password.tsx
│   │   │   │       └── jwt-sign-up-view.tsx
│   │   │   └── types.ts
│   │   ├── components/
│   │   │   ├── animate/
│   │   │   │   ├── back-to-top/
│   │   │   │   │   ├── back-to-top.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── scroll-progress/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── scroll-progress.tsx
│   │   │   │   │   └── use-scroll-progress.ts
│   │   │   │   ├── variants/
│   │   │   │   │   ├── actions.ts
│   │   │   │   │   ├── background.ts
│   │   │   │   │   ├── bounce.ts
│   │   │   │   │   ├── container.ts
│   │   │   │   │   ├── fade.ts
│   │   │   │   │   ├── flip.ts
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── path.ts
│   │   │   │   │   ├── rotate.ts
│   │   │   │   │   ├── scale.ts
│   │   │   │   │   ├── slide.ts
│   │   │   │   │   ├── transition.ts
│   │   │   │   │   └── zoom.ts
│   │   │   │   ├── animate-avatar.tsx
│   │   │   │   ├── animate-border.tsx
│   │   │   │   ├── animate-count-up.tsx
│   │   │   │   ├── animate-logo.tsx
│   │   │   │   ├── animate-text.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── motion-container.tsx
│   │   │   │   ├── motion-lazy.tsx
│   │   │   │   ├── motion-viewport.tsx
│   │   │   │   └── types.ts
│   │   │   ├── carousel/
│   │   │   │   ├── components/
│   │   │   │   │   ├── carousel-arrow-buttons.tsx
│   │   │   │   │   ├── carousel-dot-buttons.tsx
│   │   │   │   │   ├── carousel-progress-bar.tsx
│   │   │   │   │   ├── carousel-slide.tsx
│   │   │   │   │   └── carousel-thumbs.tsx
│   │   │   │   ├── hooks/
│   │   │   │   │   ├── use-carousel-arrows.ts
│   │   │   │   │   ├── use-carousel-auto-play.ts
│   │   │   │   │   ├── use-carousel-auto-scroll.ts
│   │   │   │   │   ├── use-carousel-dots.ts
│   │   │   │   │   ├── use-carousel-parallax.ts
│   │   │   │   │   ├── use-carousel-progress.ts
│   │   │   │   │   ├── use-carousel.ts
│   │   │   │   │   └── use-thumbs.ts
│   │   │   │   ├── breakpoints.ts
│   │   │   │   ├── carousel.tsx
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── chart/
│   │   │   │   ├── chart-legends.tsx
│   │   │   │   ├── chart-select.tsx
│   │   │   │   ├── chart.tsx
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── styles.css
│   │   │   │   ├── types.ts
│   │   │   │   └── use-chart.ts
│   │   │   ├── color-utils/
│   │   │   │   ├── color-picker.tsx
│   │   │   │   ├── color-preview.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── custom-breadcrumbs/
│   │   │   │   ├── breadcrumb-link.tsx
│   │   │   │   ├── custom-breadcrumbs.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── custom-date-range-picker/
│   │   │   │   ├── custom-date-range-picker.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── types.ts
│   │   │   │   └── use-date-range-picker.ts
│   │   │   ├── custom-dialog/
│   │   │   │   ├── confirm-dialog.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── custom-popover/
│   │   │   │   ├── custom-popover.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── styles.tsx
│   │   │   │   ├── types.ts
│   │   │   │   ├── use-popover.ts
│   │   │   │   └── utils.ts
│   │   │   ├── custom-tabs/
│   │   │   │   ├── custom-tabs.tsx
│   │   │   │   └── index.ts
│   │   │   ├── dynamic-form/
│   │   │   │   ├── components/
│   │   │   │   │   ├── dynamic-field.tsx
│   │   │   │   │   └── dynamic-form.tsx
│   │   │   │   ├── core/
│   │   │   │   │   ├── config-factory.ts
│   │   │   │   │   ├── config-registry.ts
│   │   │   │   │   ├── field-templates.ts
│   │   │   │   │   ├── providers.ts
│   │   │   │   │   └── types.ts
│   │   │   │   ├── hooks/
│   │   │   │   │   └── use-dynamic-form.ts
│   │   │   │   └── index.ts
│   │   │   ├── editor/
│   │   │   │   ├── components/
│   │   │   │   │   ├── code-highlight-block.css
│   │   │   │   │   ├── code-highlight-block.tsx
│   │   │   │   │   ├── heading-block.tsx
│   │   │   │   │   ├── image-block.tsx
│   │   │   │   │   ├── link-block.tsx
│   │   │   │   │   └── toolbar-item.tsx
│   │   │   │   ├── classes.ts
│   │   │   │   ├── editor.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── styles.tsx
│   │   │   │   ├── toolbar.tsx
│   │   │   │   └── types.ts
│   │   │   ├── empty-content/
│   │   │   │   ├── empty-content.tsx
│   │   │   │   └── index.ts
│   │   │   ├── hook-form/
│   │   │   │   ├── fields.tsx
│   │   │   │   ├── form-provider.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── rhf-autocomplete.tsx
│   │   │   │   ├── rhf-checkbox.tsx
│   │   │   │   ├── rhf-code.tsx
│   │   │   │   ├── rhf-date-picker.tsx
│   │   │   │   ├── rhf-editor.tsx
│   │   │   │   ├── rhf-radio-group.tsx
│   │   │   │   ├── rhf-rating.tsx
│   │   │   │   ├── rhf-select.tsx
│   │   │   │   ├── rhf-slider.tsx
│   │   │   │   ├── rhf-switch.tsx
│   │   │   │   ├── rhf-text-field.tsx
│   │   │   │   └── schema-helper.ts
│   │   │   ├── iconify/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── flag-icon.tsx
│   │   │   │   ├── iconify.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── image/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── image.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── styles.css
│   │   │   │   └── types.ts
│   │   │   ├── label/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── label.tsx
│   │   │   │   ├── styles.ts
│   │   │   │   └── types.ts
│   │   │   ├── loading-screen/
│   │   │   │   ├── index.ts
│   │   │   │   ├── loading-screen.tsx
│   │   │   │   └── splash-screen.tsx
│   │   │   ├── logo/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── logo.tsx
│   │   │   ├── markdown/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── code-highlight-block.css
│   │   │   │   ├── html-tags.ts
│   │   │   │   ├── html-to-markdown.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── markdown.tsx
│   │   │   │   ├── styles.ts
│   │   │   │   └── types.ts
│   │   │   ├── nav-basic/
│   │   │   │   ├── desktop/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── nav-basic-desktop.tsx
│   │   │   │   │   ├── nav-item.tsx
│   │   │   │   │   └── nav-list.tsx
│   │   │   │   ├── mobile/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── nav-basic-mobile.tsx
│   │   │   │   │   ├── nav-item.tsx
│   │   │   │   │   └── nav-list.tsx
│   │   │   │   ├── classes.ts
│   │   │   │   ├── css-vars.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── nav-section/
│   │   │   │   ├── horizontal/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── nav-item.tsx
│   │   │   │   │   ├── nav-list.tsx
│   │   │   │   │   └── nav-section-horizontal.tsx
│   │   │   │   ├── mini/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── nav-item.tsx
│   │   │   │   │   ├── nav-list.tsx
│   │   │   │   │   └── nav-section-mini.tsx
│   │   │   │   ├── vertical/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── nav-item.tsx
│   │   │   │   │   ├── nav-list.tsx
│   │   │   │   │   └── nav-section-vertical.tsx
│   │   │   │   ├── classes.ts
│   │   │   │   ├── css-vars.ts
│   │   │   │   ├── hooks.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── styles.tsx
│   │   │   │   └── types.ts
│   │   │   ├── progress-bar/
│   │   │   │   ├── index.ts
│   │   │   │   ├── progress-bar.tsx
│   │   │   │   └── styles.css
│   │   │   ├── scrollbar/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── scrollbar.tsx
│   │   │   │   ├── styles.css
│   │   │   │   └── types.ts
│   │   │   ├── search-not-found/
│   │   │   │   ├── index.ts
│   │   │   │   └── search-not-found.tsx
│   │   │   ├── settings/
│   │   │   │   ├── context/
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── settings-provider.tsx
│   │   │   │   │   └── use-settings-context.ts
│   │   │   │   ├── drawer/
│   │   │   │   │   ├── base-option.tsx
│   │   │   │   │   ├── font-options.tsx
│   │   │   │   │   ├── fullscreen-button.tsx
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── nav-options.tsx
│   │   │   │   │   ├── presets-options.tsx
│   │   │   │   │   ├── settings-drawer.tsx
│   │   │   │   │   └── styles.tsx
│   │   │   │   ├── config-settings.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   ├── snackbar/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── snackbar.tsx
│   │   │   │   └── styles.tsx
│   │   │   ├── svg-color/
│   │   │   │   ├── classes.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── svg-color.tsx
│   │   │   │   └── types.ts
│   │   │   └── table/
│   │   │       ├── index.ts
│   │   │       ├── table-empty-rows.tsx
│   │   │       ├── table-head-custom.tsx
│   │   │       ├── table-no-data.tsx
│   │   │       ├── table-pagination-custom.tsx
│   │   │       ├── table-selected-action.tsx
│   │   │       ├── table-skeleton.tsx
│   │   │       ├── types.ts
│   │   │       ├── use-table.ts
│   │   │       └── utils.ts
│   │   ├── context/
│   │   │   ├── AdminContext.tsx
│   │   │   ├── GroupsContext.tsx
│   │   │   └── UserContext.tsx
│   │   ├── hooks/
│   │   │   ├── use-boolean.ts
│   │   │   ├── use-client-rect.ts
│   │   │   ├── use-copy-to-clipboard.ts
│   │   │   ├── use-countdown.ts
│   │   │   ├── use-debounce.ts
│   │   │   ├── use-double-click.ts
│   │   │   ├── use-event-listener.ts
│   │   │   ├── use-local-storage.ts
│   │   │   ├── use-responsive.ts
│   │   │   ├── use-scroll-offset-top.ts
│   │   │   ├── use-scroll-to-top.ts
│   │   │   ├── use-set-state.ts
│   │   │   └── use-tabs.ts
│   │   ├── layouts/
│   │   │   ├── auth-centered/
│   │   │   │   ├── index.ts
│   │   │   │   ├── layout.tsx
│   │   │   │   └── main.tsx
│   │   │   ├── auth-split/
│   │   │   │   ├── index.ts
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── main.tsx
│   │   │   │   └── section.tsx
│   │   │   ├── components/
│   │   │   │   ├── searchbar/
│   │   │   │   │   ├── index.tsx
│   │   │   │   │   ├── result-item.tsx
│   │   │   │   │   └── utils.ts
│   │   │   │   ├── account-button.tsx
│   │   │   │   ├── account-drawer.tsx
│   │   │   │   ├── account-popover.tsx
│   │   │   │   ├── contacts-popover.tsx
│   │   │   │   ├── language-popover.tsx
│   │   │   │   ├── menu-button.tsx
│   │   │   │   ├── nav-toggle-button.tsx
│   │   │   │   ├── sign-in-button.tsx
│   │   │   │   ├── sign-out-button.tsx
│   │   │   │   ├── theme-toggle-button.tsx
│   │   │   │   └── workspaces-popover.tsx
│   │   │   ├── core/
│   │   │   │   ├── header-section.tsx
│   │   │   │   └── layout-section.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── index.ts
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── main.tsx
│   │   │   │   ├── nav-horizontal.tsx
│   │   │   │   ├── nav-mobile.tsx
│   │   │   │   ├── nav-vertical.tsx
│   │   │   │   └── styles.ts
│   │   │   ├── simple/
│   │   │   │   ├── index.ts
│   │   │   │   ├── layout.tsx
│   │   │   │   └── main.tsx
│   │   │   ├── classes.ts
│   │   │   ├── config-nav-account.tsx
│   │   │   └── config-nav-dashboard.tsx
│   │   ├── locales/
│   │   │   ├── langs/
│   │   │   │   ├── ar/
│   │   │   │   │   ├── common.json
│   │   │   │   │   └── navbar.json
│   │   │   │   ├── cn/
│   │   │   │   │   ├── common.json
│   │   │   │   │   └── navbar.json
│   │   │   │   ├── en/
│   │   │   │   │   ├── common.json
│   │   │   │   │   └── navbar.json
│   │   │   │   ├── fr/
│   │   │   │   │   ├── common.json
│   │   │   │   │   └── navbar.json
│   │   │   │   └── vi/
│   │   │   │       ├── common.json
│   │   │   │       └── navbar.json
│   │   │   ├── utils/
│   │   │   │   └── number-format-locale.ts
│   │   │   ├── all-langs.ts
│   │   │   ├── config-locales.ts
│   │   │   ├── i18n-provider.tsx
│   │   │   ├── index.ts
│   │   │   ├── localization-provider.tsx
│   │   │   └── use-locales.ts
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   └── jwt/
│   │   │   │       ├── account-setup.tsx
│   │   │   │       ├── reset-password.tsx
│   │   │   │       ├── sign-in.tsx
│   │   │   │       └── sign-up.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── account/
│   │   │   │   │   ├── connectors/
│   │   │   │   │   │   ├── connector-settings.tsx
│   │   │   │   │   │   ├── googleWorkspace-business-config.tsx
│   │   │   │   │   │   └── googleWorkspace-individual-config.tsx
│   │   │   │   │   ├── ai-models-settings.tsx
│   │   │   │   │   ├── authentication-settings.tsx
│   │   │   │   │   ├── company-profile.tsx
│   │   │   │   │   ├── group-details.tsx
│   │   │   │   │   ├── personal-profile.tsx
│   │   │   │   │   ├── saml-sso-config.tsx
│   │   │   │   │   ├── services-settings.tsx
│   │   │   │   │   ├── user-and-groups.jsx
│   │   │   │   │   └── user-profile.tsx
│   │   │   │   ├── components/
│   │   │   │   │   └── full-name-dialog.tsx
│   │   │   │   ├── configuration-stepper/
│   │   │   │   │   ├── components/
│   │   │   │   │   │   └── stepper.tsx
│   │   │   │   │   └── services/
│   │   │   │   │       └── config-services.ts
│   │   │   │   ├── knowledgebase/
│   │   │   │   │   ├── knowledgebase-search.tsx
│   │   │   │   │   ├── knowledgebase.tsx
│   │   │   │   │   └── record-details.tsx
│   │   │   │   └── qna/
│   │   │   │       └── chatbot.tsx
│   │   │   ├── error/
│   │   │   │   ├── 403.tsx
│   │   │   │   ├── 404.tsx
│   │   │   │   └── 500.tsx
│   │   │   └── maintenance/
│   │   │       └── index.tsx
│   │   ├── routes/
│   │   │   ├── components/
│   │   │   │   ├── index.ts
│   │   │   │   └── router-link.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── index.ts
│   │   │   │   ├── use-active-link.ts
│   │   │   │   ├── use-params.ts
│   │   │   │   ├── use-pathname.ts
│   │   │   │   ├── use-router.ts
│   │   │   │   └── use-search-params.ts
│   │   │   ├── sections/
│   │   │   │   ├── auth.tsx
│   │   │   │   ├── dashboard.tsx
│   │   │   │   ├── index.tsx
│   │   │   │   └── main.tsx
│   │   │   ├── paths.ts
│   │   │   └── utils.ts
│   │   ├── sections/
│   │   │   ├── accountdetails/
│   │   │   │   ├── account-settings/
│   │   │   │   │   ├── ai-models/
│   │   │   │   │   │   ├── components/
│   │   │   │   │   │   │   ├── configure-model-dialog.tsx
│   │   │   │   │   │   │   ├── embedding-config-form.tsx
│   │   │   │   │   │   │   └── llm-config-form.tsx
│   │   │   │   │   │   ├── services/
│   │   │   │   │   │   │   └── universal-config.ts
│   │   │   │   │   │   ├── ai-models-settings.tsx
│   │   │   │   │   │   └── types.ts
│   │   │   │   │   ├── auth/
│   │   │   │   │   │   ├── components/
│   │   │   │   │   │   │   ├── auth-methods-header.tsx
│   │   │   │   │   │   │   ├── auth-methods-list.tsx
│   │   │   │   │   │   │   ├── azureAd-auth-form.tsx
│   │   │   │   │   │   │   ├── configure-method-dialog.tsx
│   │   │   │   │   │   │   ├── configure-smtp-dialog.tsx
│   │   │   │   │   │   │   ├── google-auth-form.tsx
│   │   │   │   │   │   │   ├── microsoft-auth-form.tsx
│   │   │   │   │   │   │   ├── oauth-auth-form.tsx
│   │   │   │   │   │   │   ├── saml-sso-config.tsx
│   │   │   │   │   │   │   └── smtp-config-form.tsx
│   │   │   │   │   │   ├── utils/
│   │   │   │   │   │   │   ├── auth-configuration-service.ts
│   │   │   │   │   │   │   └── validations.ts
│   │   │   │   │   │   └── authentication-settings.tsx
│   │   │   │   │   ├── connector/
│   │   │   │   │   │   ├── components/
│   │   │   │   │   │   │   ├── configure-connector-company-dialog.tsx
│   │   │   │   │   │   │   ├── configure-connector-individual-dialog.tsx
│   │   │   │   │   │   │   ├── connectors-header.tsx
│   │   │   │   │   │   │   ├── connectors-list.tsx
│   │   │   │   │   │   │   ├── google-workspace-config-company-form.tsx
│   │   │   │   │   │   │   └── google-workspace-config-individual-form.tsx
│   │   │   │   │   │   ├── connector-settings.tsx
│   │   │   │   │   │   ├── connector-stats.tsx
│   │   │   │   │   │   ├── googleWorkspace-business-config.tsx
│   │   │   │   │   │   └── googleWorkspace-individual-config.tsx
│   │   │   │   │   └── services/
│   │   │   │   │       ├── components/
│   │   │   │   │       │   ├── arangodb-config-form.tsx
│   │   │   │   │       │   ├── backend-nodejs-config-form.tsx
│   │   │   │   │       │   ├── connector-url-config-form.tsx
│   │   │   │   │       │   ├── frontend-url-config-form.tsx
│   │   │   │   │       │   ├── kafka-config-form.tsx
│   │   │   │   │       │   ├── mongodb-config-form.tsx
│   │   │   │   │       │   ├── qdrant-config-form.tsx
│   │   │   │   │       │   ├── redis-config-form.tsx
│   │   │   │   │       │   └── storage-service-form.tsx
│   │   │   │   │       ├── utils/
│   │   │   │   │       │   └── services-configuration-service.ts
│   │   │   │   │       ├── configure-services-dialog.tsx
│   │   │   │   │       ├── external-services-settings.tsx
│   │   │   │   │       ├── internal-services-settings.tsx
│   │   │   │   │       └── service-settings.tsx
│   │   │   │   ├── types/
│   │   │   │   │   ├── group-details.ts
│   │   │   │   │   ├── organization-data.ts
│   │   │   │   │   └── user-data.ts
│   │   │   │   ├── user-and-groups/
│   │   │   │   │   ├── group-details.tsx
│   │   │   │   │   ├── groups.tsx
│   │   │   │   │   ├── invites.tsx
│   │   │   │   │   ├── users-and-groups.tsx
│   │   │   │   │   └── users.tsx
│   │   │   │   ├── view/
│   │   │   │   │   ├── company-settings.tsx
│   │   │   │   │   └── index.ts
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── company-profile.tsx
│   │   │   │   ├── personal-profile.tsx
│   │   │   │   ├── user-profile.tsx
│   │   │   │   └── utils.ts
│   │   │   ├── coming-soon/
│   │   │   │   └── view.tsx
│   │   │   ├── error/
│   │   │   │   ├── 403-view.tsx
│   │   │   │   ├── 500-view.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── not-found-view.tsx
│   │   │   ├── knowledgebase/
│   │   │   │   ├── constants/
│   │   │   │   │   └── knowledge-search.ts
│   │   │   │   ├── types/
│   │   │   │   │   ├── departments.ts
│   │   │   │   │   ├── knowledge-base.ts
│   │   │   │   │   ├── modules.ts
│   │   │   │   │   ├── record-categories.ts
│   │   │   │   │   ├── record-details.ts
│   │   │   │   │   ├── records-ask-me-anything.ts
│   │   │   │   │   ├── search-response.ts
│   │   │   │   │   └── search-tags.ts
│   │   │   │   ├── ask-me-anything-sidebar.tsx
│   │   │   │   ├── ask-me-anything.tsx
│   │   │   │   ├── delete-record-dialog.tsx
│   │   │   │   ├── edit-record-dialog.tsx
│   │   │   │   ├── knowledge-base-details.tsx
│   │   │   │   ├── knowledge-base-search.tsx
│   │   │   │   ├── knowledge-base-sidebar.tsx
│   │   │   │   ├── knowledge-base.tsx
│   │   │   │   ├── knowledge-search-sidebar.tsx
│   │   │   │   ├── knowledge-search.tsx
│   │   │   │   ├── record-details.tsx
│   │   │   │   ├── show-documents.tsx
│   │   │   │   └── utils.ts
│   │   │   ├── maintenance/
│   │   │   │   └── view.tsx
│   │   │   ├── permission/
│   │   │   │   └── view.tsx
│   │   │   └── qna/
│   │   │       ├── chatbot/
│   │   │       │   ├── components/
│   │   │       │   │   ├── dialogs/
│   │   │       │   │   │   ├── archieve-chat-dialog.tsx
│   │   │       │   │   │   ├── delete-conversation-dialog.tsx
│   │   │       │   │   │   └── share-conversation-dialog.tsx
│   │   │       │   │   ├── mock/
│   │   │       │   │   │   └── citations.ts
│   │   │       │   │   ├── style/
│   │   │       │   │   │   ├── App.css
│   │   │       │   │   │   └── Spinner.css
│   │   │       │   │   ├── chat-header.tsx
│   │   │       │   │   ├── chat-input.tsx
│   │   │       │   │   ├── chat-message-area.tsx
│   │   │       │   │   ├── chat-message.tsx
│   │   │       │   │   ├── chat-sidebar.tsx
│   │   │       │   │   ├── citations-hover-card.tsx
│   │   │       │   │   ├── docx-highlighter.tsx
│   │   │       │   │   ├── excel-highlighter.tsx
│   │   │       │   │   ├── highlighter-sidebar.tsx
│   │   │       │   │   ├── html-highlighter.tsx
│   │   │       │   │   ├── markdown-highlighter.tsx
│   │   │       │   │   ├── message-feedback.tsx
│   │   │       │   │   ├── pdf-highlighter.tsx
│   │   │       │   │   ├── pdf-viewer.tsx
│   │   │       │   │   ├── record-details.tsx
│   │   │       │   │   ├── remove-button.tsx
│   │   │       │   │   ├── sample-pdf.pdf
│   │   │       │   │   ├── sources-citations.tsx
│   │   │       │   │   ├── text-highlighter.tsx
│   │   │       │   │   └── welcome-message.tsx
│   │   │       │   ├── utils/
│   │   │       │   │   └── styles/
│   │   │       │   │       ├── content-processing.ts
│   │   │       │   │       └── scrollbar.js
│   │   │       │   └── chat-bot.tsx
│   │   │       ├── utils/
│   │   │       │   └── styles/
│   │   │       │       └── scrollbar.js
│   │   │       └── view/
│   │   │           ├── chat-bot-view.tsx
│   │   │           └── index.ts
│   │   ├── store/
│   │   │   ├── authSlice.ts
│   │   │   ├── store.ts
│   │   │   └── userAndGroupsSlice.ts
│   │   ├── theme/
│   │   │   ├── core/
│   │   │   │   ├── components/
│   │   │   │   │   ├── accordion.tsx
│   │   │   │   │   ├── alert.tsx
│   │   │   │   │   ├── appbar.tsx
│   │   │   │   │   ├── autocomplete.tsx
│   │   │   │   │   ├── avatar.tsx
│   │   │   │   │   ├── backdrop.tsx
│   │   │   │   │   ├── badge.tsx
│   │   │   │   │   ├── breadcrumbs.tsx
│   │   │   │   │   ├── button-fab.tsx
│   │   │   │   │   ├── button-group.tsx
│   │   │   │   │   ├── button-toggle.tsx
│   │   │   │   │   ├── button.tsx
│   │   │   │   │   ├── card.tsx
│   │   │   │   │   ├── checkbox.tsx
│   │   │   │   │   ├── chip.tsx
│   │   │   │   │   ├── dialog.tsx
│   │   │   │   │   ├── drawer.tsx
│   │   │   │   │   ├── form.tsx
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── link.tsx
│   │   │   │   │   ├── list.tsx
│   │   │   │   │   ├── menu.tsx
│   │   │   │   │   ├── mui-x-data-grid.tsx
│   │   │   │   │   ├── mui-x-date-picker.tsx
│   │   │   │   │   ├── mui-x-tree-view.tsx
│   │   │   │   │   ├── pagination.tsx
│   │   │   │   │   ├── paper.tsx
│   │   │   │   │   ├── popover.tsx
│   │   │   │   │   ├── progress.tsx
│   │   │   │   │   ├── radio.tsx
│   │   │   │   │   ├── rating.tsx
│   │   │   │   │   ├── select.tsx
│   │   │   │   │   ├── skeleton.tsx
│   │   │   │   │   ├── slider.tsx
│   │   │   │   │   ├── stack.tsx
│   │   │   │   │   ├── stepper.tsx
│   │   │   │   │   ├── svg-icon.tsx
│   │   │   │   │   ├── switch.tsx
│   │   │   │   │   ├── table.tsx
│   │   │   │   │   ├── tabs.tsx
│   │   │   │   │   ├── textfield.tsx
│   │   │   │   │   ├── timeline.tsx
│   │   │   │   │   ├── tooltip.tsx
│   │   │   │   │   └── typography.tsx
│   │   │   │   ├── colors.json
│   │   │   │   ├── custom-shadows.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── palette.ts
│   │   │   │   ├── shadows.ts
│   │   │   │   └── typography.ts
│   │   │   ├── styles/
│   │   │   │   ├── index.ts
│   │   │   │   ├── mixins.ts
│   │   │   │   └── utils.ts
│   │   │   ├── with-settings/
│   │   │   │   ├── primary-color.json
│   │   │   │   ├── right-to-left.tsx
│   │   │   │   └── update-theme.ts
│   │   │   ├── create-theme.ts
│   │   │   ├── overrides-theme.ts
│   │   │   ├── scheme-config.ts
│   │   │   ├── theme-provider.tsx
│   │   │   └── types.ts
│   │   ├── types/
│   │   │   ├── blog.ts
│   │   │   ├── calendar.ts
│   │   │   ├── chat-bot.ts
│   │   │   ├── chat-message.ts
│   │   │   ├── chat-sidebar.ts
│   │   │   ├── chat.ts
│   │   │   ├── common.ts
│   │   │   └── pdf-highlighter.ts
│   │   ├── utils/
│   │   │   ├── axios.tsx
│   │   │   ├── change-case.ts
│   │   │   ├── format-number.ts
│   │   │   ├── format-time.ts
│   │   │   ├── helper.ts
│   │   │   ├── storage-available.ts
│   │   │   └── uuidv4.ts
│   │   ├── app.tsx
│   │   ├── config-global.ts
│   │   ├── global.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── .editorconfig
│   ├── .env.template
│   ├── .eslintignore
│   ├── .eslintrc.cjs
│   ├── .gitignore
│   ├── .prettierignore
│   ├── Dockerfile
│   ├── README.md
│   ├── env.template
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── prettier.config.mjs
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vercel.json
│   ├── vite.config.ts
│   └── yarn.lock
├── .dockerignore
├── .gitignore
├── CONTRIBUTING.md
├── Dockerfile
├── Dockerfile.cloud
├── LICENSE
├── README.md
└── generate_filetree.py
```

## Project Structure Overview

### File Types Distribution

- `.ts`: 438 files
- `.tsx`: 329 files
- `.py`: 157 files
- `.json`: 23 files
- `no extension`: 15 files
- `.svg`: 13 files
- `.md`: 12 files
- `.hbs`: 11 files
- `.css`: 9 files
- `.template`: 8 files
- `.yml`: 4 files
- `.sh`: 2 files
- `.ttf`: 2 files
- `.js`: 2 files
- `.cloud`: 1 files
- `.yaml`: 1 files
- `.toml`: 1 files
- `.cjs`: 1 files
- `.html`: 1 files
- `.mjs`: 1 files