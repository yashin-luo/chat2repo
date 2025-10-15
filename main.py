"""
Chat2Repo 主应用
"""
import uuid
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    RepoChatRequest, 
    TechChatRequest, 
    ChatResponse, 
    ChatMessage,
    SessionHistory
)
from agents import RepoAgent, SearchAgent
from config import get_settings
import uvicorn


# 创建应用
app = FastAPI(
    title="Chat2Repo - Gitee Repository Chat Agent",
    description="与 Gitee 仓库对话，获取技术解决方案",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 会话存储（简单的内存存储，生产环境应使用数据库）
sessions: Dict[str, SessionHistory] = {}


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to Chat2Repo API",
        "version": "1.0.0",
        "endpoints": {
            "repo_chat": "/api/chat/repo",
            "tech_chat": "/api/chat/tech",
            "session": "/api/sessions/{session_id}"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.post("/api/chat/repo", response_model=ChatResponse)
async def chat_with_repo(request: RepoChatRequest):
    """与仓库对话
    
    与指定的 Gitee 仓库进行对话，Agent 会自动读取所需的文件内容
    """
    # 获取或创建会话
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = SessionHistory(
            session_id=session_id,
            messages=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    session = sessions[session_id]
    
    # 创建 Agent
    agent = RepoAgent()
    
    # 恢复对话历史
    for msg in session.messages:
        agent.add_message(msg.role, msg.content)
    
    try:
        # 执行对话
        result = agent.chat(
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            question=request.question,
            ref=request.ref
        )
        
        # 保存消息到会话
        session.messages.append(ChatMessage(role="user", content=request.question))
        session.messages.append(ChatMessage(role="assistant", content=result["answer"]))
        session.updated_at = datetime.now()
        
        # 构建响应
        return ChatResponse(
            answer=result["answer"],
            session_id=session_id,
            tool_calls=result.get("tool_calls", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")


@app.post("/api/chat/tech", response_model=ChatResponse)
async def chat_tech_question(request: TechChatRequest):
    """技术问答
    
    提出技术问题，Agent 会在 Gitee 上搜索相关的开源解决方案
    """
    # 获取或创建会话
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = SessionHistory(
            session_id=session_id,
            messages=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    session = sessions[session_id]
    
    # 创建 Agent
    agent = SearchAgent()
    
    # 恢复对话历史
    for msg in session.messages:
        agent.add_message(msg.role, msg.content)
    
    try:
        # 执行搜索
        result = agent.search(
            question=request.question,
            language=request.language
        )
        
        # 保存消息到会话
        session.messages.append(ChatMessage(role="user", content=request.question))
        session.messages.append(ChatMessage(role="assistant", content=result["answer"]))
        session.updated_at = datetime.now()
        
        # 构建响应
        return ChatResponse(
            answer=result["answer"],
            session_id=session_id,
            tool_calls=result.get("tool_calls", [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")


@app.get("/api/sessions/{session_id}", response_model=SessionHistory)
async def get_session(session_id: str):
    """获取会话历史"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return sessions[session_id]


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    del sessions[session_id]
    return {"message": "会话已删除", "session_id": session_id}


@app.get("/api/sessions")
async def list_sessions():
    """列出所有会话"""
    return {
        "sessions": [
            {
                "session_id": sid,
                "message_count": len(session.messages),
                "created_at": session.created_at,
                "updated_at": session.updated_at
            }
            for sid, session in sessions.items()
        ],
        "total": len(sessions)
    }


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
