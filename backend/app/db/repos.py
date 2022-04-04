from databases import Database
from app.models.models import UserList, MessageList, MessageCreate, User
from typing import Optional


class BaseRepository:
    def __init__(self, db: Database) -> None:
        self.db = db


class UsersRepository(BaseRepository):

    async def get_all_users(self) -> Optional[UserList]:
        USERS_QUERY = """
        SELECT * from messaging.users
        """
        users = await self.db.fetch_all(query=USERS_QUERY)
        return UserList(users)

    async def get_user_by_name(self, user_name: str) -> Optional[User]:
        USERS_QUERY = """
        SELECT * from messaging.users 
        WHERE user_name = :user_name
        """
        user = await self.db.fetch_one(query=USERS_QUERY, values={"user_name": user_name})
        if not user:
            return None
        return User(**user)


class MessagesRepository(BaseRepository):

    async def get_messages_user(self, user_id: id) -> MessageList:
        GET_MESSAGES_QUERY = """
        SELECT * from messaging.messages 
        WHERE created_at >=  current_date - interval '30 days'
        AND (sender_id = :sender_id 
        OR recipient_id = :recipient_id);
        """
        messages = await self.db.fetch_all(query=GET_MESSAGES_QUERY,
                                           values={"sender_id": user_id, "recipient_id": user_id})
        return MessageList(messages)

    async def create_messages(self, message: MessageCreate) -> None:
        INSERT_MESSAGES_QUERY = """
        INSERT INTO messaging.messages(
        sender_id,
        recipient_id,
        body,
        created_at,
        timestamp_sent
        ) VALUES (:sender_id, :recipient_id, :body, :created_at, :timestamp_sent)
        """
        await self.db.fetch_one(query=INSERT_MESSAGES_QUERY, values=message.dict())
