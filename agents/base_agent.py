"""
Agent 基类
"""
import json
from typing import List, Dict, Any, Optional
from llm_client import LLMClient
from tools import GiteeTools
from config import get_settings


class BaseAgent:
    """Agent 基类，提供通用的 Agent 功能"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.tools = GiteeTools()
        self.settings = get_settings()
        self.conversation_history: List[Dict[str, str]] = []
        self.tool_calls_log: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str):
        """添加消息到对话历史"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        self.tool_calls_log = []
    
    def run(self, user_input: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """运行 Agent
        
        Args:
            user_input: 用户输入
            system_prompt: 系统提示词
            
        Returns:
            Agent 响应结果
        """
        # 构建消息列表
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 添加对话历史
        messages.extend(self.conversation_history)
        
        # 添加用户输入
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 运行 Agent 循环
        iterations = 0
        max_iterations = self.settings.max_iterations
        
        while iterations < max_iterations:
            iterations += 1
            
            # 调用 LLM
            response = self.llm.chat(
                messages=messages,
                tools=self.tools.get_tools_definition(),
                tool_choice="auto"
            )
            
            if not response.get("success"):
                return {
                    "success": False,
                    "error": response.get("error"),
                    "tool_calls": self.tool_calls_log
                }
            
            assistant_message = response["response"].choices[0].message
            
            # 检查是否需要调用工具
            if assistant_message.tool_calls:
                # 添加助手消息
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # 执行工具调用
                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # 记录工具调用
                    self.tool_calls_log.append({
                        "function": function_name,
                        "arguments": function_args
                    })
                    
                    # 执行工具
                    tool_response = self.tools.execute_tool(function_name, function_args)
                    
                    # 添加工具响应
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_response, ensure_ascii=False),
                        "tool_call_id": tool_call.id
                    })
                
                # 继续下一轮迭代
                continue
            else:
                # 没有工具调用，返回最终答案
                final_answer = assistant_message.content or ""
                
                # 保存对话历史
                self.add_message("user", user_input)
                self.add_message("assistant", final_answer)
                
                return {
                    "success": True,
                    "answer": final_answer,
                    "tool_calls": self.tool_calls_log,
                    "iterations": iterations
                }
        
        # 达到最大迭代次数
        return {
            "success": False,
            "error": f"达到最大迭代次数 {max_iterations}",
            "tool_calls": self.tool_calls_log
        }
