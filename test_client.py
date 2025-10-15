"""
Chat2Repo 测试客户端
用于测试 API 功能
"""
import os
import sys
import requests
import json
from typing import Optional


class Chat2RepoTestClient:
    """测试客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def test_health(self):
        """测试健康检查"""
        print("\n=== 测试健康检查 ===")
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"错误: {e}")
            return False
    
    def test_repo_chat(self, owner: str, repo: str, question: str, session_id: Optional[str] = None):
        """测试仓库对话"""
        print(f"\n=== 测试仓库对话 ===")
        print(f"仓库: {owner}/{repo}")
        print(f"问题: {question}")
        
        try:
            data = {
                "repo_owner": owner,
                "repo_name": repo,
                "question": question
            }
            if session_id:
                data["session_id"] = session_id
            
            response = requests.post(
                f"{self.base_url}/api/chat/repo",
                json=data,
                timeout=120
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n会话ID: {result['session_id']}")
                print(f"\n答案:\n{result['answer']}")
                
                if result.get('tool_calls'):
                    print(f"\n工具调用次数: {len(result['tool_calls'])}")
                    print("工具调用记录:")
                    for i, call in enumerate(result['tool_calls'], 1):
                        print(f"  {i}. {call['function']}({json.dumps(call['arguments'], ensure_ascii=False)})")
                
                return True, result['session_id']
            else:
                print(f"错误: {response.text}")
                return False, None
                
        except Exception as e:
            print(f"错误: {e}")
            return False, None
    
    def test_tech_search(self, question: str, language: Optional[str] = None, session_id: Optional[str] = None):
        """测试技术搜索"""
        print(f"\n=== 测试技术搜索 ===")
        print(f"问题: {question}")
        if language:
            print(f"语言过滤: {language}")
        
        try:
            data = {
                "question": question
            }
            if language:
                data["language"] = language
            if session_id:
                data["session_id"] = session_id
            
            response = requests.post(
                f"{self.base_url}/api/chat/tech",
                json=data,
                timeout=120
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n会话ID: {result['session_id']}")
                print(f"\n答案:\n{result['answer']}")
                
                if result.get('tool_calls'):
                    print(f"\n工具调用次数: {len(result['tool_calls'])}")
                    print("工具调用记录:")
                    for i, call in enumerate(result['tool_calls'], 1):
                        print(f"  {i}. {call['function']}({json.dumps(call['arguments'], ensure_ascii=False)})")
                
                return True, result['session_id']
            else:
                print(f"错误: {response.text}")
                return False, None
                
        except Exception as e:
            print(f"错误: {e}")
            return False, None
    
    def test_get_session(self, session_id: str):
        """测试获取会话历史"""
        print(f"\n=== 测试获取会话历史 ===")
        print(f"会话ID: {session_id}")
        
        try:
            response = requests.get(f"{self.base_url}/api/sessions/{session_id}")
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n会话创建时间: {result['created_at']}")
                print(f"会话更新时间: {result['updated_at']}")
                print(f"消息数量: {len(result['messages'])}")
                
                print("\n对话历史:")
                for i, msg in enumerate(result['messages'], 1):
                    print(f"  {i}. [{msg['role']}] {msg['content'][:100]}...")
                
                return True
            else:
                print(f"错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"错误: {e}")
            return False


def main():
    """主函数"""
    print("Chat2Repo 测试客户端")
    print("=" * 50)
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("\n警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请确保 .env 文件已正确配置")
    
    if not os.getenv("GITEE_ACCESS_TOKEN"):
        print("\n警告: 未设置 GITEE_ACCESS_TOKEN 环境变量")
        print("请确保 .env 文件已正确配置")
    
    # 创建测试客户端
    client = Chat2RepoTestClient()
    
    # 测试健康检查
    if not client.test_health():
        print("\n服务未启动或无法访问，请先启动服务：")
        print("  python main.py")
        sys.exit(1)
    
    # 测试 1: 仓库对话
    success, session_id = client.test_repo_chat(
        owner="dromara",
        repo="hutool",
        question="这个项目是做什么的？请简要介绍一下。"
    )
    
    if success and session_id:
        # 测试持续对话
        client.test_repo_chat(
            owner="dromara",
            repo="hutool",
            question="它有哪些主要功能模块？",
            session_id=session_id
        )
        
        # 测试获取会话历史
        client.test_get_session(session_id)
    
    # 测试 2: 技术搜索
    client.test_tech_search(
        question="推荐一些 Java 的工具类库",
        language="Java"
    )
    
    print("\n" + "=" * 50)
    print("测试完成！")


if __name__ == "__main__":
    main()
