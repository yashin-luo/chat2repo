"""
技术搜索 Agent
"""
from typing import Dict, Any, Optional
from .base_agent import BaseAgent


class SearchAgent(BaseAgent):
    """技术搜索 Agent，帮助用户找到技术问题的开源解决方案"""
    
    def __init__(self):
        super().__init__()
    
    def search(self, question: str, language: Optional[str] = None) -> Dict[str, Any]:
        """搜索技术解决方案
        
        Args:
            question: 技术问题
            language: 编程语言过滤（可选）
            
        Returns:
            Agent 响应
        """
        # 构建系统提示词
        language_filter = f"，重点关注 {language} 语言的项目" if language else ""
        
        system_prompt = f"""你是一个专业的技术顾问，帮助开发者在 Gitee 上找到合适的开源解决方案。

当前任务：根据用户的技术问题，在 Gitee 上搜索相关的开源项目，并提供专业的建议。

你可以使用的工具：
1. search_repositories - 在 Gitee 上搜索开源仓库

工作流程：
1. 分析用户的技术需求
2. 提取关键词，在 Gitee 上搜索相关项目
3. 评估搜索结果的质量（星标数、更新时间、描述等）
4. 为用户推荐最合适的 2-5 个项目
5. 解释每个项目的特点和适用场景

搜索策略：
- 优先搜索中文关键词（因为 Gitee 以中文社区为主）
- 可以尝试多个相关关键词组合
- 考虑使用技术栈、框架名称等作为关键词
- 注意项目的活跃度（更新时间、星标数）{language_filter}

回答格式：
1. 简要说明搜索策略
2. 列出推荐的项目（包含项目名、描述、星标数、链接）
3. 对每个项目的特点和适用场景进行分析
4. 给出最终建议

用户的问题是：{question}

请开始搜索并提供建议。"""
        
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
                "answer": f"抱歉，搜索时遇到错误：{result.get('error')}",
                "tool_calls": result.get("tool_calls", []),
                "error": result.get("error")
            }
