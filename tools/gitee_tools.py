"""
Gitee 工具集，供 Agent 使用
"""
from typing import Dict, Any, List
from gitee_client import GiteeClient


class GiteeTools:
    """Gitee 工具集，提供给 Agent 使用的工具函数"""
    
    def __init__(self):
        self.client = GiteeClient()
    
    @staticmethod
    def get_tools_definition() -> List[Dict[str, Any]]:
        """获取工具定义（OpenAI Function Calling 格式）"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_repo_info",
                    "description": "获取 Gitee 仓库的基本信息，包括描述、星标数、Fork 数、语言等",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "仓库所有者用户名"
                            },
                            "repo": {
                                "type": "string",
                                "description": "仓库名称"
                            }
                        },
                        "required": ["owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_file_content",
                    "description": "读取仓库中指定文件的内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "仓库所有者用户名"
                            },
                            "repo": {
                                "type": "string",
                                "description": "仓库名称"
                            },
                            "path": {
                                "type": "string",
                                "description": "文件路径，例如 'src/main.py' 或 'README.md'"
                            },
                            "ref": {
                                "type": "string",
                                "description": "分支名称，默认为 master",
                                "default": "master"
                            }
                        },
                        "required": ["owner", "repo", "path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_directory",
                    "description": "列出仓库中指定目录的内容（文件和子目录）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "仓库所有者用户名"
                            },
                            "repo": {
                                "type": "string",
                                "description": "仓库名称"
                            },
                            "path": {
                                "type": "string",
                                "description": "目录路径，空字符串表示根目录",
                                "default": ""
                            },
                            "ref": {
                                "type": "string",
                                "description": "分支名称，默认为 master",
                                "default": "master"
                            }
                        },
                        "required": ["owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_readme",
                    "description": "获取仓库的 README 文件内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "仓库所有者用户名"
                            },
                            "repo": {
                                "type": "string",
                                "description": "仓库名称"
                            },
                            "ref": {
                                "type": "string",
                                "description": "分支名称，默认为 master",
                                "default": "master"
                            }
                        },
                        "required": ["owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_code",
                    "description": "在仓库中搜索代码片段或关键词",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词"
                            },
                            "owner": {
                                "type": "string",
                                "description": "仓库所有者用户名"
                            },
                            "repo": {
                                "type": "string",
                                "description": "仓库名称"
                            }
                        },
                        "required": ["query", "owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_commits",
                    "description": "获取仓库的提交历史记录",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "仓库所有者用户名"
                            },
                            "repo": {
                                "type": "string",
                                "description": "仓库名称"
                            },
                            "per_page": {
                                "type": "integer",
                                "description": "每页数量，默认 10",
                                "default": 10
                            }
                        },
                        "required": ["owner", "repo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_repositories",
                    "description": "在 Gitee 上搜索开源仓库",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词，例如 '分布式任务队列' 或 'machine learning'"
                            },
                            "language": {
                                "type": "string",
                                "description": "编程语言过滤，例如 'Python', 'Java', 'Go' 等"
                            },
                            "sort": {
                                "type": "string",
                                "description": "排序方式：best_match, stars, forks, updated",
                                "default": "best_match"
                            },
                            "per_page": {
                                "type": "integer",
                                "description": "每页数量，默认 10",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具函数
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            工具执行结果
        """
        if tool_name == "get_repo_info":
            return self.get_repo_info(**arguments)
        elif tool_name == "get_file_content":
            return self.get_file_content(**arguments)
        elif tool_name == "list_directory":
            return self.list_directory(**arguments)
        elif tool_name == "get_readme":
            return self.get_readme(**arguments)
        elif tool_name == "search_code":
            return self.search_code(**arguments)
        elif tool_name == "get_commits":
            return self.get_commits(**arguments)
        elif tool_name == "search_repositories":
            return self.search_repositories(**arguments)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """获取仓库信息"""
        result = self.client.get_repo_info(owner, repo)
        if result.get("error"):
            return result
        
        # 提取关键信息
        return {
            "name": result.get("name"),
            "full_name": result.get("full_name"),
            "description": result.get("description"),
            "language": result.get("language"),
            "stars_count": result.get("stars_count", 0),
            "forks_count": result.get("forks_count", 0),
            "watchers_count": result.get("watchers_count", 0),
            "open_issues_count": result.get("open_issues_count", 0),
            "default_branch": result.get("default_branch", "master"),
            "created_at": result.get("created_at"),
            "updated_at": result.get("updated_at"),
            "html_url": result.get("html_url")
        }
    
    def get_file_content(self, owner: str, repo: str, path: str, ref: str = "master") -> Dict[str, Any]:
        """读取文件内容"""
        result = self.client.get_file_content(owner, repo, path, ref)
        if result.get("error"):
            return result
        
        return {
            "path": result.get("path"),
            "name": result.get("name"),
            "size": result.get("size"),
            "type": result.get("type"),
            "content": result.get("decoded_content", ""),
            "sha": result.get("sha"),
            "url": result.get("url")
        }
    
    def list_directory(self, owner: str, repo: str, path: str = "", ref: str = "master") -> Dict[str, Any]:
        """列出目录内容"""
        result = self.client.list_directory(owner, repo, path, ref)
        
        items = []
        for item in result:
            items.append({
                "name": item.get("name"),
                "path": item.get("path"),
                "type": item.get("type"),
                "size": item.get("size"),
                "sha": item.get("sha")
            })
        
        return {
            "path": path or "/",
            "items": items,
            "count": len(items)
        }
    
    def get_readme(self, owner: str, repo: str, ref: str = "master") -> Dict[str, Any]:
        """获取 README"""
        result = self.client.get_repo_readme(owner, repo, ref)
        if result.get("error"):
            return result
        
        return {
            "name": result.get("name"),
            "path": result.get("path"),
            "content": result.get("decoded_content", ""),
            "html_url": result.get("html_url")
        }
    
    def search_code(self, query: str, owner: str, repo: str) -> Dict[str, Any]:
        """搜索代码"""
        result = self.client.search_code(query, owner, repo)
        if result.get("error"):
            return result
        
        items = []
        for item in result.get("items", [])[:5]:  # 限制返回前 5 个结果
            items.append({
                "name": item.get("name"),
                "path": item.get("path"),
                "repository": item.get("repository", {}).get("full_name"),
                "html_url": item.get("html_url")
            })
        
        return {
            "total_count": result.get("total_count", 0),
            "items": items
        }
    
    def get_commits(self, owner: str, repo: str, per_page: int = 10) -> Dict[str, Any]:
        """获取提交历史"""
        result = self.client.get_repo_commits(owner, repo, per_page=per_page)
        
        commits = []
        for commit in result[:per_page]:
            commit_data = commit.get("commit", {})
            commits.append({
                "sha": commit.get("sha"),
                "message": commit_data.get("message"),
                "author": commit_data.get("author", {}).get("name"),
                "date": commit_data.get("author", {}).get("date"),
                "html_url": commit.get("html_url")
            })
        
        return {
            "commits": commits,
            "count": len(commits)
        }
    
    def search_repositories(self, query: str, language: str = None, 
                          sort: str = "best_match", per_page: int = 10) -> Dict[str, Any]:
        """搜索仓库"""
        result = self.client.search_repositories(query, per_page=per_page, language=language, sort=sort)
        if result.get("error"):
            return result
        
        repos = []
        for repo in result.get("items", [])[:per_page]:
            repos.append({
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars_count": repo.get("stars_count", 0),
                "forks_count": repo.get("forks_count", 0),
                "html_url": repo.get("html_url"),
                "updated_at": repo.get("updated_at")
            })
        
        return {
            "total_count": result.get("total_count", 0),
            "repositories": repos,
            "count": len(repos)
        }
