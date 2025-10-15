# Chat2Repo - Gitee 仓库智能对话系统

[English](README.md) | 简体中文

一个类似 GitHub Copilot Chat 的智能对话应用，连接 Gitee.com 仓库，基于 OpenAI 标准 API 的 Agent 系统。

## ✨ 核心特性

### 🤖 功能 1：仓库智能问答
与 Gitee 上的任意仓库进行自然语言对话：
- 📖 自动读取仓库文件和代码
- 🔍 智能分析项目结构
- 💬 支持多轮连续对话
- 📝 基于实际代码内容回答

**示例对话**：
```
你：这个项目是用什么语言写的？主要功能是什么？
Agent：[自动调用 get_repo_info 和 get_readme]
      这是一个用 Java 编写的工具类库...

你：src 目录下有哪些主要模块？
Agent：[自动调用 list_directory]
      src 目录包含以下模块：...
```

### 🔎 功能 2：技术问题解答
提出技术问题，获取 Gitee 上的开源解决方案：
- 🌐 在 Gitee 搜索相关开源项目
- ⭐ 评估项目质量和活跃度
- 📊 推荐 2-5 个最佳方案
- 💡 分析每个方案的特点和适用场景

**示例对话**：
```
你：推荐一些 Java 的工具类库
Agent：[自动搜索 Gitee]
      我为您找到以下优秀项目：
      1. Hutool - 5000+ stars，功能全面的 Java 工具库...
      2. ...
```

## 🚀 5 分钟快速开始

### 1. 克隆项目
```bash
git clone <your-repo>
cd chat2repo
```

### 2. 配置环境
```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env，填入以下配置
OPENAI_API_KEY=sk-your-api-key        # OpenAI API Key
GITEE_ACCESS_TOKEN=your-gitee-token   # Gitee Token
```

> **获取 Gitee Token**: 访问 https://gitee.com/profile/personal_access_tokens

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动服务
```bash
python main.py
# 或使用脚本
./run.sh
```

### 5. 开始使用

#### 方式 1: 使用 CLI 工具（推荐）
```bash
python cli.py interactive

# 进入交互模式后
> repo dromara hutool
> 这个项目是做什么的？
```

#### 方式 2: 使用 API
```bash
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目的主要功能是什么？"
  }'
```

#### 方式 3: 使用 Web 聊天界面（推荐）
打开浏览器访问聊天页面：http://localhost:8000/static/chat.html

**聊天页面特性**：
- 🎯 支持技术问答和仓库对话两种模式
- 💬 实时消息显示，支持 Markdown 格式
- 📚 自动保存会话历史，随时恢复对话
- 🎨 现代化 UI，响应式设计
- ⚡ 快速示例问题，一键开始对话

详细说明请参考：[聊天页面文档](CHAT_PAGE.md)

#### 方式 4: 访问 API 文档
打开浏览器: http://localhost:8000/docs

## 📖 详细文档

- 📘 [快速开始指南](QUICKSTART.md) - 5 分钟快速体验
- 💬 [聊天页面文档](CHAT_PAGE.md) - Web 对话界面使用指南
- 📙 [使用示例](examples.md) - 丰富的使用案例
- 📕 [开发文档](DEVELOPMENT.md) - 开发指南和最佳实践
- 📗 [架构设计](ARCHITECTURE.md) - 系统架构详解
- 📋 [项目清单](CHECKLIST.md) - 功能完成情况

## 🏗️ 项目架构

```
用户
 ↓
FastAPI REST API
 ↓
Agent 系统 (RepoAgent / SearchAgent)
 ↓
工具层 (7 个 Gitee 工具)
 ↓
客户端层 (LLM Client / Gitee Client)
```

### 核心组件

- **Agent 系统**: 基于 ReAct 模式的智能 Agent
- **工具集**: 7 个精心设计的 Gitee API 工具
- **LLM 集成**: 支持 OpenAI 标准 API 的所有兼容服务
- **会话管理**: 多会话支持，上下文自动恢复

## 🛠️ 技术栈

- **后端**: Python 3.8+ / FastAPI / Uvicorn
- **AI**: OpenAI API (支持 Azure OpenAI、本地 LLM 等)
- **API**: Gitee API v5
- **数据验证**: Pydantic
- **配置**: Environment Variables / .env

## 📦 Docker 部署

### 使用 Docker Compose（推荐）
```bash
docker-compose up -d
```

### 使用 Docker
```bash
docker build -t chat2repo .
docker run -d -p 8000:8000 --env-file .env chat2repo
```

## 💡 使用场景

### 1. 快速了解开源项目
```bash
# 想了解一个新项目？直接问！
python cli.py repo openharmony docs "这个项目的文档结构是怎样的？"
```

### 2. 代码学习和研究
```bash
# 深入学习具体实现
> 这个项目是如何处理 HTTP 请求的？
> 能给我看看相关的代码吗？
```

### 3. 技术选型
```bash
# 寻找技术解决方案
python cli.py tech "推荐一些微服务框架" --language Go
```

### 4. 持续对话
```bash
# 保持对话上下文
> 这个项目用的什么构建工具？
> 那配置文件在哪里？
> 能给我看看配置的内容吗？
```

## 🎯 主要特点

- ✅ **智能 Agent**: 自主决定需要哪些信息
- ✅ **多轮对话**: 理解上下文，连续对话
- ✅ **实时查询**: 直接读取 Gitee 仓库内容
- ✅ **准确回答**: 基于实际代码，不是臆测
- ✅ **易于扩展**: 模块化设计，易于添加新功能
- ✅ **开箱即用**: 完整文档，5 分钟启动

## 🔧 配置示例

### 支持 OpenAI
```env
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4
```

### 支持 Azure OpenAI
```env
OPENAI_API_BASE=https://your.openai.azure.com/openai/deployments/gpt-4
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4
```

### 支持其他兼容服务
```env
OPENAI_API_BASE=http://localhost:8080/v1
OPENAI_API_KEY=dummy
OPENAI_MODEL=your-model
```

## 📊 项目状态

- ✅ **核心功能**: 已完成
- ✅ **文档**: 完善
- ✅ **代码质量**: 良好
- ✅ **可用性**: 可以部署使用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙋 FAQ

**Q: 如何获取 Gitee Token？**
A: 访问 https://gitee.com/profile/personal_access_tokens，创建一个新 Token，只需要 `projects` 读权限。

**Q: 支持哪些 LLM？**
A: 支持所有兼容 OpenAI API 格式的服务，包括 OpenAI、Azure OpenAI、本地部署的 LLM（如 LocalAI）等。

**Q: 响应时间多长？**
A: 通常 5-30 秒，取决于 LLM 响应速度和工具调用次数。

**Q: 是否支持 GitHub？**
A: 当前版本专注于 Gitee，GitHub 支持已列入路线图。

**Q: 如何添加新功能？**
A: 参考 [开发文档](DEVELOPMENT.md) 的扩展指南。

## 🌟 Star History

如果觉得这个项目有用，请给个 Star ⭐️！

---

**Made with ❤️ for the open source community**
