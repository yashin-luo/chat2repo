# Chat2Repo 架构设计文档

## 系统概述

Chat2Repo 是一个智能代码仓库对话系统，通过 AI Agent 的方式帮助用户理解和探索 Gitee 上的开源项目，同时提供技术问题的解决方案搜索。

## 核心特性

### 1. 仓库智能问答 (Repo Agent)
- **自主信息获取**: Agent 自动决定需要读取哪些文件
- **多轮对话**: 支持上下文理解的连续对话
- **深度分析**: 可以分析代码结构、实现逻辑、提交历史等
- **精准引用**: 回答时会引用具体的文件路径和代码片段

### 2. 技术方案搜索 (Search Agent)
- **智能搜索**: 根据技术问题在 Gitee 搜索相关项目
- **方案评估**: 分析项目的活跃度、星标数、适用场景
- **多维度推荐**: 提供 2-5 个最佳方案供选择
- **中文优化**: 针对 Gitee 中文社区优化搜索策略

## 技术架构

### 架构图

```
┌──────────────────────────────────────────────────────────┐
│                      客户端层                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │   CLI   │  │   Web   │  │  REST   │  │  SDK    │    │
│  │  工具    │  │   UI    │  │   API   │  │  Client │    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────────────┐
│                    FastAPI 服务层                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  路由 (main.py)                                   │   │
│  │  • POST /api/chat/repo  - 仓库对话               │   │
│  │  • POST /api/chat/tech  - 技术搜索               │   │
│  │  • GET  /api/sessions   - 会话管理               │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  会话管理器                                       │   │
│  │  • 对话历史存储                                   │   │
│  │  • 上下文维护                                     │   │
│  │  • 多租户隔离                                     │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────────────┐
│                      Agent 层                             │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  BaseAgent (基础 Agent)                           │   │
│  │  • Agent 运行循环 (思考-行动-观察)                │   │
│  │  • 工具调用管理                                   │   │
│  │  • 对话历史管理                                   │   │
│  │  • 迭代控制                                       │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐     │
│  │  RepoAgent          │    │  SearchAgent        │     │
│  │  (仓库问答)          │    │  (技术搜索)          │     │
│  │                     │    │                     │     │
│  │  • 仓库信息获取      │    │  • 关键词提取        │     │
│  │  • 文件内容读取      │    │  • 仓库搜索          │     │
│  │  • 代码结构分析      │    │  • 结果评估          │     │
│  │  • 上下文理解        │    │  • 方案推荐          │     │
│  └─────────────────────┘    └─────────────────────┘     │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────────────┐
│                      工具层                               │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  GiteeTools (Gitee 工具集)                        │   │
│  │                                                   │   │
│  │  1. get_repo_info      - 获取仓库基本信息         │   │
│  │  2. get_file_content   - 读取文件内容             │   │
│  │  3. list_directory     - 列出目录结构             │   │
│  │  4. get_readme         - 获取 README              │   │
│  │  5. search_code        - 搜索代码                 │   │
│  │  6. get_commits        - 查看提交历史             │   │
│  │  7. search_repositories - 搜索仓库               │   │
│  │                                                   │   │
│  │  • OpenAI Function Calling 格式                  │   │
│  │  • 自动参数验证                                   │   │
│  │  • 结果格式化                                     │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────┴─────────────────────────────────┐
│                    客户端层                               │
│                                                           │
│  ┌─────────────────────┐    ┌─────────────────────┐     │
│  │  LLMClient          │    │  GiteeClient        │     │
│  │  (LLM 客户端)        │    │  (Gitee API 客户端)  │     │
│  │                     │    │                     │     │
│  │  • OpenAI API       │    │  • Gitee API v5     │     │
│  │  • Function Calling │    │  • 认证管理          │     │
│  │  • 流式响应          │    │  • 请求封装          │     │
│  │  • 错误处理          │    │  • Base64 解码       │     │
│  └─────────────────────┘    └─────────────────────┘     │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  ConfigManager (配置管理)                         │   │
│  │  • 环境变量加载                                    │   │
│  │  • 配置验证                                        │   │
│  │  • 单例模式                                        │   │
│  └──────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

## 数据流

### 1. 仓库问答流程

```
用户请求
  ↓
FastAPI 接收
  ↓
创建/恢复会话
  ↓
创建 RepoAgent
  ↓
恢复对话历史
  ↓
构建系统提示词
  ↓
┌─────────────────────────────────────────┐
│         Agent 循环 (最多 10 轮)          │
│                                         │
│  1. 调用 LLM (带工具定义)                │
│     ↓                                   │
│  2. LLM 分析并决定行动                   │
│     ↓                                   │
│  3a. 需要调用工具？                      │
│      ↓ YES                              │
│      调用 GiteeTools                    │
│      ↓                                   │
│      执行 Gitee API 请求                │
│      ↓                                   │
│      返回结果给 LLM                      │
│      ↓                                   │
│      继续下一轮                          │
│                                         │
│  3b. 不需要工具                          │
│      ↓ NO                               │
│      生成最终答案                        │
│      ↓                                   │
│      跳出循环                            │
└─────────────────────────────────────────┘
  ↓
保存对话到会话
  ↓
返回响应给用户
```

### 2. 技术搜索流程

```
技术问题
  ↓
SearchAgent
  ↓
