"""チャットエンドポイント"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import Message, MessageCreate
from app.services.chat_service import ChatService
from app.dependencies import get_db
from app.db.session import MockDatabase

router = APIRouter()


@router.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
def create_message(
    message: MessageCreate,
    db: MockDatabase = Depends(get_db)
):
    """メッセージを作成"""
    service = ChatService(db)
    return service.create_message(message)


@router.get("/messages", response_model=List[Message])
def read_messages(
    skip: int = 0,
    limit: int = 100,
    db: MockDatabase = Depends(get_db)
):
    """メッセージ一覧を取得"""
    service = ChatService(db)
    return service.get_messages(skip=skip, limit=limit)


@router.get("/messages/{message_id}", response_model=Message)
def read_message(
    message_id: int,
    db: MockDatabase = Depends(get_db)
):
    """メッセージを取得"""
    service = ChatService(db)
    message = service.get_message(message_id)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    return message


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int,
    db: MockDatabase = Depends(get_db)
):
    """メッセージを削除"""
    service = ChatService(db)
    if not service.delete_message(message_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

