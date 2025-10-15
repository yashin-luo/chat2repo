# Getting Started with Chat2Repo

## 🎯 What is Chat2Repo?

Chat2Repo is an intelligent chat application similar to GitHub Copilot Chat, designed for Gitee.com repositories. It uses AI agents to help you understand and explore open-source projects through natural language conversations.

## 🌟 Key Features

### 1. Repository Q&A
Chat with any Gitee repository:
- Automatically reads files and code
- Understands project structure
- Supports multi-turn conversations
- Provides accurate answers based on actual code

### 2. Tech Solution Search
Get open-source solutions for technical problems:
- Searches Gitee for relevant projects
- Evaluates project quality
- Recommends 2-5 best solutions
- Analyzes pros and cons of each solution

## 🚀 Quick Start (3 Steps)

### Step 1: Configure Environment

```bash
# Copy the example config
cp .env.example .env

# Edit .env and add your keys
OPENAI_API_KEY=sk-your-openai-key
GITEE_ACCESS_TOKEN=your-gitee-token
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python main.py
```

That's it! The service is now running at http://localhost:8000

## 💬 Your First Chat

### Option 1: Use the CLI Tool

```bash
python cli.py interactive
```

Then in the interactive mode:
```
> repo dromara hutool
> What is this project about?
```

### Option 2: Use the API

```bash
curl -X POST http://localhost:8000/api/chat/repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "dromara",
    "repo_name": "hutool",
    "question": "What is this project about?"
  }'
```

### Option 3: Use the API Documentation

Visit http://localhost:8000/docs to see the interactive API documentation.

## 📚 Example Conversations

### Example 1: Understanding a Project

```
You: What language is this project written in?
Agent: [Calls get_repo_info]
      This is a Java project with 5000+ stars...

You: What are the main modules?
Agent: [Calls list_directory and get_readme]
      The main modules are...
```

### Example 2: Finding Solutions

```
You: Recommend some Java utility libraries
Agent: [Searches Gitee]
      I found these excellent projects:
      1. Hutool - A comprehensive Java utility library...
      2. ...
```

## 🛠️ How It Works

```
User Question
    ↓
FastAPI API
    ↓
Agent (RepoAgent or SearchAgent)
    ↓
LLM decides what tools to use
    ↓
Tools execute (read files, search, etc.)
    ↓
LLM generates answer
    ↓
Return to user
```

## 📖 What's Next?

- [Detailed Examples](examples.md) - More usage examples
- [Development Guide](DEVELOPMENT.md) - For developers
- [Architecture](ARCHITECTURE.md) - System design
- [API Reference](http://localhost:8000/docs) - After starting the service

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Config error"
**Solution**: Check your .env file
```bash
# Make sure these are set
OPENAI_API_KEY=sk-...
GITEE_ACCESS_TOKEN=...
```

### Issue: "Gitee API error"
**Solution**: Verify your Gitee token at https://gitee.com/profile/personal_access_tokens

## 🎉 You're Ready!

Start exploring Gitee repositories with natural language! 

For more details, see [QUICKSTART.md](QUICKSTART.md).
