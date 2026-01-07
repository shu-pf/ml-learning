"""アイテムエンドポイント"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import Item, ItemCreate, ItemUpdate
from app.services.item_service import ItemService
from app.dependencies import get_db
from app.db.session import MockDatabase

router = APIRouter()


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: MockDatabase = Depends(get_db)
):
    """アイテムを作成"""
    service = ItemService(db)
    return service.create_item(item)


@router.get("/", response_model=List[Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: MockDatabase = Depends(get_db)
):
    """アイテム一覧を取得"""
    service = ItemService(db)
    return service.get_items(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=Item)
def read_item(
    item_id: int,
    db: MockDatabase = Depends(get_db)
):
    """アイテムを取得"""
    service = ItemService(db)
    item = service.get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: MockDatabase = Depends(get_db)
):
    """アイテムを更新"""
    service = ItemService(db)
    updated_item = service.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: MockDatabase = Depends(get_db)
):
    """アイテムを削除"""
    service = ItemService(db)
    if not service.delete_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