分析问题提取关键词
  ↓
调用 search_repositories
  ↓
获取搜索结果
  ↓
评估项目质量
  ↓
生成推荐报告
  ↓
返回给用户
```

## 核心组件详解

### 1. BaseAgent - Agent 引擎

**职责**:
- 实现 ReAct (Reasoning + Acting) 模式
- 管理工具调用循环
- 维护对话上下文
- 控制迭代次数防止无限循环

**核心方法**:
```python
def run(user_input, system_prompt):
    while iterations < max_iterations:
        # 1. 调用 LLM
        response = llm.chat(messages, tools)
        
        # 2. 检查是否需要调用工具
        if has_tool_calls:
            # 3. 执行工具
            results = execute_tools(tool_calls)
            # 4. 将结果返回给 LLM
            messages.append(results)
            continue
        else:
            # 5. 返回最终答案
            return response
```

### 2. GiteeTools - 工具系统

**设计原则**:
- 每个工具职责单一
- 使用 OpenAI Function Calling 标准格式
- 自动参数验证和类型转换
- 结果标准化处理

**工具定义示例**:
```python
{
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "读取仓库中指定文件的内容",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "仓库所有者"},
                "repo": {"type": "string", "description": "仓库名称"},
                "path": {"type": "string", "description": "文件路径"}
            },
            "required": ["owner", "repo", "path"]
        }
    }
}
```

### 3. Session Management - 会话管理

**功能**:
- 多会话隔离
- 对话历史持久化
- 上下文自动恢复
- 会话生命周期管理

**存储结构**:
```python
sessions = {
    "session_id": {
        "messages": [
            {"role": "user", "content": "问题1"},
            {"role": "assistant", "content": "答案1"},
            {"role": "user", "content": "问题2"},
            {"role": "assistant", "content": "答案2"}
        ],
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:05:00"
    }
}
```

## 配置系统

### 环境变量

```bash
# LLM 配置
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4

# Gitee 配置
GITEE_ACCESS_TOKEN=xxx
GITEE_API_BASE=https://gitee.com/api/v5

# 服务配置
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Agent 配置
MAX_ITERATIONS=10
TIMEOUT=300
```

### 配置加载

使用 Pydantic Settings 自动加载和验证：

```python
class Settings(BaseSettings):
    openai_api_key: str  # 必需
    gitee_access_token: str  # 必需
    openai_model: str = "gpt-4"  # 可选，有默认值
    
    class Config:
        env_file = ".env"
```

## 安全考虑

### 1. API 密钥保护
- 使用环境变量存储
- 不提交到版本控制
- 使用 .gitignore 排除 .env

### 2. 输入验证
- Pydantic 模型验证所有输入
- 参数类型检查
- 长度和格式限制

### 3. 错误处理
- 统一异常处理
- 不暴露敏感信息
- 友好的错误消息

### 4. 访问控制
- Gitee Token 权限最小化
- 可选的 API 认证
- 请求限流

## 扩展性设计

### 1. 支持更多代码托管平台

添加新的客户端和工具：
```python
# github_client.py
class GitHubClient: ...

# github_tools.py  
class GitHubTools: ...
```

### 2. 支持更多 LLM 提供商

抽象 LLM 接口：
```python
class BaseLLMClient(ABC):
    @abstractmethod
    def chat(self, messages): ...

class OpenAIClient(BaseLLMClient): ...
class ClaudeClient(BaseLLMClient): ...
```

### 3. 添加更多 Agent 类型

继承 BaseAgent：
```python
class DocAgent(BaseAgent):  # 文档生成
class ReviewAgent(BaseAgent):  # 代码审查
class TestAgent(BaseAgent):  # 测试生成
```

### 4. 持久化存储

替换内存存储：
```python
# 使用 Redis
from redis import Redis
sessions = RedisSessionStore(Redis())

# 使用数据库
from sqlalchemy import create_engine
sessions = DBSessionStore(engine)
```

## 性能优化

### 1. 缓存策略
- Gitee API 响应缓存
- LLM 响应缓存（相同问题）
- 文件内容缓存

### 2. 并发处理
- 异步 HTTP 请求
- 并行工具调用
- 流式响应

### 3. 资源限制
- 最大迭代次数
- 请求超时
- 文件大小限制
- Token 数量限制

## 监控和日志

### 关键指标
- API 请求量和响应时间
- Agent 迭代次数分布
- 工具调用频率
- 错误率和类型
- LLM Token 使用量

### 日志级别
- DEBUG: 详细的执行流程
- INFO: 关键操作记录
- WARNING: 可恢复的错误
- ERROR: 系统错误

## 未来规划

### 短期 (1-3 个月)
- [ ] 添加单元测试和集成测试
- [ ] 实现 Redis 会话存储
- [ ] 添加 API 认证和限流
- [ ] Web UI 界面
- [ ] 流式响应支持

### 中期 (3-6 个月)
- [ ] 支持 GitHub、GitLab
- [ ] 代码审查 Agent
- [ ] 文档生成 Agent
- [ ] 多语言支持
- [ ] 插件系统

### 长期 (6-12 个月)
- [ ] 本地部署的 LLM 支持
- [ ] 企业版功能（SSO、审计）
- [ ] 代码执行沙箱
- [ ] PR 自动化处理
- [ ] IDE 插件集成
