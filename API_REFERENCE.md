# FCM (Content Manager) API Reference — http://<FCM_HOST>

Generated from the live OpenAPI spec (`/apis/docs-json`), API **Content Manager API v1.1.0**. **194 endpoints** across **26 groups**.

> [!TIP]
> Interactive Swagger UI: http://<FCM_HOST>/apis/docs · Raw spec: http://<FCM_HOST>/apis/docs-json

## 1. Authentication

All endpoints (except `auth/signin`, `auth/signup`, SSO and the webhook) require `Authorization: Bearer <accessToken>`. The access token lasts **30 min**; use the refresh token to renew.

```bash
# Set these first (see .env.example)
export FCM_HOST="<FCM_HOST>"          # e.g. 203.0.113.10 or fcm.example.com
export FCM_EMAIL="<FCM_EMAIL>"        # e.g. user@example.com
export FCM_PASSWORD="<FCM_PASSWORD>"
BASE=http://$FCM_HOST/apis/v1

# Sign in -> {"accessToken": "...", "refreshToken": "..."}
RESP=$(curl -s -X POST $BASE/auth/signin -H 'Content-Type: application/json' \
  -d "{\"email\":\"$FCM_EMAIL\",\"password\":\"$FCM_PASSWORD\"}")
TOKEN=$(echo "$RESP" | jq -r .accessToken)
REFRESH_TOKEN=$(echo "$RESP" | jq -r .refreshToken)

# Call any endpoint
curl -s $BASE/instances -H "Authorization: Bearer $TOKEN" | jq .

# Refresh (verified): send refreshToken in a JSON body -> {"accessToken": "..."}
# (Sending it as a Bearer header returns HTTP 500.)
curl -s -X POST $BASE/auth/refresh -H 'Content-Type: application/json' \
  -d "{\"refreshToken\":\"$REFRESH_TOKEN\"}"
```

Paginated list endpoints accept `?page=` and `?size=` and wrap results in `{"data": [...]}`.

> [!WARNING]
> If your FCM server is served over plain HTTP, credentials travel unencrypted. Never commit real hosts, emails, passwords or tokens — keep them in environment variables.

**Legend:** `{param}` = path parameter · `?q` = query parameters · `*` = required field.

## 2. Endpoint Index

