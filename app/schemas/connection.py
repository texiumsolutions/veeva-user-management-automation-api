from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime


class ConnectionType(str, Enum):
    servicenow = "servicenow"
    veeva_vault = "veeva_vault"
    sap_leanix = "sap_leanix"
    workday = "workday"
    successfactors = "successfactors"
    cornerstone = "cornerstone"


class AuthType(str, Enum):
    basic = "basic"
    oauth2 = "oauth2"
    api_key = "api_key"


class Environment(str, Enum):
    production = "production"
    staging = "staging"
    development = "development"


class Credentials(BaseModel):

    authType: AuthType

    username: Optional[str] = None
    password: Optional[str] = None

    apiToken: Optional[str] = None

    clientId: Optional[str] = None
    clientSecret: Optional[str] = None
    tokenUrl: Optional[str] = None
    grantType: Optional[str] = None


class Config(BaseModel):

    instanceUrl: Optional[str] = None
    baseUrl: Optional[str] = None
    tenant: Optional[str] = None
    tenantName: Optional[str] = None
    workspace: Optional[str] = None
    region: Optional[str] = None
    apiVersion: Optional[str] = None
    companyId: Optional[str] = None


class ConnectionCreateRequest(BaseModel):

    connectionName: str
    displayName: str
    description: Optional[str] = None

    type: ConnectionType
    environment: Optional[Environment] = Environment.production

    config: Config
    credentials: Credentials


class ConnectionUpdateRequest(BaseModel):

    displayName: Optional[str] = None
    description: Optional[str] = None
    environment: Optional[Environment] = None

    config: Optional[Config] = None
    credentials: Optional[Credentials] = None


class ConnectionResponse(BaseModel):

    connection_id: str = Field(..., alias="_id")

    connectionName: str
    displayName: str
    description: Optional[str]

    type: str
    environment: str

    config: Optional[Dict]
    credentials: Optional[Dict]

    created_at: datetime
    updated_at: datetime


class ConnectionListResponse(BaseModel):

    status: str
    message: str
    total: int
    data: List[Dict]


class ConnectionDetailResponse(BaseModel):

    status: str
    message: str
    data: Dict


class ConnectionActionResponse(BaseModel):

    status: str
    message: str
    connection_id: Optional[str] = None