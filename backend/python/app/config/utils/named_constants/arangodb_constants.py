from enum import Enum


class AircraftNames(Enum):
    # Boeing Aircraft
    BOEING_737 = "Boeing 737"
    BOEING_737_700 = "Boeing 737-700"
    BOEING_737_800 = "Boeing 737-800"
    BOEING_737_900 = "Boeing 737-900"
    BOEING_737_MAX = "Boeing 737 MAX"
    BOEING_747 = "Boeing 747"
    BOEING_747_8 = "Boeing 747-8"
    BOEING_757 = "Boeing 757"
    BOEING_767 = "Boeing 767"
    BOEING_777 = "Boeing 777"
    BOEING_777_200 = "Boeing 777-200"
    BOEING_777_300 = "Boeing 777-300"
    BOEING_777X = "Boeing 777X"
    BOEING_787 = "Boeing 787"
    BOEING_787_8 = "Boeing 787-8"
    BOEING_787_9 = "Boeing 787-9"
    BOEING_787_10 = "Boeing 787-10"
    
    # Airbus Aircraft
    AIRBUS_A220 = "Airbus A220"
    AIRBUS_A300 = "Airbus A300"
    AIRBUS_A310 = "Airbus A310"
    AIRBUS_A318 = "Airbus A318"
    AIRBUS_A319 = "Airbus A319"
    AIRBUS_A320 = "Airbus A320"
    AIRBUS_A321 = "Airbus A321"
    AIRBUS_A330 = "Airbus A330"
    AIRBUS_A330_200 = "Airbus A330-200"
    AIRBUS_A330_300 = "Airbus A330-300"
    AIRBUS_A340 = "Airbus A340"
    AIRBUS_A350 = "Airbus A350"
    AIRBUS_A350_900 = "Airbus A350-900"
    AIRBUS_A350_1000 = "Airbus A350-1000"
    AIRBUS_A380 = "Airbus A380"
    
    # Embraer Aircraft
    EMBRAER_E170 = "Embraer E170"
    EMBRAER_E175 = "Embraer E175"
    EMBRAER_E190 = "Embraer E190"
    EMBRAER_E195 = "Embraer E195"
    
    # Bombardier Aircraft
    BOMBARDIER_CRJ = "Bombardier CRJ"
    BOMBARDIER_Q400 = "Bombardier Q400"
    
    # Other Aircraft
    ATR_42 = "ATR 42"
    ATR_72 = "ATR 72"
    
    # Generic/Unknown
    UNKNOWN = "Unknown Aircraft"


class Connectors(Enum):
    GOOGLE_DRIVE = "DRIVE"
    GOOGLE_MAIL = "GMAIL"
    GOOGLE_CALENDAR = "CALENDAR"

class AppGroups(Enum):
    GOOGLE_WORKSPACE = "Google Workspace"

class RecordTypes(Enum):
    FILE = "FILE"
    ATTACHMENT = "ATTACHMENT"
    LINK = "LINK"
    MAIL = "MAIL"
    DRIVE = "DRIVE"


class RecordRelations(Enum):
    PARENT_CHILD = "PARENT_CHILD"
    SIBLING = "SIBLING"
    ATTACHMENT = "ATTACHMENT"


class OriginTypes(Enum):
    CONNECTOR = "CONNECTOR"
    UPLOAD = "UPLOAD"


class EventTypes(Enum):
    NEW_RECORD = "newRecord"
    UPDATE_RECORD = "updateRecord"
    DELETE_RECORD = "deleteRecord"
    REINDEX_RECORD = "reindexRecord"
    REINDEX_FAILED = "reindexFailed"


class CollectionNames(Enum):
    # Records and Record relations
    RECORDS = "records"
    RECORD_RELATIONS = "recordRelations"

    # Knowledge base
    KNOWLEDGE_BASE = "knowledgeBase"
    IS_OF_TYPE = "isOfType"
    BELONGS_TO_KNOWLEDGE_BASE = "belongsToKnowledgeBase"
    PERMISSIONS_TO_KNOWLEDGE_BASE = "permissionsToKnowledgeBase"

    # Drive related
    DRIVES = "drives"
    USER_DRIVE_RELATION = "userDriveRelation"

    # Record types
    FILES = "files"
    ATTACHMENTS = "attachments"
    LINKS = "links"
    MAILS = "mails"

    # Users and groups
    PEOPLE = "people"
    USERS = "users"
    GROUPS = "groups"
    ORGS = "organizations"
    ANYONE = "anyone"
    BELONGS_TO = "belongsTo"

    # Aircraft
    AIRCRAFT = "aircraft"
    BELONGS_TO_AIRCRAFT = "belongsToAircraft"
    CATEGORIES = "categories"
    BELONGS_TO_CATEGORY = "belongsToCategory"
    LANGUAGES = "languages"
    BELONGS_TO_LANGUAGE = "belongsToLanguage"
    TOPICS = "topics"
    BELONGS_TO_TOPIC = "belongsToTopic"
    SUBCATEGORIES1 = "subcategories1"
    SUBCATEGORIES2 = "subcategories2"
    SUBCATEGORIES3 = "subcategories3"
    INTER_CATEGORY_RELATIONS = "interCategoryRelations"

    # Permissions
    PERMISSIONS = "permissions"

    # Other
    CHANNEL_HISTORY = "channelHistory"
    PAGE_TOKENS = "pageTokens"

    # Graphs
    FILE_ACCESS_GRAPH = "fileAccessGraph"

    APPS = "apps"
    ORG_APP_RELATION = "orgAppRelation"
    USER_APP_RELATION = "userAppRelation"
    ORG_AIRCRAFT_RELATION = "orgAircraftRelation"

    BLOCKS = "blocks"


class QdrantCollectionNames(Enum):
    RECORDS = "records"


class ExtensionTypes(Enum):
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    PPTX = "pptx"
    PPT = "ppt"
    XLSX = "xlsx"
    XLS = "xls"
    CSV = "csv"
    TXT = "txt"
    MD = "md"
    MDX = "mdx"
    HTML = "html"


class MimeTypes(Enum):
    PDF = "application/pdf"
    GMAIL = "text/gmail_content"
    GOOGLE_SLIDES = "application/vnd.google-apps.presentation"
    GOOGLE_DOCS = "application/vnd.google-apps.document"
    GOOGLE_SHEETS = "application/vnd.google-apps.spreadsheet"
    GOOGLE_DRIVE_FOLDER = "application/vnd.google-apps.folder"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    DOC = "application/msword"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    PPT = "application/vnd.ms-powerpoint"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    XLS = "application/vnd.ms-excel"
    CSV = "text/csv"


class ProgressStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    PAUSED = "PAUSED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    FILE_TYPE_NOT_SUPPORTED = "FILE_TYPE_NOT_SUPPORTED"
    AUTO_INDEX_OFF = "AUTO_INDEX_OFF"


class AccountType(Enum):
    INDIVIDUAL = "individual"
    ENTERPRISE = "enterprise"
    BUSINESS = "business"
    ADMIN = "admin"
