#!/usr/bin/env python3
"""
Chat2Repo 命令行工具
"""
import sys
import argparse
import requests
import json
from typing import Optional


class Chat2RepoCLI:
    """CLI 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id: Optional[str] = None
    
    def chat_repo(self, owner: str, repo: str, question: str, ref: str = "master"):
        """仓库对话"""
        data = {
            "repo_owner": owner,
            "repo_name": repo,
            "question": question,
            "ref": ref
        }
        
        if self.session_id:
            data["session_id"] = self.session_id
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/repo",
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            
            self.session_id = result["session_id"]
            
            print(f"\n{'='*60}")
            print(f"仓库: {owner}/{repo}")
            print(f"问题: {question}")
            print(f"{'='*60}\n")
            print(result["answer"])
            
            if result.get("tool_calls"):
                print(f"\n{'='*60}")
                print(f"工具调用 ({len(result['tool_calls'])} 次):")
                for i, call in enumerate(result["tool_calls"], 1):
                    print(f"  {i}. {call['function']}")
            
            print(f"\n{'='*60}")
            print(f"会话ID: {self.session_id}")
            print(f"{'='*60}\n")
            
        except requests.exceptions.RequestException as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    
    def search_tech(self, question: str, language: Optional[str] = None):
        """技术搜索"""
        data = {
            "question": question
        }
        
        if language:
            data["language"] = language
        
        if self.session_id:
            data["session_id"] = self.session_id
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat/tech",
                json=data,
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            
            self.session_id = result["session_id"]
            
            print(f"\n{'='*60}")
            print(f"技术问题: {question}")
            if language:
                print(f"语言过滤: {language}")
            print(f"{'='*60}\n")
            print(result["answer"])
            
            if result.get("tool_calls"):
                print(f"\n{'='*60}")
                print(f"工具调用 ({len(result['tool_calls'])} 次):")
                for i, call in enumerate(result["tool_calls"], 1):
                    print(f"  {i}. {call['function']}")
            
            print(f"\n{'='*60}")
            print(f"会话ID: {self.session_id}")
            print(f"{'='*60}\n")
            
        except requests.exceptions.RequestException as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    
    def show_session(self, session_id: Optional[str] = None):
        """显示会话历史"""
        sid = session_id or self.session_id
        
        if not sid:
            print("错误: 请指定会话ID", file=sys.stderr)
            sys.exit(1)
        
        try:
            response = requests.get(f"{self.base_url}/api/sessions/{sid}")
            response.raise_for_status()
            result = response.json()
            
            print(f"\n{'='*60}")
            print(f"会话ID: {result['session_id']}")
            print(f"创建时间: {result['created_at']}")
            print(f"更新时间: {result['updated_at']}")
            print(f"消息数量: {len(result['messages'])}")
            print(f"{'='*60}\n")
            
            for i, msg in enumerate(result["messages"], 1):
                role_display = "🧑 用户" if msg["role"] == "user" else "🤖 助手"
                print(f"{role_display}:")
                print(msg["content"])
                print()
            
        except requests.exceptions.RequestException as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)
    
    def interactive_mode(self):
        """交互式模式"""
        print("Chat2Repo 交互式命令行")
        print("=" * 60)
        print("命令:")
        print("  repo <owner> <name> - 切换到仓库对话模式")
        print("  tech                - 切换到技术搜索模式")
        print("  history             - 查看当前会话历史")
        print("  clear               - 清空当前会话")
        print("  quit / exit         - 退出")
        print("=" * 60)
        
        mode = None
        repo_owner = None
        repo_name = None
        
        while True:
            try:
                if mode == "repo":
                    prompt = f"[仓库: {repo_owner}/{repo_name}] > "
                elif mode == "tech":
                    prompt = "[技术搜索] > "
                else:
                    prompt = "[命令] > "
                
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["quit", "exit"]:
                    print("再见！")
                    break
                
                if user_input.lower() == "clear":
                    self.session_id = None
                    print("会话已清空")
                    continue
                
                if user_input.lower() == "history":
                    if self.session_id:
                        self.show_session()
                    else:
                        print("当前没有会话")
                    continue
                
                if user_input.startswith("repo "):
                    parts = user_input.split()
                    if len(parts) >= 3:
                        mode = "repo"
                        repo_owner = parts[1]
                        repo_name = parts[2]
                        print(f"已切换到仓库模式: {repo_owner}/{repo_name}")
                    else:
                        print("用法: repo <owner> <name>")
                    continue
                
                if user_input.lower() == "tech":
                    mode = "tech"
                    print("已切换到技术搜索模式")
                    continue
                
                # 处理用户问题
                if mode == "repo":
                    if repo_owner and repo_name:
                        self.chat_repo(repo_owner, repo_name, user_input)
                    else:
                        print("请先使用 'repo <owner> <name>' 命令指定仓库")
                elif mode == "tech":
                    self.search_tech(user_input)
                else:
                    print("请先选择模式：")
                    print("  repo <owner> <name> - 仓库对话")
                    print("  tech                - 技术搜索")
                
            except KeyboardInterrupt:
                print("\n\n使用 'quit' 或 'exit' 退出")
            except EOFError:
                print("\n再见！")
                break


def main():
    parser = argparse.ArgumentParser(
        description="Chat2Repo - 与 Gitee 仓库对话的命令行工具"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API 服务地址 (默认: http://localhost:8000)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # repo 命令
    repo_parser = subparsers.add_parser("repo", help="仓库对话")
    repo_parser.add_argument("owner", help="仓库所有者")
    repo_parser.add_argument("name", help="仓库名称")
    repo_parser.add_argument("question", help="问题")
    repo_parser.add_argument("--ref", default="master", help="分支名称")
    
    # tech 命令
    tech_parser = subparsers.add_parser("tech", help="技术搜索")
    tech_parser.add_argument("question", help="技术问题")
    tech_parser.add_argument("--language", help="编程语言过滤")
    
    # session 命令
    session_parser = subparsers.add_parser("session", help="查看会话历史")
    session_parser.add_argument("session_id", help="会话ID")
    
    # interactive 命令
    subparsers.add_parser("interactive", help="交互式模式")
    
    args = parser.parse_args()
    
    cli = Chat2RepoCLI(base_url=args.url)
    
    if args.command == "repo":
        cli.chat_repo(args.owner, args.name, args.question, args.ref)
    elif args.command == "tech":
        cli.search_tech(args.question, args.language)
    elif args.command == "session":
        cli.show_session(args.session_id)
    elif args.command == "interactive":
        cli.interactive_mode()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
