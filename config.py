"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # OpenAI 兼容的 LLM API 配置
    openai_api_base: str = "https://api.openai.com/v1"
    openai_api_key: str
    openai_model: str = "gpt-4"
    
    # Gitee API 配置
    gitee_access_token: str
    gitee_api_base: str = "https://gitee.com/api/v5"
    
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Agent 配置
    max_iterations: int = 10
    timeout: int = 300
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
