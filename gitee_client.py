"""
Gitee API 客户端
"""
import base64
from typing import Dict, List, Optional, Any
import httpx
from config import get_settings


class GiteeClient:
    """Gitee API 客户端"""
    
    def __init__(self):
        settings = get_settings()
        self.api_base = settings.gitee_api_base
        self.access_token = settings.gitee_access_token
        self.client = httpx.Client(timeout=30.0)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送 API 请求"""
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        params = kwargs.get('params', {})
        params['access_token'] = self.access_token
        kwargs['params'] = params
        
        try:
            response = self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}
    
    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """获取仓库信息"""
        return self._request("GET", f"/repos/{owner}/{repo}")
    
    def get_repo_tree(self, owner: str, repo: str, path: str = "", recursive: int = 0) -> Dict[str, Any]:
        """获取仓库目录树
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            path: 路径，默认为根目录
            recursive: 是否递归获取，1为递归，0为不递归
        """
        params = {"recursive": recursive}
        if path:
            params["path"] = path
        return self._request("GET", f"/repos/{owner}/{repo}/git/trees/master", params=params)
    
    def get_file_content(self, owner: str, repo: str, path: str, ref: str = "master") -> Dict[str, Any]:
        """获取文件内容
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            path: 文件路径
            ref: 分支名称，默认为 master
        """
        result = self._request("GET", f"/repos/{owner}/{repo}/contents/{path}", params={"ref": ref})
        
        # 解码 Base64 内容
        if "content" in result and not result.get("error"):
            try:
                result["decoded_content"] = base64.b64decode(result["content"]).decode("utf-8")
            except Exception as e:
                result["decode_error"] = str(e)
        
        return result
    
    def list_directory(self, owner: str, repo: str, path: str = "", ref: str = "master") -> List[Dict[str, Any]]:
        """列出目录内容
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            path: 目录路径，默认为根目录
            ref: 分支名称，默认为 master
        """
        result = self._request("GET", f"/repos/{owner}/{repo}/contents/{path}", params={"ref": ref})
        
        if isinstance(result, list):
            return result
        elif isinstance(result, dict) and not result.get("error"):
            return [result]
        else:
            return []
    
    def get_repo_readme(self, owner: str, repo: str, ref: str = "master") -> Dict[str, Any]:
        """获取仓库 README"""
        result = self._request("GET", f"/repos/{owner}/{repo}/readme", params={"ref": ref})
        
        # 解码内容
        if "content" in result and not result.get("error"):
            try:
                result["decoded_content"] = base64.b64decode(result["content"]).decode("utf-8")
            except Exception as e:
                result["decode_error"] = str(e)
        
        return result
    
    def search_repositories(self, query: str, page: int = 1, per_page: int = 20, 
                          language: Optional[str] = None, sort: str = "best_match") -> Dict[str, Any]:
        """搜索仓库
        
        Args:
            query: 搜索关键词
            page: 页码
            per_page: 每页数量
            language: 编程语言过滤
            sort: 排序方式，可选：best_match, stars, forks, updated
        """
        params = {
            "q": query,
            "page": page,
            "per_page": per_page,
            "sort": sort,
            "order": "desc"
        }
        
        if language:
            params["language"] = language
        
        return self._request("GET", "/search/repositories", params=params)
    
    def get_repo_commits(self, owner: str, repo: str, page: int = 1, per_page: int = 10, 
                        sha: str = "master") -> List[Dict[str, Any]]:
        """获取仓库提交历史
        
        Args:
            owner: 仓库所有者
            repo: 仓库名称
            page: 页码
            per_page: 每页数量
            sha: 分支名称
        """
        params = {
            "sha": sha,
            "page": page,
            "per_page": per_page
        }
        result = self._request("GET", f"/repos/{owner}/{repo}/commits", params=params)
        
        if isinstance(result, list):
            return result
        else:
            return []
    
    def search_code(self, query: str, owner: str, repo: str, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """在仓库中搜索代码
        
        Args:
            query: 搜索关键词
            owner: 仓库所有者
            repo: 仓库名称
            page: 页码
            per_page: 每页数量
        """
        search_query = f"{query} repo:{owner}/{repo}"
        params = {
            "q": search_query,
            "page": page,
            "per_page": per_page
        }
        return self._request("GET", "/search/code", params=params)
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'client'):
            self.client.close()
