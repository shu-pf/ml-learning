"""アイテムサービスのビジネスロジック"""
from typing import List, Optional
from app.models.schemas import Item, ItemCreate, ItemUpdate
from app.db.session import MockDatabase


class ItemService:
    """アイテムサービスクラス"""
    
    def __init__(self, db: MockDatabase):
        self.db = db
    
    def create_item(self, item: ItemCreate) -> Item:
        """アイテムを作成"""
        item_data = item.model_dump()
        created = self.db.create_item(item_data)
        return Item(**created)
    
    def get_item(self, item_id: int) -> Optional[Item]:
        """アイテムを取得"""
        item = self.db.get_item(item_id)
        if item:
            return Item(**item)
        return None
    
    def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """アイテム一覧を取得"""
        items = self.db.get_items(skip=skip, limit=limit)
        return [Item(**item) for item in items]
    
    def update_item(self, item_id: int, item: ItemUpdate) -> Optional[Item]:
        """アイテムを更新"""
        update_data = item.model_dump(exclude_unset=True)
        updated = self.db.update_item(item_id, update_data)
        if updated:
            return Item(**updated)
        return None
    
    def delete_item(self, item_id: int) -> bool:
        """アイテムを削除"""
        return self.db.delete_item(item_id)

