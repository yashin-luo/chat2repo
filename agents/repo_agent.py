"""
仓库问答 Agent
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class RepoAgent(BaseAgent):
    """仓库问答 Agent，专门用于回答关于 Gitee 仓库的问题"""
    
    def __init__(self):
        super().__init__()
    
    def chat(self, repo_owner: str, repo_name: str, question: str, ref: str = "master") -> Dict[str, Any]:
        """与仓库对话
        
        Args:
            repo_owner: 仓库所有者
            repo_name: 仓库名称
            question: 用户问题
            ref: 分支名称
            
        Returns:
            Agent 响应
        """
        # 构建系统提示词
        system_prompt = f"""你是一个专业的代码分析助手，专门帮助用户理解和分析 Gitee 上的开源仓库。

当前正在分析的仓库：{repo_owner}/{repo_name}
分支：{ref}

你可以使用以下工具来获取仓库信息：
1. get_repo_info - 获取仓库基本信息
2. get_readme - 读取 README 文件
3. list_directory - 列出目录结构
4. get_file_content - 读取文件内容
5. search_code - 在仓库中搜索代码
6. get_commits - 查看提交历史

工作流程：
1. 首先理解用户的问题
2. 判断需要哪些信息来回答问题
3. 使用合适的工具获取所需信息
4. 综合分析后给出详细、准确的回答

注意事项：
- 如果问题涉及整体结构，先查看 README 和目录结构
- 如果问题涉及具体代码实现，使用 get_file_content 读取相关文件
- 如果需要查找特定功能，使用 search_code
- 回答要基于实际的仓库内容，不要臆测
- 提供具体的代码路径和文件名作为引用
- 用中文回答，保持专业和友好的语气

用户的问题是：{question}

请开始分析并回答。"""
        
        # 运行 Agent
        result = self.run(user_input=question, system_prompt=system_prompt)
        
        if result.get("success"):
            return {
                "answer": result["answer"],
                "tool_calls": result["tool_calls"],
                "iterations": result["iterations"]
            }
        else:
            return {
                "answer": f"抱歉，处理您的问题时遇到错误：{result.get('error')}",
                "tool_calls": result.get("tool_calls", []),
                "error": result.get("error")
            }
