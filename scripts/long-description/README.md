# Long Description

This script is used return all services, but include their long descriptions (with HTML tags and such).

## Instructions

Copy [configuration-example.py](configuration-example.py) to configuration.py and modify as needed.

## Changelog

#### 2018-10-15 (JIRA: CO-1225)

Rename fields and change the data type to string for ID fields (`categoryID`, `configurationItemID`, `maintenanceScheduleID`, `requestApplicationID`, `requestTypeCategoryID` and `requestTypeID`). For renaming fields, basically just follow camelCase naming convention and also change some fields to improve readibility. The following table show all old field names with their new names:

| Old Field Name | New Field Name|
|----------------|---------------|
| Attachments | attachments |
| CategoriesParsedFromFullCategoryText | categories |
| CategoryID | categoryID |
| CategoryName | categoryName |
| CompositeName | compositeName |
| ConfigurationItemID | configurationItemID |
| FullCategoryText | fullCategoryText |
| ID | **This field has been removed** |
| IsActive | isActive |
| IsPublic | isPublic |
| LongDescription | longDescription |
| MaintenanceScheduleID | maintenanceScheduleID |
| MaintenanceScheduleName | maintenanceScheduleName |
| ManagerFullName | managerFullName |
| ManagerUid | managerUid |
| ManagingGroupID | managingGroupID |
| ManagingGroupName | managingGroupName |
| Name | name |
| NewTicketUrl | newTicketUrl |
| Order | order |
| RequestApplicationID | requestApplicationID |
| RequestApplicationIsActive | requestApplicationIsActive |
| RequestApplicationName | requestApplicationName |
| RequestText | requestText |
| RequestTypeCategoryID | requestTypeCategoryID |
| RequestTypeCategoryName | requestTypeCategoryName |
| RequestTypeComponent | requestTypeComponent |
| RequestTypeID | requestTypeID |
| RequestTypeIsActive | requestTypeIsActive |
| RequestTypeName | requestTypeName |
| RequestUrl | requestUrl |
| ShortDescription | shortDescription |
| SpanTagsParsedFromLongDescription | **This field has been removed. All fields under this field are collapsed to be in the same attributes object as the other fields** |
| SpanTagsParsedFromLongDescription['AccessRequirements'] | accessRequirements |
| SpanTagsParsedFromLongDescription['AdditionalLinkTitle'] | additionalLinkTitle |
| SpanTagsParsedFromLongDescription['AdditionalLinkURL'] | additionalLinkURL |
| SpanTagsParsedFromLongDescription['AudienceAssociated'] | audienceAssociated |
| SpanTagsParsedFromLongDescription['AudienceDepartments'] | audienceDepartments |
| SpanTagsParsedFromLongDescription['AudienceDescription'] | audienceDescription |
| SpanTagsParsedFromLongDescription['AudienceEmployees'] | audienceEmployees |
| SpanTagsParsedFromLongDescription['AudienceStudents'] | audienceStudents |
| SpanTagsParsedFromLongDescription['BusinessContact'] | businessContact |
| SpanTagsParsedFromLongDescription['BusinessImpact'] | businessImpact |
| SpanTagsParsedFromLongDescription['BusinessOwner'] | businessOwner |
| SpanTagsParsedFromLongDescription['BusinessPriority']| businessPriority |
| SpanTagsParsedFromLongDescription['BusinessUnit'] | businessUnit |
| SpanTagsParsedFromLongDescription['ChargesOptionsFees'] | chargesOptionsFees |
| SpanTagsParsedFromLongDescription['Cost'] | cost |
| SpanTagsParsedFromLongDescription['EnablingServices'] | enablingServices |
| SpanTagsParsedFromLongDescription['EnhancingServices'] | enhancingServices |
| SpanTagsParsedFromLongDescription['EscalationContact'] | escalationContact |
| SpanTagsParsedFromLongDescription['LOSLearn'] | losLearn |
| SpanTagsParsedFromLongDescription['LOSOperate']| losOperate |
| SpanTagsParsedFromLongDescription['LOSResearch'] | losResearch |
| SpanTagsParsedFromLongDescription['LOSWork'] | losWork |
| SpanTagsParsedFromLongDescription['LongDescription'] | spanLongDescription |
| SpanTagsParsedFromLongDescription['RelatedServices'] | relatedServices |
| SpanTagsParsedFromLongDescription['RequestAccess'] | requestAccess |
| SpanTagsParsedFromLongDescription['SLA'] | sla |
| SpanTagsParsedFromLongDescription['SecurityRating'] | securityRating |
| SpanTagsParsedFromLongDescription['ServiceHours'] | serviceHours |
| SpanTagsParsedFromLongDescription['ServiceManager'] | serviceManager |
| SpanTagsParsedFromLongDescription['ServiceOwner'] | serviceOwner |
| SpanTagsParsedFromLongDescription['ServiceType'] | serviceType |
| SpanTagsParsedFromLongDescription['ShortDescription'] | spanShortDescription |
| SpanTagsParsedFromLongDescription['SupportAvailability'] | supportAvailability |
| SpanTagsParsedFromLongDescription['SynonymsList'] | synonymsList |
| SpanTagsParsedFromLongDescription['Training'] | training |
| SpanTagsParsedFromLongDescription['Value'] | value |
| Uri | **This field has been removed** |

### Run with Docker
```
$ docker build -t long_description .
$ docker run --rm -it -v "$PWD"/configuration.py:/usr/src/long-description/configuration.py:ro --name='long_description' long_description
$ docker cp long_description:/usr/src/long-description/services.json .
$ docker rm long_description
```
