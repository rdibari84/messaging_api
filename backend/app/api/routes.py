import logging
from typing import Optional

from fastapi import APIRouter, Depends
from datetime import datetime
from app.db.connection import get_repository
from app.db.repos import MessagesRepository, UsersRepository
from app.models.models import UserList, MessageCreateRequest, Message, MessageList, User, MessageCreate
from starlette.status import HTTP_201_CREATED

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/users", response_model=UserList)
async def get_all_users(
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> MessageList:
    logger.info(f"Fetching all users")
    users: UserList = await users_repo.get_all_users()
    return users


@router.get("/messages/{user_name}", response_model=MessageList)
async def get_all_messages(user_name: str,
                           users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
                           messaging_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
                           ) -> MessageList:
    logger.info(f"Fetching all messages for user_name: {user_name}")
    user: Optional[User] = await users_repo.get_user_by_name(user_name)

    if not user:
        logger.warning(f"There is no user with the user_name: {user_name}")
        return MessageList([])

    user_id = user.id
    logger.info(f"Fetching all messages for user_id: {user_id}")
    messages = await messaging_repo.get_messages_user(user_id=user_id)
    return messages


@router.post("/messages", response_model=Message, status_code=HTTP_201_CREATED)
async def create_new_messages(
        message_to_send: MessageCreateRequest,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
        messaging_repo: MessagesRepository = Depends(get_repository(MessagesRepository)),
):
    """
    :param messaging_repo:
    :param users_repo:
    :param message_to_send: MessageCreateRequest
    {
        sender_user_name: str
        recipient_user_name: str
        body: str
    }
    """
    logger.info("Sending a message")
    recipient_user: User = await users_repo.get_user_by_name(message_to_send.recipient_user_name)
    sender_user: User = await users_repo.get_user_by_name(message_to_send.sender_user_name)

    message_to_save = MessageCreate(
        **{
            "sender_id": sender_user.id,
            "recipient_id": recipient_user.id,
            "body": message_to_send.body.replace("'", "''"),
            "created_at": datetime.now(),
            "timestamp_sent": datetime.now(),
        }
    )
    await messaging_repo.create_messages(message_to_save)
