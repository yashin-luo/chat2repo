"""
LLM 客户端，支持 OpenAI 标准 API
"""
from typing import List, Dict, Any, Optional
from openai import OpenAI
from config import get_settings


class LLMClient:
    """LLM 客户端，支持 OpenAI 标准 API 格式"""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base
        )
        self.model = settings.openai_model
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.7,
             max_tokens: Optional[int] = None,
             tools: Optional[List[Dict[str, Any]]] = None,
             tool_choice: Optional[str] = None) -> Dict[str, Any]:
        """发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数
            tools: 可用工具列表（Function Calling）
            tool_choice: 工具选择策略
            
        Returns:
            API 响应
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        if tools:
            kwargs["tools"] = tools
            if tool_choice:
                kwargs["tool_choice"] = tool_choice
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return {
                "success": True,
                "response": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def stream_chat(self, messages: List[Dict[str, str]], 
                    temperature: float = 0.7,
                    max_tokens: Optional[int] = None):
        """流式聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数
            
        Yields:
            响应流
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        try:
            stream = self.client.chat.completions.create(**kwargs)
            for chunk in stream:
                yield chunk
        except Exception as e:
            yield {"error": str(e)}