| Group | # |
|---|---|
| [rules](#rules) | 9 |
| [reflists](#reflists) | 6 |
| [repos](#repos) | 8 |
| [user management](#user-management) | 4 |
| [role management](#role-management) | 5 |
| [permission set](#permission-set) | 5 |
| [permissions](#permissions) | 1 |
| [custom-parsers](#custom-parsers) | 6 |
| [data-tables](#data-tables) | 6 |
| [extensions](#extensions) | 6 |
| [feeds](#feeds) | 6 |
| [dashboards](#dashboards) | 6 |
| [exclusions](#exclusions) | 6 |
| [instances](#instances) | 34 |
| [audit-log](#audit-log) | 1 |
| [curated-rules](#curated-rules) | 3 |
| [publisher](#publisher) | 42 |
| [rule validation](#rule-validation) | 3 |
| [webhooks](#webhooks) | 1 |
| [DummyValidation](#dummyvalidation) | 1 |
| [auth](#auth) | 8 |
| [release-notes](#release-notes) | 3 |
| [static-info](#static-info) | 4 |
| [maintenance](#maintenance) | 6 |
| [adoption](#adoption) | 6 |
| [tags](#tags) | 8 |

## 3. Endpoints by Group

### rules

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/rules` | List all rules | ?`id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `tags`, `plainList`, `page`, `size` |
| `POST` | `/rules` | Create new Rule | **RuleInfo** — `fileName`: string, `content`*: string, `repository`: string, `subtitle`: string, `roleId`: string |
| `GET` | `/rules/references` | Get reference lists and data tables associated with rules | ?`ruleIds`* |
| `GET` | `/rules/filters` | Get the info for the rules filters | — |
| `POST` | `/rules/validate` | Validate Rule | ?`referenceLists`*<br>**ValidateRuleDTO** — `id`: string, `repository`: string, `fileName`: string, `content`*: string, `subtitle`: string, `roleId`: string |
| `POST` | `/rules/create-multiple` | Create new Rules | **[RuleInfo]** — `fileName`: string, `content`*: string, `repository`: string, `subtitle`: string, `roleId`: string |
| `PATCH` | `/rules/{ruleID}` | Edit rule details (name,content and repository) | **EditRuleDTO** — `fileName`: string, `content`: string, `repository`: string, `subtitle`: string, `roleId`: string |
| `GET` | `/rules/{ruleId}` | Get rule info | — |
| `DELETE` | `/rules/{ruleId}` | Delete rule | — |

### reflists

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/reflists` | List all reference lists | ?`id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `tags`, `plainList`, `page`, `size` |
| `GET` | `/reflists/filters` | Get the info for the reference lists filters | — |
| `POST` | `/reflists/create-multiple` | Create/edit multiple reference lists | **[RefListDetails]** — `name`: string, `subtitle`: string, `description`: string, `content`: string, `contentType`: string (CONTENT_TYPE_DEFAULT_STRING\|REGEX\|CIDR), `repository`: string, `fileName`: string, `roleId`: string, `id`: string |
| `PATCH` | `/reflists/{reflistId}` | Edit reference list details (content and repository) | **EditRefListDTO** — `content`: string, `repository`: string, `fileName`: string, `description`: string, `subtitle`: string, `contentType`: string (CONTENT_TYPE_DEFAULT_STRING\|REGEX\|CIDR), `roleId`: string |
| `DELETE` | `/reflists/{reflistId}` | Delete reference list | — |
| `GET` | `/reflists/{refListId}` | Get reference list info | — |

### repos

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/repositories` | List all repos | ?`pullBeginDate`, `pullEndDate`, `pushBeginDate`, `pushEndDate`, `permissions`, `libraryStatus`, `page`, `size` |
| `POST` | `/repositories` | Create new repository | **CreateRepositoryDTO** — `name`*: string, `url`*: string, `serviceAccount`*: string, `status`*: boolean, `repoVendor`*: string (github\|gitlab), `roleId`*: string |
| `GET` | `/repositories/filters` | List all repositories filter info | — |
| `POST` | `/repositories/validate` | Validate if a repository can be linked | **ValidateRepositoryDTO** — `url`*: string, `serviceAccount`*: string, `repoVendor`*: string (github\|gitlab), `edit`: boolean |
| `POST` | `/repositories/init/{repoId}` | Create Default Folder Structure | — |
| `PATCH` | `/repositories/{repoId}` | Edit repository (name,service account and status) | **EditRepositoryDTO** — `name`: string, `serviceAccount`: string, `status`: boolean, `repoVendor`*: string (github\|gitlab) |
| `DELETE` | `/repositories/{repoId}` | Delete repository | — |
| `POST` | `/repositories/{repositoryId}/{action}` | Sync rules to Github | — |

### user management

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/users` | List users and their tenant memberships | ?`id`, `name`, `searchTerm`, `page`, `size` |
| `POST` | `/users` | Onboard new user with group access | **CreateUserReqDto** — `email`*: string, `name`*: string, `groupIds`*: string[], `roleId`*: string, `userType`*: string (superAdmin\|groupAdmin), `permissionSetId`*: string |
| `PATCH` | `/users/{id}` | Update profile and modify group access | **UpdateUserReqDto** — `email`: string, `name`: string, `roleId`: string, `userType`: string (superAdmin\|groupAdmin), `groupIds`: string[], `permissionSetId`: string |
| `DELETE` | `/users/{id}` | Delete user | — |

### role management

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/roles` | List all roles. | ?`id`, `name`, `searchTerm`, `page`, `size` |
| `POST` | `/roles` | Create custom role. | **CreateRoleReq** — `displayName`*: string, `description`*: string |
| `GET` | `/roles/{id}` | Get specific role. | — |
| `PATCH` | `/roles/{id}` | Update role. | **UpdateRoleReq** — `displayName`: string, `description`: string |
| `DELETE` | `/roles/{id}` | Delete role. | — |

### permission set

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/permission-sets` | List all permission sets | ?`searchTerm` |
| `POST` | `/permission-sets` | Create a new permission set | **CreatePermissionSetDto** — `name`*: string, `description`: string, `permissionIds`: string[] |
| `GET` | `/permission-sets/{id}` | Get a permission set by ID | — |
| `PUT` | `/permission-sets/{id}` | Update permission set | **UpdatePermissionSetDto** — `name`: string, `description`: string, `permissionIds`: string[] |
| `DELETE` | `/permission-sets/{id}` | Delete permission set | — |

### permissions

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/permissions` | List all available permissions | — |

### custom-parsers

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/custom-parsers` | List all custom parsers | ?`logtypes`, `tags`, `id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `plainList`, `page`, `size` |
| `GET` | `/custom-parsers/filters` | Get the info for the custom parsers filters | — |
| `GET` | `/custom-parsers/{parserId}` | Get custom parser info | — |
| `PATCH` | `/custom-parsers/{parserId}` | Edit custom parser details (content, repository and status) | **EditCustomParserDTO** — `subtitle`: string, `description`: string, `content`: string, `fileName`: string, `repository`: string, `roleId`: string |
| `DELETE` | `/custom-parsers/{parserId}` | Delete custom parser | — |
| `POST` | `/custom-parsers/create-multiple` | Create multiple custom parsers | **[CreateCustomParserDTO]** — `logtype`*: string, `subtitle`: string, `description`: string, `content`*: string, `fileName`: string, `repository`: string, `roleId`: string |

### data-tables

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/data-tables` | List all data tables | ?`id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `tags`, `plainList`, `page`, `size` |
| `GET` | `/data-tables/filters` | Get the info for the data tables filters | — |
| `POST` | `/data-tables/create-multiple` | Create multiple data tables | **[CreateDataTableDTO]** — `name`*: string, `subtitle`: string, `description`: string, `content`*: string, `contentType`*: string[], `mappedColumnPath`*: string[], `repository`: string, `fileName`: string, `roleId`: string |
| `GET` | `/data-tables/{dataTableID}` | Get data table info | — |
| `PATCH` | `/data-tables/{dataTableID}` | Edit data table details | **EditDataTableDTO** — `subtitle`: string, `description`: string, `content`: string, `contentType`: string[], `mappedColumnPath`: string[], `repository`: string, `fileName`: string, `roleId`: string |
| `DELETE` | `/data-tables/{dataTableID}` | Delete data table | — |

### extensions

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/extensions` | List all extensions | ?`logtypes`, `tags`, `id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `plainList`, `page`, `size` |
| `GET` | `/extensions/filters` | Get the info for the extensions filters | — |
| `GET` | `/extensions/{extensionId}` | Get extension info | — |
| `PATCH` | `/extensions/{extensionId}` | Edit extension | **EditExtensionDTO** — `subtitle`: string, `description`: string, `content`: string, `fileName`: string, `repository`: string, `roleId`: string |
| `DELETE` | `/extensions/{extensionId}` | Delete extension | — |
| `POST` | `/extensions/create-multiple` | Create multiple custom parsers | **[CreateExtensionDTO]** — `logtype`*: string, `subtitle`: string, `description`: string, `content`*: string, `fileName`: string, `repository`: string, `roleId`: string |

### feeds

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `POST` | `/feeds/create-multiple` | Create multiple feeds | **[CreateFeedDTO]** — `feedName`*: string, `feedType`*: string (AMAZON_S3\|AZURE_BLOBSTORE\|GOOGLE_CLOUD_STORAGE\|AMAZON_S3_V2\|AZURE_BLOBSTORE_V2\|GOOGLE_CLOUD_STORAGE_V2), `subtitle`: string, `description`: string, `logType`*: string, `details`*: object, `repository`: string, `fileName`: string, `assetNamespace`: string, `labels`: object, `roleId`: string |
| `GET` | `/feeds` | Get all feeds | ?`tags`, `id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `plainList`, `page`, `size` |
| `GET` | `/feeds/filters` | Get the info for the feeds filters | — |
| `GET` | `/feeds/{feedId}` | Get a specific feed | — |
| `PATCH` | `/feeds/{feedId}` | Update a feed | **EditFeedDTO** — `feedName`: string, `subtitle`: string, `description`: string, `details`: object, `repository`: string, `fileName`: string, `assetNamespace`: string, `labels`: object, `roleId`: string |
| `DELETE` | `/feeds/{feedId}` | Delete feed | — |

### dashboards

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `POST` | `/dashboards/create-multiple` | Create multiple dashboards | **[CreateDashboardsDTO]** — `dashboards`*: CreateDashboardDTO[] |
| `GET` | `/dashboards` | Get all dashboards | ?`tags`, `id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `plainList`, `page`, `size` |
| `GET` | `/dashboards/filters` | Get the info for the dashboards filters | — |
| `GET` | `/dashboards/{dashboardId}` | Get a specific dashboard | — |
| `PATCH` | `/dashboards/{dashboardId}` | Update a dashboard | **EditDashboardDTO** — `fileName`: string, `subtitle`: string, `description`: string, `repository`: string, `dashboard`: object, `dashboardCharts`: object[], `dashboardQueries`: object[], `roleId`: string |
| `DELETE` | `/dashboards/{dashboardId}` | Delete dashboard | — |

### exclusions

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/exclusions` | List all exclusions | ?`id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `repositories`, `authors`, `instances`, `tags`, `plainList`, `page`, `size` |
| `GET` | `/exclusions/filters` | Get the info for the exclusions filters | — |
| `GET` | `/exclusions/{exclusionId}` | Get exclusion info | — |
| `PATCH` | `/exclusions/{exclusionId}` | Edit exclusion details (content, repository and status) | **EditExclusionDTO** — `name`: string, `subtitle`: string, `description`: string, `query`: ExclusionQuery[], `curatedRuleItems`: string[], `fileName`: string, `repository`: string |
| `DELETE` | `/exclusions/{exclusionId}` | Delete exclusion | — |
| `POST` | `/exclusions/create-multiple` | Create multiple exclusions | **[CreateExclusionDTO]** — `name`*: string, `subtitle`: string, `description`: string, `query`*: ExclusionQuery[], `curatedRuleItems`*: string[], `fileName`: string, `repository`: string |

### instances

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/instances` | List all instances | ?`groups`, `discovery`, `alphaV1APIConfigured`, `page`, `size` |
| `POST` | `/instances` | Create new Instance | **CreateInstanceDTO** — `url`*: string, `name`*: string, `groups`: string[], `serviceAccount`*: object, `alphaV1Credentials`: AlphaV1Credentials, `customerId`: string, `projectNumber`: string |
| `GET` | `/instances/filters` | List all instances filter info | — |
| `GET` | `/instances/{instanceID}/deployed-rules` | Return instance info and rules | ?`lastChangedBeginDate`, `lastChangedEndDate`, `live`, `severity`, `alerting`, `author`, `origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-rules/filters` | Get the info for the rules filters in instance | — |
| `GET` | `/instances/{instanceID}/deployed-reflists` | Return instance info and reflists | ?`origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-reflists/filters` | Get the info for the reference lists filters in instance | — |
| `GET` | `/instances/{instanceID}/deployed-custom-parsers` | Return instance info and custom parsers | ?`lastChangedBeginDate`, `lastChangedEndDate`, `origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-custom-parsers/filters` | Return instance info and custom parsers | — |
| `GET` | `/instances/{instanceID}/deployed-extensions` | Return instance info and extensions | ?`lastChangedBeginDate`, `lastChangedEndDate`, `origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-extensions/filters` | Return instance info and extensions | — |
| `GET` | `/instances/{instanceID}/deployed-feeds` | Return instance info and feeds | — |
| `GET` | `/instances/{instanceID}/deployed-feeds/filters` | Return feed filters | — |
| `GET` | `/instances/{instanceID}/deployed-data-tables` | Return instance info and data tables | ?`lastChangedBeginDate`, `lastChangedEndDate`, `origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-data-tables/filters` | Return instance info and custom parsers | — |
| `GET` | `/instances/{instanceID}/deployed-curated-rules` | Return instance info and curated rules | ?`lastChangedBeginDate`, `lastChangedEndDate`, `origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-curated-rules/filters` | Return instance info and curated rules | — |
| `GET` | `/instances/{instanceID}/deployed-exclusions` | Return instance info and exclusions | ?`lastChangedBeginDate`, `lastChangedEndDate`, `origin`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `page`, `size` |
| `GET` | `/instances/{instanceID}/deployed-exclusions/filters` | Return instance info and custom parsers | — |
| `GET` | `/instances/{instanceID}/deployed-dashboards` | Return instance info and dashboards | — |
| `GET` | `/instances/{instanceID}/deployed-dashboards/filters` | Return dashboard filters | — |
| `POST` | `/instances/validate` | Validate if an instance can be linked | **ValidateInstanceDTO** — `url`*: string, `serviceAccount`*: object |
| `GET` | `/instances/mssp` | Run MSSP Cron Job | — |
| `POST` | `/instances/mssp` | Create Multiple Instances with MSSP | **MSSPInfo** — `name`*: string, `region`*: string, `serviceAccount`*: object |
| `POST` | `/instances/mssp/validate` | Validate MSSP credentials | **MSSPInfo** — `name`*: string, `region`*: string, `serviceAccount`*: object |
| `PATCH` | `/instances/{instanceID}` | Edit instance details (groups, name, service account or platform status) | **EditInstanceDTO** — `groups`: string[], `name`: string, `serviceAccount`: object, `discovery`: boolean |
| `GET` | `/instances/{instanceID}` | Return instance info | — |
| `POST` | `/instances/alphav1/{instanceID}` | Validate alphaV1 credentials | **AlphaV1Credentials** — `serviceAccount`*: object, `customerId`*: string, `projectNumber`*: string |
| `PATCH` | `/instances/alphav1/{instanceID}` | Edit instance credentials from alphav1 | **AlphaV1Credentials** — `serviceAccount`*: object, `customerId`*: string, `projectNumber`*: string |
| `GET` | `/instances/groups` | List all groups | ?`page`, `size` |
| `POST` | `/instances/groups` | Create group | **CreateGroupDTO** — `name`*: string, `instances`*: string[] |
| `PATCH` | `/instances/groups/{groupId}` | Edit group | **CreateGroupDTO** — `name`*: string, `instances`*: string[] |
| `DELETE` | `/instances/groups/{groupId}` | Delete group | — |
| `DELETE` | `/instances/{instanceID}/{deleteMode}` | Delete instance | ?`type` |

### audit-log

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/audit-log` | List all logs | ?`id`, `action`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `author`, `page`, `size` |

### curated-rules

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/curated-rules` | List all curated rules | ?`id`, `name`, `searchTerm`, `createdBeginDate`, `createdEndDate`, `modifiedBeginDate`, `modifiedEndDate`, `instances`, `page`, `size`, `onlySets` |
| `GET` | `/curated-rules/filters` | Get the info for the curated rules filters | — |
| `GET` | `/curated-rules/{curatedRuleId}` | Get curated rule info | — |

### publisher

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/publisher` | List all publications | — |
| `GET` | `/publisher/update-curated` | Update curated rule | — |
| `GET` | `/publisher/audit-log` | List all tasks for audit log | ?`page`, `size` |
| `GET` | `/publisher/audit-log/{taskId}` | List a task's subtasks info | ?`page`, `size`, `searchTerm` |
| `GET` | `/publisher/{id}` | List subtasks from task | — |
| `POST` | `/publisher/publish-multiple` | Publish content | **CreatePublicationDTO** — `contentItems`*: ContentPublicationItem[] |
| `POST` | `/publisher/archive` | Unpublish rule | ?`name`<br>**ArchiveManagementDTO** — `instanceId`*: string, `ruleId`*: string |
| `POST` | `/publisher/curated-capacity` | List the capacity of the curated rules in an instance | **InstanceListDTO** — `instances`*: string[] |
| `POST` | `/publisher/{instanceId}/deployed-curated-rules-populate` | Save curated rules in our database | — |
| `POST` | `/publisher/{instanceId}/curated-content-availability` | Check if curated content are available in an instance | **CheckCuratedContentDTO** — `exclusionId`*: string |
| `GET` | `/publisher/{ruleId}/deployed-rules` | List the status and data of the rule in instances | ?`live`, `alerting`, `severity`, `lastPublishedBeginDate`, `lastPublishedEndDate`, `deployment`, `page`, `size` |
| `GET` | `/publisher/{instanceID}/deployed-rules/{ruleId}` | Return rule that exists in an instance | — |
| `PATCH` | `/publisher/{instanceID}/deployed-rules/{ruleId}` | Edit rule in instance | ?`name`<br>**EditRuleInInstance** — `live`: boolean, `alerting`: boolean, `runFrequency`: string (LIVE\|HOURLY\|DAILY) |
| `GET` | `/publisher/{reflistId}/deployed-reflists` | List all instances that have the reference list | — |
| `GET` | `/publisher/{instanceID}/deployed-reflists/{refListName}` | Return reference list that exists in an instance | — |
| `GET` | `/publisher/{parserId}/deployed-custom-parsers` | List the status and data of the custom parser in instances | — |
| `GET` | `/publisher/{instanceID}/deployed-custom-parsers/{logtype}/{parserId}` | Return custom parser that exists in an instance | — |
| `PATCH` | `/publisher/{instanceID}/deployed-custom-parsers/{logtype}/{parserId}` | Edit rule in instance | ?`status`* |
| `DELETE` | `/publisher/{instanceID}/deployed-custom-parsers/{logtype}/{parserId}` | Delete custom parser in instance | — |
| `GET` | `/publisher/{exclusionId}/deployed-exclusions` | List the status and data of the exclusions in instances | — |
| `GET` | `/publisher/{instanceID}/deployed-exclusions/{exclusionId}` | Return exclusion that exists in an instance | — |
| `PATCH` | `/publisher/{instanceID}/deployed-exclusions/{exclusionId}` | Edit exclusion in instance | ?`status`* |
| `DELETE` | `/publisher/{instanceID}/deployed-exclusions/{exclusionId}` | Delete exclusion in instance | — |
| `GET` | `/publisher/{extensionId}/deployed-extensions` | List the status and data of the extension in instances | — |
| `GET` | `/publisher/{instanceID}/deployed-extensions/{logtype}/{extensionId}` | Return extension that exists in an instance | — |
| `PATCH` | `/publisher/{instanceID}/deployed-extensions/{logtype}/{extensionId}` | Edit extension in instance | ?`status`* |
| `DELETE` | `/publisher/{instanceID}/deployed-extensions/{logtype}/{extensionId}` | Delete extension in instance | — |
| `GET` | `/publisher/{feedId}/deployed-feeds` | List the status and data of the feed in instances | — |
| `GET` | `/publisher/{instanceID}/deployed-feeds/{feedId}` | Return feed that exists in an instance | — |
| `PATCH` | `/publisher/{instanceID}/deployed-feeds/{feedId}` | Edit feed in instance | ?`status`* |
| `DELETE` | `/publisher/{instanceID}/deployed-feeds/{feedId}` | Delete feed in instance | — |
| `POST` | `/publisher/{instanceID}/deployed-content` | Get content deployment status in instance | **ContentIds** — `rulesIds`*: string[], `refListsIds`*: string[], `customParsersIds`*: string[], `feedsIds`*: string[], `dataTablesIds`*: string[], `extensionsIds`*: string[], `exclusionsIds`*: string[], `dashboardsIds`*: string[] |
| `GET` | `/publisher/{instanceID}/siem-content-info` | Return content info from instance | ?`contentType`*, `contentId`* |
| `GET` | `/publisher/{dataTableId}/deployed-data-tables` | List all instances that have the data table | — |
| `GET` | `/publisher/{instanceID}/deployed-data-tables/{dataTableName}` | Return data table that exists in an instance | — |
| `DELETE` | `/publisher/{instanceID}/deployed-data-tables/{dataTableName}` | Delete data table in instance | — |
| `GET` | `/publisher/{curatedRuleId}/deployed-curated-rules` | List the status and data of the curated rule in instances | — |
| `GET` | `/publisher/{instanceID}/deployed-curated-rules/{curatedRuleId}` | Edit curated rule in instance | — |
| `PATCH` | `/publisher/{instanceID}/deployed-curated-rules/{curatedRuleId}` | Edit curated rule in instance | **EditCuratedRuleInInstance** — `precise`*: CuratedPrecisionDTO, `broad`*: CuratedPrecisionDTO |
| `GET` | `/publisher/{dashboardId}/deployed-dashboards` | List the status and data of the dashboard in instances | — |
| `GET` | `/publisher/{instanceID}/deployed-dashboards/{dashboardId}` | Return dashboard that exists in an instance | — |
| `DELETE` | `/publisher/{instanceID}/deployed-dashboards/{dashboardId}` | Delete dashboard in instance | — |

### rule validation

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/rules-validation/validation-status` | Get validation service status | — |
| `POST` | `/rules-validation/validations` | Request a rule validation | **CreateValidationDto** — `ruleIds`*: string[] |
| `GET` | `/rules-validation/validations/{id}` | Check validation job status | — |

### webhooks

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `POST` | `/webhooks/validation/rule-validations` | Handle validation webhook | **ValidationWebhookPayloadDto** — `internalValidationId`*: string, `results`*: RuleValidationResultDto[] |

### DummyValidation

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `POST` | `/dummy-validation` | DummyValidationController_dummyValidation | — |

### auth

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `POST` | `/auth/refresh` | AuthController_refresh | — |
| `GET` | `/auth/sso/saml/login` | AuthController_samlLogin | — |
| `POST` | `/auth/sso/saml/ac` | AuthController_samlAssertionConsumer | — |
| `GET` | `/auth/profile` | AuthController_getProfile | — |
| `GET` | `/auth/sso/saml/metadata` | AuthController_getSpMetadata | — |
| `POST` | `/auth/signup` | AuthController_signup | **CreateUserDTO** — `email`*: string, `name`: string, `password`: string |
| `POST` | `/auth/verify` | AuthController_verifyAccount | ?`code`*, `email`* |
| `POST` | `/auth/signin` | AuthController_signin | **CreateUserDTO** — `email`*: string, `name`: string, `password`: string |

### release-notes

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/release-notes` | Published release notes, newest first | — |
| `GET` | `/release-notes/status` | Whether this user has an unseen release | — |
| `POST` | `/release-notes/seen` | Dismiss the What's new dialog for the calling user | — |

### static-info

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/static-info/{type}` | List all info | ?`page`, `size`, `searchTerm` |
| `POST` | `/static-info/create-multiple` | Create multiple info | **[CreateInfo]** — `type`*: string (LOGTYPE\|REGION\|DATATABLES_MAPPING\|EXCLUSIONS_FIELD), `data`*: object |
| `PATCH` | `/static-info/{infoId}` | Update a info | **CreateInfo** — `type`*: string (LOGTYPE\|REGION\|DATATABLES_MAPPING\|EXCLUSIONS_FIELD), `data`*: object |
| `DELETE` | `/static-info/{infoId}` | Delete info | — |

### maintenance

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/maintenance/cron-lock` | Get state of cron job lock | — |
| `POST` | `/maintenance/cron-lock` | Update state of cron job lock | ?`state`* |
| `GET` | `/maintenance/update-notpublished-to-failed` | Update all NotPublished states to Failed state | — |
| `GET` | `/maintenance/interrupt-ongoing-publications` | Update all expired publications to failed state | ?`id` |
| `GET` | `/maintenance/SIEM-duplicates/{ids}` | List duplicate SIEM entries | — |
| `DELETE` | `/maintenance/SIEM-duplicates/{ids}` | Delete duplicate SIEM entries | — |

### adoption

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/adoption/library-content` | Get library content with conflicts for adoption | ?`comparisonType`*, `repoIDs`, `contentType`, `instanceIDs` |
| `POST` | `/adoption/library-content` | Get library content with conflicts for adoption (large selection) | **LibraryContentBodyDTO** — `comparisonType`*: string (NAME\|NAME_CONTENT), `contentType`: string (Rule\|ReferenceList\|CustomParser\|Extension\|Feed\|DataTable…), `instanceIDs`: string[], `repoIDs`: string |
| `GET` | `/adoption/instance-content` | Get instance content with conflicts for adoption | ?`comparisonType`*, `contentIDs`*, `instanceIDs`*, `contentType`* |
| `POST` | `/adoption/instance-content` | Get instance content with conflicts for adoption (large selection) | **InstanceContentBodyDTO** — `comparisonType`*: string (NAME\|NAME_CONTENT), `contentType`*: string (Rule\|ReferenceList\|CustomParser\|Extension\|Feed\|DataTable…), `contentIDs`*: string[], `instanceIDs`*: string[] |
| `POST` | `/adoption/create-assoc` | Associate content between instances and FCM | **AssociationRequestDTO** — `assoc`*: AssocEntryDTO[] |
| `POST` | `/adoption/sync-instance-rules` | Sync rules from a Chronicle instance | **SyncInstanceRulesDTO** — `instanceId`*: string, `ruleIds`: string[] |

### tags

| Method | Path | Description | Query / Body |
|---|---|---|---|
| `GET` | `/tags` | List the global tag catalog | — |
| `POST` | `/tags` | Create a tag | **TagNameDTO** — `name`*: string |
| `GET` | `/tags/associations` | Tags attached to content items, keyed by content id | ?`contentType`*, `contentIds` |
| `POST` | `/tags/associations` | Attach tags to one or more content items (bulk-capable) | **TagAssociationsDTO** — `tagIds`*: string[], `items`*: ContentRefDTO[] |
| `DELETE` | `/tags/associations` | Detach tags from one or more content items | **TagAssociationsDTO** — `tagIds`*: string[], `items`*: ContentRefDTO[] |
| `GET` | `/tags/{id}` | Get a tag and the content it is attached to | — |
| `PATCH` | `/tags/{id}` | Rename a tag (its slug stays fixed) | **TagNameDTO** — `name`*: string |
| `DELETE` | `/tags/{id}` | Delete a tag and detach it from all content items | — |
