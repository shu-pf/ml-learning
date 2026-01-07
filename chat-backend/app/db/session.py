"""モックデータベースセッション"""
from typing import Dict, List, Any, Optional
from datetime import datetime


class MockDatabase:
    """モックデータベースクラス"""
    
    def __init__(self):
        self._items: Dict[int, Dict[str, Any]] = {}
        self._messages: Dict[int, Dict[str, Any]] = {}
        self._item_counter = 0
        self._message_counter = 0
    
    # Items関連メソッド
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """アイテムを作成"""
        self._item_counter += 1
        item = {
            "id": self._item_counter,
            **item_data,
        }
        self._items[self._item_counter] = item
        return item
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """アイテムを取得"""
        return self._items.get(item_id)
    
    def get_items(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """アイテム一覧を取得"""
        items = list(self._items.values())
        return items[skip:skip + limit]
    
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """アイテムを更新"""
        if item_id not in self._items:
            return None
        self._items[item_id].update(item_data)
        return self._items[item_id]
    
    def delete_item(self, item_id: int) -> bool:
        """アイテムを削除"""
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
    
    # Messages関連メソッド
    def create_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """メッセージを作成"""
        self._message_counter += 1
        message = {
            "id": self._message_counter,
            "created_at": datetime.now().isoformat(),
            **message_data,
        }
        self._messages[self._message_counter] = message
        return message
    
    def get_message(self, message_id: int) -> Optional[Dict[str, Any]]:
        """メッセージを取得"""
        return self._messages.get(message_id)
    
    def get_messages(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """メッセージ一覧を取得"""
        messages = list(self._messages.values())
        return messages[skip:skip + limit]
    
    def delete_message(self, message_id: int) -> bool:
        """メッセージを削除"""
        if message_id in self._messages:
            del self._messages[message_id]
            return True
        return False


# グローバルなモックDBインスタンス
mock_db = MockDatabase()

