from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    app_name: str = "Chat Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API設定
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

