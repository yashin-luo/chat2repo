"""
数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class RepoChatRequest(BaseModel):
    """仓库对话请求"""
    repo_owner: str = Field(..., description="仓库所有者")
    repo_name: str = Field(..., description="仓库名称")
    question: str = Field(..., description="用户问题")
    session_id: Optional[str] = Field(None, description="会话 ID，用于保持上下文")
    ref: str = Field("master", description="分支名称")


class TechChatRequest(BaseModel):
    """技术问答请求"""
    question: str = Field(..., description="技术问题")
    session_id: Optional[str] = Field(None, description="会话 ID")
    language: Optional[str] = Field(None, description="编程语言过滤")


class ChatResponse(BaseModel):
    """聊天响应"""
    answer: str = Field(..., description="回答内容")
    session_id: str = Field(..., description="会话 ID")
    sources: Optional[List[Dict[str, Any]]] = Field(None, description="引用来源")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(None, description="工具调用记录")


class SessionHistory(BaseModel):
    """会话历史"""
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime
