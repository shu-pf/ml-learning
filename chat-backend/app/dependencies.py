"""依存性注入"""
from app.db.session import mock_db


def get_db():
    """データベースセッションを取得（モック）"""
    try:
        yield mock_db
    finally:
        pass  # モックなのでクリーンアップ不要

