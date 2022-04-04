from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pydantic_collections import BaseCollectionModel

from pydantic.dataclasses import dataclass


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    created_at: datetime


class IDModelMixin(BaseModel):
    id: int


class User(IDModelMixin, CoreModel):
    first_name: Optional[str]
    last_name: Optional[str]
    user_name: str
    email: str
    mfa: bool
    modified_at: Optional[str]


class Message(IDModelMixin, CoreModel):
    sender_id: int
    recipient_id: int
    body: str
    timestamp_sent: datetime
    timestamp_delivered: Optional[datetime]
    timestamp_read: Optional[datetime]


class MessageList(BaseCollectionModel[Message]):
    pass


class MessageCreateRequest(BaseModel):
    sender_user_name: str
    recipient_user_name: str
    body: str


class MessageCreate(CoreModel):
    sender_id: int
    recipient_id: int
    body: str
    timestamp_sent: datetime


class UserList(BaseCollectionModel[User]):
    pass


class MessagePublic(IDModelMixin, CoreModel):
    pass
