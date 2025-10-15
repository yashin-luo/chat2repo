# Chat2Repo 开发文档

## 项目架构

### 整体架构

```
┌─────────────┐
│   客户端     │ (CLI / Web / API)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FastAPI    │ (REST API)
│   服务层     │
└──────┬──────┘
       │
       ├──────────┬──────────┐
       ▼          ▼          ▼
  ┌────────┐  ┌────────┐  ┌────────┐
  │ Repo   │  │ Search │  │ Session│
  │ Agent  │  │ Agent  │  │ Manager│
  └───┬────┘  └───┬────┘  └────────┘
      │           │
      ▼           ▼
  ┌──────────────────┐
  │   Tools Layer    │
  │  (Gitee Tools)   │
  └────┬─────────────┘
       │
       ├─────────────┬────────────┐
       ▼             ▼            ▼
  ┌────────┐   ┌─────────┐  ┌─────────┐
  │  LLM   │   │  Gitee  │  │ Config  │
  │ Client │   │  Client │  │ Manager │
  └────────┘   └─────────┘  └─────────┘
```

### 模块说明

#### 1. API 层 (`main.py`)
- 基于 FastAPI 的 REST API
- 提供三个主要端点：
  - `/api/chat/repo` - 仓库对话
  - `/api/chat/tech` - 技术搜索
  - `/api/sessions/*` - 会话管理
- 负责请求验证、会话管理、错误处理

#### 2. Agent 层 (`agents/`)
- **BaseAgent**: Agent 基类
  - 管理对话历史
  - 实现 Agent 循环（思考-行动-观察）
  - 处理工具调用
  
- **RepoAgent**: 仓库问答 Agent
  - 专门处理仓库相关问题
  - 自动选择合适的工具获取信息
  - 基于实际代码内容回答
  
- **SearchAgent**: 技术搜索 Agent
  - 在 Gitee 上搜索开源项目
  - 评估和筛选搜索结果
  - 提供技术方案建议

#### 3. 工具层 (`tools/`)
- **GiteeTools**: Gitee API 工具集
  - 提供 7 个核心工具：
    1. `get_repo_info` - 获取仓库信息
    2. `get_file_content` - 读取文件内容
    3. `list_directory` - 列出目录
    4. `get_readme` - 获取 README
    5. `search_code` - 搜索代码
    6. `get_commits` - 查看提交历史
    7. `search_repositories` - 搜索仓库
  - 使用 OpenAI Function Calling 格式

#### 4. 客户端层
- **GiteeClient** (`gitee_client.py`): Gitee API 客户端
  - 封装所有 Gitee API 调用
  - 处理认证和错误
  - 解码 Base64 内容
  
- **LLMClient** (`llm_client.py`): LLM 客户端
  - 支持 OpenAI 标准 API
  - 支持 Function Calling
  - 支持流式响应（预留）

#### 5. 配置层 (`config.py`)
- 使用 Pydantic Settings
- 从环境变量和 .env 文件加载配置
- 提供配置单例

#### 6. 数据模型 (`models/`)
- 使用 Pydantic 定义所有数据模型
- 包括请求、响应、会话历史等

## Agent 工作原理

### RepoAgent 工作流程

```
用户问题
   │
   ▼
系统提示词构建
   │
   ▼
Agent 循环开始
   │
   ├─→ LLM 思考
   │      │
   │      ├─→ 需要调用工具？
   │      │      │
   │      │      YES ─→ 调用工具
   │      │      │         │
   │      │      │         ▼
   │      │      │    执行工具函数
   │      │      │         │
   │      │      │         ▼
   │      │      │    获取结果
   │      │      │         │
   │      │      └─────────┘
   │      │      
   │      NO
   │      │
   │      ▼
   │   生成最终答案
   │
   ▼
返回结果
```

### 工具调用示例

当用户问："这个项目的主要功能是什么？"

1. **第一轮**：
   - LLM 决定先获取 README
   - 调用 `get_readme(owner, repo)`
   - 获取 README 内容

2. **第二轮**：
   - LLM 基于 README 内容思考
   - 可能还需要查看目录结构
   - 调用 `list_directory(owner, repo, "")`
   - 获取根目录列表

3. **第三轮**：
   - LLM 基于收集的信息
   - 生成最终答案
   - 返回给用户

