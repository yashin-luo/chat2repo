# Chat2Repo - Gitee Repository Chat Agent

一个类似 GitHub Copilot Chat 的智能对话应用，连接 Gitee.com 仓库，支持 OpenAI 标准 API。

## 功能特性

### 1. 仓库智能问答
与 Gitee 上的任意仓库进行对话，Agent 会自动：
- 读取仓库文件内容
- 分析代码结构
- 查看提交历史
- 回答关于仓库的各种问题

### 2. 技术问题解答
提出技术问题，Agent 会：
- 在 Gitee 上搜索相关开源项目
- 提供技术解决方案
- 推荐参考实现

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# OpenAI 兼容的 LLM API 配置
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4

# Gitee API 配置
GITEE_ACCESS_TOKEN=your_gitee_token_here

# 服务配置
HOST=0.0.0.0
PORT=8000
```

### 3. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## API 使用示例

### 1. 仓库问答

```bash
curl -X POST "http://localhost:8000/api/chat/repo" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "openharmony",
    "repo_name": "docs",
    "question": "这个项目的主要目录结构是什么？",
    "session_id": "optional_session_id"
  }'
```

### 2. 技术问答

```bash
curl -X POST "http://localhost:8000/api/chat/tech" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "如何实现一个分布式任务队列？",
    "session_id": "optional_session_id"
  }'
```

### 3. 查看对话历史

```bash
curl "http://localhost:8000/api/sessions/{session_id}"
```

### 4. 访问 Web 界面

打开浏览器访问: http://localhost:8000

服务启动后，可以通过浏览器访问美观的 Web 界面，了解项目功能和使用方式。

## 项目结构

```
chat2repo/
├── main.py                 # FastAPI 应用入口
├── config.py              # 配置管理
├── gitee_client.py        # Gitee API 客户端
├── llm_client.py          # LLM 客户端（OpenAI 兼容）
├── agents/                # Agent 实现
│   ├── __init__.py
│   ├── base_agent.py     # Agent 基类
│   ├── repo_agent.py     # 仓库问答 Agent
│   └── search_agent.py   # 技术搜索 Agent
├── tools/                 # Agent 工具
│   ├── __init__.py
│   └── gitee_tools.py    # Gitee API 工具
├── models/                # 数据模型
│   └── __init__.py
├── requirements.txt       # Python 依赖
├── .env.example          # 环境变量示例
├── .gitignore            # Git 忽略文件
└── README.md             # 项目文档
```

## 开发说明

### Agent 工作原理

1. **仓库 Agent**：使用工具链（Tool Chain）模式
   - 工具1：读取文件内容
   - 工具2：列出目录结构
   - 工具3：搜索文件
   - 工具4：查看提交历史

2. **搜索 Agent**：使用规划执行（Plan & Execute）模式
   - 分析技术问题
   - 在 Gitee 搜索相关项目
   - 评估和筛选解决方案
   - 生成推荐报告

## License

MIT License
