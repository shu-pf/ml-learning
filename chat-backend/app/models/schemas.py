from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    """アイテムのベーススキーマ"""
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    """アイテム作成用スキーマ"""
    pass


class ItemUpdate(BaseModel):
    """アイテム更新用スキーマ"""
    name: Optional[str] = None
    description: Optional[str] = None


class Item(ItemBase):
    """アイテムレスポンス用スキーマ"""
    id: int
    
    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    """メッセージのベーススキーマ"""
    content: str
    user_id: Optional[int] = None


class MessageCreate(MessageBase):
    """メッセージ作成用スキーマ"""
    pass


class Message(MessageBase):
    """メッセージレスポンス用スキーマ"""
    id: int
    created_at: str
    
    class Config:
        from_attributes = True

