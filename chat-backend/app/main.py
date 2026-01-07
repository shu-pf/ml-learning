"""FastAPIアプリケーションのエントリーポイント"""
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# APIルーターを登録
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def read_root():
    """ルートエンドポイント"""
    return {
        "message": "Welcome to Chat Backend API",
        "version": settings.app_version,
        "docs": "/docs"
    }

