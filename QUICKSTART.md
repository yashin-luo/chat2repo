# Chat2Repo 快速开始指南

## 5 分钟快速体验

### 第一步：克隆项目

```bash
git clone <your-repo-url>
cd chat2repo
```

### 第二步：配置环境

1. 复制配置文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入必要的配置：

```env
# OpenAI API 配置（必需）
OPENAI_API_KEY=sk-your-api-key-here

# Gitee Access Token（必需）
# 获取方式：https://gitee.com/profile/personal_access_tokens
GITEE_ACCESS_TOKEN=your-gitee-token-here
```

> **获取 Gitee Token**:
> 1. 访问 https://gitee.com/profile/personal_access_tokens
> 2. 点击"生成新令牌"
> 3. 选择权限：`projects` (只读即可)
> 4. 复制生成的 token

### 第三步：安装依赖

```bash
# 使用 pip
pip install -r requirements.txt

# 或使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 第四步：启动服务

```bash
python main.py
```

或使用启动脚本：
```bash
./run.sh
```

看到以下输出表示启动成功：
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 第五步：测试 API

#### 方法 1: 使用 CLI 工具（推荐）

```bash
# 交互式模式
python cli.py interactive

# 然后输入命令
> repo dromara hutool
> 这个项目是做什么的？
```

#### 方法 2: 使用 curl

```bash
# 测试健康检查
curl http://localhost:8000/health

# 仓库问答
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目的主要功能是什么？"
  }'
```

#### 方法 3: 访问 API 文档

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 使用示例

### 示例 1：询问项目信息

**问题**: "这个项目是用什么语言写的？有多少 Star？"

```bash
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "vuejs",
    "repo_name": "core",
    "question": "这个项目是用什么语言写的？有多少 Star？"
  }'
```

**Agent 会**:
1. 调用 `get_repo_info` 工具获取仓库基本信息
2. 分析返回的数据
3. 生成回答

### 示例 2：查看目录结构

**问题**: "这个项目的主要目录结构是什么？"

```bash
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目的主要目录结构是什么？"
  }'
```

**Agent 会**:
1. 调用 `list_directory` 工具列出根目录
2. 可能会进一步查看子目录
3. 总结目录结构

### 示例 3：阅读具体文件

**问题**: "README 里说了什么？"

```bash
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "README 里说了什么？"
  }'
```

**Agent 会**:
1. 调用 `get_readme` 工具读取 README
2. 提取关键信息
3. 生成摘要

### 示例 4：持续对话

```bash
# 第一次对话
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目有哪些核心模块？",
    "session_id": "my-session-123"
  }'

# 第二次对话（延续上下文）
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "第一个模块是做什么的？",
    "session_id": "my-session-123"
  }'
```

### 示例 5：技术搜索

**问题**: "推荐一些 Java 工具库"

```bash
curl -X POST http://localhost:8000/api/chat/tech \
  -H "Content-Type: application/json" \
  -d '{
    "question": "推荐一些好用的 Java 工具库",
    "language": "Java"
  }'
```

**Agent 会**:
1. 调用 `search_repositories` 工具搜索
2. 分析搜索结果（星标、更新时间、描述）
3. 推荐 2-5 个最佳项目
4. 解释每个项目的特点

## 进阶使用

### 使用 Python 客户端

创建文件 `my_client.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# 创建会话
session_id = "my-session"

# 第一次提问
response1 = requests.post(
    f"{BASE_URL}/api/chat/repo",
    json={
        "repo_owner": "dromara",
        "repo_name": "hutool",
        "question": "这个项目主要解决什么问题？",
        "session_id": session_id
    }
).json()

print("回答 1:", response1["answer"])
print("工具调用:", len(response1["tool_calls"]), "次")

# 第二次提问（基于上下文）
response2 = requests.post(
    f"{BASE_URL}/api/chat/repo",
    json={
        "repo_owner": "dromara",
        "repo_name": "hutool",
        "question": "能给我看看具体的代码实现吗？",
        "session_id": session_id
    }
).json()

