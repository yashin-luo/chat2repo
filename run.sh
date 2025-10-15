#!/bin/bash

# Chat2Repo 启动脚本

echo "================================"
echo "Chat2Repo - Gitee Repository Chat Agent"
echo "================================"

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python 版本: $PYTHON_VERSION"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo ""
    echo "警告: 未找到 .env 文件"
    echo "请从 .env.example 复制并配置："
    echo "  cp .env.example .env"
    echo "  # 然后编辑 .env 文件填入您的配置"
    exit 1
fi

# 检查必要的环境变量
source .env
if [ -z "$OPENAI_API_KEY" ]; then
    echo "错误: 未设置 OPENAI_API_KEY"
    exit 1
fi

if [ -z "$GITEE_ACCESS_TOKEN" ]; then
    echo "错误: 未设置 GITEE_ACCESS_TOKEN"
    exit 1
fi

echo "配置检查通过 ✓"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "虚拟环境创建完成 ✓"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "依赖安装完成 ✓"
echo ""

# 启动服务
echo "================================"
echo "启动服务..."
echo "API 文档: http://localhost:${PORT:-8000}/docs"
echo "================================"
echo ""

python main.py
