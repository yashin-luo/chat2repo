# Chat2Repo 使用示例

## 1. 仓库问答示例

### 示例 1：询问项目结构

```bash
curl -X POST "http://localhost:8000/api/chat/repo" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目的主要模块有哪些？每个模块的作用是什么？"
  }'
```

### 示例 2：询问具体实现

```bash
curl -X POST "http://localhost:8000/api/chat/repo" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目是如何处理 HTTP 请求的？能给我看看相关代码吗？"
  }'
```

### 示例 3：持续对话（使用 session_id）

第一次对话：
```bash
curl -X POST "http://localhost:8000/api/chat/repo" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "这个项目用的什么构建工具？",
    "session_id": "my-session-123"
  }'
```

第二次对话（延续上下文）：
```bash
curl -X POST "http://localhost:8000/api/chat/repo" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "那配置文件在哪里？",
    "session_id": "my-session-123"
  }'
```

## 2. 技术问答示例

### 示例 1：寻找分布式解决方案

```bash
curl -X POST "http://localhost:8000/api/chat/tech" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "我需要一个分布式任务调度框架，最好是 Java 的，有什么推荐？"
  }'
```

### 示例 2：指定编程语言

```bash
curl -X POST "http://localhost:8000/api/chat/tech" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "推荐一些微服务框架",
    "language": "Go"
  }'
```

### 示例 3：前端框架搜索

```bash
curl -X POST "http://localhost:8000/api/chat/tech" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "有没有好用的 Vue 3 管理后台模板？",
    "language": "JavaScript"
  }'
```

### 示例 4：特定技术栈

```bash
curl -X POST "http://localhost:8000/api/chat/tech" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "基于 Spring Boot 的权限管理系统"
  }'
```

## 3. 会话管理示例

### 查看会话历史

```bash
curl "http://localhost:8000/api/sessions/my-session-123"
```

### 列出所有会话

```bash
curl "http://localhost:8000/api/sessions"
```

### 删除会话

```bash
curl -X DELETE "http://localhost:8000/api/sessions/my-session-123"
```

## 4. Python 客户端示例

```python
import requests
import json

# 配置
BASE_URL = "http://localhost:8000"

# 1. 仓库问答
def chat_with_repo(owner, repo, question, session_id=None):
    url = f"{BASE_URL}/api/chat/repo"
    data = {
        "repo_owner": owner,
        "repo_name": repo,
        "question": question
    }
    if session_id:
        data["session_id"] = session_id
    
    response = requests.post(url, json=data)
    return response.json()

# 2. 技术问答
def search_solution(question, language=None, session_id=None):
    url = f"{BASE_URL}/api/chat/tech"
    data = {
        "question": question
    }
    if language:
        data["language"] = language
    if session_id:
        data["session_id"] = session_id
    
    response = requests.post(url, json=data)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 示例 1：询问仓库
    result = chat_with_repo(
        owner="dromara",
        repo="hutool",
        question="这个项目主要用来做什么？"
    )
    print("答案：", result["answer"])
    print("工具调用：", result["tool_calls"])
    
    # 示例 2：搜索技术方案
    result = search_solution(
        question="推荐一个消息队列中间件",
        language="Java"
    )
    print("答案：", result["answer"])
    print("工具调用：", result["tool_calls"])
```

## 5. JavaScript/TypeScript 客户端示例

```typescript
// chat2repo-client.ts
interface RepoChatRequest {
  repo_owner: string;
  repo_name: string;
  question: string;
  session_id?: string;
  ref?: string;
}

interface TechChatRequest {
  question: string;
  session_id?: string;
  language?: string;
}

interface ChatResponse {
  answer: string;
  session_id: string;
  tool_calls?: any[];
}

class Chat2RepoClient {
  private baseUrl: string;

  constructor(baseUrl: string = "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }

  async chatWithRepo(request: RepoChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat/repo`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
    return response.json();
  }

  async searchSolution(request: TechChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat/tech`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
    return response.json();
  }

  async getSession(sessionId: string) {
    const response = await fetch(`${this.baseUrl}/api/sessions/${sessionId}`);
    return response.json();
  }
}

// 使用示例
const client = new Chat2RepoClient();

// 仓库问答
client.chatWithRepo({
  repo_owner: "dromara",
  repo_name: "hutool",
  question: "这个项目的核心功能是什么？"
}).then(result => {
  console.log("答案：", result.answer);
});

// 技术搜索
client.searchSolution({
  question: "推荐一些后台管理系统模板",
  language: "Vue"
}).then(result => {
  console.log("答案：", result.answer);
});
```

## 6. 高级用法

### 多轮对话（带上下文）

```python
import requests

BASE_URL = "http://localhost:8000"
session_id = "my-conversation"

# 第一轮
response1 = requests.post(
    f"{BASE_URL}/api/chat/repo",
    json={
        "repo_owner": "vuejs",
        "repo_name": "core",
        "question": "这个项目的目录结构是怎样的？",
        "session_id": session_id
    }
).json()
print("第一轮：", response1["answer"])

# 第二轮（基于上一轮的上下文）
response2 = requests.post(
    f"{BASE_URL}/api/chat/repo",
    json={
        "repo_owner": "vuejs",
        "repo_name": "core",
        "question": "那 compiler 目录下有什么？",
        "session_id": session_id
    }
).json()
print("第二轮：", response2["answer"])

# 查看完整历史
history = requests.get(f"{BASE_URL}/api/sessions/{session_id}").json()
print("完整对话历史：", history)
```

## 7. 错误处理

```python
import requests

try:
    response = requests.post(
        f"{BASE_URL}/api/chat/repo",
        json={
            "repo_owner": "non-existent",
            "repo_name": "repo",
            "question": "这是什么？"
        },
        timeout=60
    )
    response.raise_for_status()
    result = response.json()
    
    if "error" in result:
        print(f"Agent 错误: {result['error']}")
    else:
        print(f"答案: {result['answer']}")
        
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```