print("回答 2:", response2["answer"])

# 查看完整对话历史
history = requests.get(f"{BASE_URL}/api/sessions/{session_id}").json()
print(f"\n完整对话 ({len(history['messages'])} 条消息):")
for msg in history["messages"]:
    print(f"[{msg['role']}] {msg['content'][:100]}...")
```

运行：
```bash
python my_client.py
```

### 使用交互式 CLI

```bash
python cli.py interactive
```

进入交互模式后：

```
[命令] > repo dromara hutool
已切换到仓库模式: dromara/hutool

[仓库: dromara/hutool] > 这个项目是做什么的？
(Agent 开始工作...)

[仓库: dromara/hutool] > 有哪些主要模块？
(继续对话...)

[仓库: dromara/hutool] > history
(查看对话历史)

[仓库: dromara/hutool] > tech
已切换到技术搜索模式

[技术搜索] > 推荐一些消息队列中间件
(搜索技术方案...)

[技术搜索] > quit
再见！
```

## Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 确保 .env 文件已配置
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 使用 Docker

```bash
# 构建镜像
docker build -t chat2repo .

# 运行容器
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name chat2repo \
  chat2repo

# 查看日志
docker logs -f chat2repo

# 停止容器
docker stop chat2repo
docker rm chat2repo
```

## 常见问题

### Q1: 启动时报错 "未设置 OPENAI_API_KEY"

**解决**: 检查 .env 文件是否存在，并且配置了正确的 API Key。

```bash
# 检查 .env 文件
cat .env | grep OPENAI_API_KEY

# 如果没有，添加配置
echo "OPENAI_API_KEY=sk-your-key" >> .env
```

### Q2: Gitee API 调用失败

**可能原因**:
1. Token 未配置或已过期
2. Token 权限不足
3. 网络连接问题

**解决**:
```bash
# 测试 Token 是否有效
curl "https://gitee.com/api/v5/user?access_token=YOUR_TOKEN"

# 如果返回用户信息，说明 Token 有效
```

### Q3: Agent 达到最大迭代次数

**原因**: Agent 可能陷入循环，或者问题过于复杂。

**解决**:
1. 简化问题
2. 增加最大迭代次数：在 .env 中设置 `MAX_ITERATIONS=15`
3. 检查工具实现是否正确

### Q4: 响应时间太长

**原因**: 
1. LLM API 响应慢
2. Gitee API 响应慢
3. 需要多次工具调用

**解决**:
1. 使用更快的模型（如 gpt-3.5-turbo）
2. 添加缓存机制
3. 优化系统提示词

### Q5: 如何使用其他 LLM（非 OpenAI）？

**解决**: 只要服务支持 OpenAI API 格式即可。

例如使用 Azure OpenAI:
```env
OPENAI_API_BASE=https://your-resource.openai.azure.com/openai/deployments/your-deployment
OPENAI_API_KEY=your-azure-key
OPENAI_MODEL=gpt-4
```

或使用本地部署的兼容服务（如 LocalAI、FastChat）:
```env
OPENAI_API_BASE=http://localhost:8080/v1
OPENAI_API_KEY=dummy
OPENAI_MODEL=your-model
```

## 下一步

- 📖 阅读完整的 [开发文档](DEVELOPMENT.md)
- 🏗️ 了解 [架构设计](ARCHITECTURE.md)
- 📝 查看更多 [使用示例](examples.md)
- 🐛 遇到问题？查看 [GitHub Issues](https://github.com/your-repo/issues)

## 获取帮助

- 文档: 查看本项目的 README 和其他文档
- 问题: 提交 GitHub Issue
- 讨论: GitHub Discussions

## 贡献

欢迎贡献代码、报告 Bug、提出新功能建议！

祝使用愉快！🎉
