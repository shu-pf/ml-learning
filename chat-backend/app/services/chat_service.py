"""チャットサービスのビジネスロジック"""
from typing import List, Optional
from app.models.schemas import Message, MessageCreate
from app.db.session import MockDatabase


class ChatService:
    """チャットサービスクラス"""
    
    def __init__(self, db: MockDatabase):
        self.db = db
    
    def create_message(self, message: MessageCreate) -> Message:
        """メッセージを作成"""
        message_data = message.model_dump()
        created = self.db.create_message(message_data)
        return Message(**created)
    
    def get_message(self, message_id: int) -> Optional[Message]:
        """メッセージを取得"""
        message = self.db.get_message(message_id)
        if message:
            return Message(**message)
        return None
    
    def get_messages(self, skip: int = 0, limit: int = 100) -> List[Message]:
        """メッセージ一覧を取得"""
        messages = self.db.get_messages(skip=skip, limit=limit)
        return [Message(**message) for message in messages]
    
    def delete_message(self, message_id: int) -> bool:
        """メッセージを削除"""
        return self.db.delete_message(message_id)