## 开发指南

### 添加新的工具

1. 在 `GiteeClient` 中添加 API 方法：

```python
def new_api_method(self, param1, param2):
    return self._request("GET", f"/some/endpoint")
```

2. 在 `GiteeTools` 中添加工具定义：

```python
@staticmethod
def get_tools_definition():
    return [
        # ... 现有工具
        {
            "type": "function",
            "function": {
                "name": "new_tool",
                "description": "工具描述",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "参数描述"
                        }
                    },
                    "required": ["param1"]
                }
            }
        }
    ]
```

3. 实现工具函数：

```python
def new_tool(self, param1):
    result = self.client.new_api_method(param1)
    return {"result": result}
```

4. 在 `execute_tool` 中添加路由：

```python
def execute_tool(self, tool_name, arguments):
    if tool_name == "new_tool":
        return self.new_tool(**arguments)
    # ... 其他工具
```

### 添加新的 Agent

1. 创建新的 Agent 类：

```python
from .base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__()
    
    def my_method(self, param):
        system_prompt = """系统提示词"""
        result = self.run(user_input=param, system_prompt=system_prompt)
        return result
```

2. 在 `main.py` 中添加端点：

```python
@app.post("/api/my-endpoint")
async def my_endpoint(request: MyRequest):
    agent = MyAgent()
    result = agent.my_method(request.param)
    return ChatResponse(
        answer=result["answer"],
        session_id=session_id,
        tool_calls=result.get("tool_calls", [])
    )
```

### 配置不同的 LLM 提供商

#### OpenAI

```env
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
```

#### Azure OpenAI

```env
OPENAI_API_BASE=https://your-resource.openai.azure.com/openai/deployments/your-deployment
OPENAI_API_KEY=your-azure-key
OPENAI_MODEL=gpt-4
```

#### 其他兼容 OpenAI API 的服务

```env
OPENAI_API_BASE=https://api.your-service.com/v1
OPENAI_API_KEY=your-key
OPENAI_MODEL=your-model
```

## 测试

### 单元测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest tests/
```

### 集成测试

```bash
# 启动服务
python main.py &

# 运行测试客户端
python test_client.py

# 停止服务
pkill -f "python main.py"
```

### 手动测试

使用 CLI 工具：

```bash
# 交互式模式
python cli.py interactive

# 单次命令
python cli.py repo dromara hutool "这个项目是做什么的？"
python cli.py tech "推荐一个任务队列" --language Python
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t chat2repo .

# 运行容器
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name chat2repo \
  chat2repo
```

### Docker Compose 部署

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### 生产环境部署

1. 使用 Gunicorn + Uvicorn Workers：

```bash
pip install gunicorn

gunicorn main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

2. 配置 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. 使用 Systemd 服务：

```ini
[Unit]
Description=Chat2Repo Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/chat2repo
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 性能优化

### 1. 缓存策略

可以添加 Redis 缓存来缓存 Gitee API 响应：

```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_with_cache(key, fetch_func, ttl=3600):
    cached = cache.get(key)
    if cached:
        return json.loads(cached)
    
    data = fetch_func()
    cache.setex(key, ttl, json.dumps(data))
    return data
```

### 2. 异步处理

将长时间运行的任务改为异步：

```python
from fastapi import BackgroundTasks

@app.post("/api/chat/repo")
async def chat_with_repo(request: RepoChatRequest, background_tasks: BackgroundTasks):
    # 异步处理
    pass
```

### 3. 限流

使用 slowapi 添加 API 限流：

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat/repo")
@limiter.limit("10/minute")
async def chat_with_repo(request: Request, chat_request: RepoChatRequest):
    pass
```

## 故障排查

### 常见问题

1. **连接 Gitee API 失败**
   - 检查 `GITEE_ACCESS_TOKEN` 是否有效
   - 检查网络连接
   - 查看 Gitee API 状态

2. **LLM API 调用失败**
   - 检查 `OPENAI_API_KEY` 是否正确
   - 检查 `OPENAI_API_BASE` 配置
   - 查看余额和配额

3. **Agent 达到最大迭代次数**
   - 检查工具实现是否正确
   - 增大 `MAX_ITERATIONS` 配置
   - 优化系统提示词

### 日志

启用详细日志：

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## License

MIT License
