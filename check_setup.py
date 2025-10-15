#!/usr/bin/env python3
"""
项目配置检查脚本
检查所有依赖和配置是否正确
"""
import sys
import os


def check_imports():
    """检查所有必需的模块是否可以导入"""
    print("=" * 60)
    print("检查 Python 模块导入...")
    print("=" * 60)
    
    modules = [
        ("FastAPI", "fastapi"),
        ("Uvicorn", "uvicorn"),
        ("Pydantic", "pydantic"),
        ("Pydantic Settings", "pydantic_settings"),
        ("HTTPX", "httpx"),
        ("OpenAI", "openai"),
        ("Python-dotenv", "dotenv"),
        ("Tiktoken", "tiktoken"),
        ("Tenacity", "tenacity"),
    ]
    
    failed = []
    for name, module in modules:
        try:
            __import__(module)
            print(f"✅ {name:20s} - 已安装")
        except ImportError as e:
            print(f"❌ {name:20s} - 未安装")
            failed.append(name)
    
    print()
    
    if failed:
        print(f"❌ 缺少模块: {', '.join(failed)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖已安装")
    return True


def check_project_modules():
    """检查项目自身的模块"""
    print("\n" + "=" * 60)
    print("检查项目模块...")
    print("=" * 60)
    
    modules = [
        ("配置管理", "config"),
        ("Gitee 客户端", "gitee_client"),
        ("LLM 客户端", "llm_client"),
        ("数据模型", "models"),
        ("工具集", "tools"),
        ("Agent 基类", "agents.base_agent"),
        ("仓库 Agent", "agents.repo_agent"),
        ("搜索 Agent", "agents.search_agent"),
    ]
    
    failed = []
    for name, module in modules:
        try:
            __import__(module)
            print(f"✅ {name:20s} - OK")
        except Exception as e:
            print(f"❌ {name:20s} - 错误: {e}")
            failed.append(name)
    
    print()
    
    if failed:
        print(f"❌ 模块导入失败: {', '.join(failed)}")
        return False
    
    print("✅ 所有项目模块正常")
    return True


def check_files():
    """检查必需的文件是否存在"""
    print("\n" + "=" * 60)
    print("检查项目文件...")
    print("=" * 60)
    
    files = [
        ("主应用", "main.py"),
        ("配置示例", ".env.example"),
        ("依赖列表", "requirements.txt"),
        ("README", "README.md"),
        ("启动脚本", "run.sh"),
        ("CLI 工具", "cli.py"),
        ("测试客户端", "test_client.py"),
        ("Git 忽略", ".gitignore"),
        ("Dockerfile", "Dockerfile"),
        ("Docker Compose", "docker-compose.yml"),
    ]
    
    missing = []
    for name, file in files:
        if os.path.exists(file):
            print(f"✅ {name:20s} - {file}")
        else:
            print(f"❌ {name:20s} - {file} (不存在)")
            missing.append(file)
    
    print()
    
    if missing:
        print(f"❌ 缺少文件: {', '.join(missing)}")
        return False
    
    print("✅ 所有必需文件存在")
    return True


def check_env():
    """检查环境变量配置"""
    print("\n" + "=" * 60)
    print("检查环境变量配置...")
    print("=" * 60)
    
    # 尝试加载 .env 文件
    if os.path.exists(".env"):
        print("✅ .env 文件存在")
        
        # 尝试加载配置
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            required_vars = [
                "OPENAI_API_KEY",
                "GITEE_ACCESS_TOKEN",
            ]
            
            missing = []
            for var in required_vars:
                value = os.getenv(var)
                if value:
                    # 隐藏实际值，只显示前几个字符
                    masked = value[:8] + "..." if len(value) > 8 else "***"
                    print(f"✅ {var:25s} - {masked}")
                else:
                    print(f"❌ {var:25s} - 未设置")
                    missing.append(var)
            
            print()
            
            if missing:
                print(f"❌ 缺少必需的环境变量: {', '.join(missing)}")
                print("\n请在 .env 文件中配置这些变量：")
                for var in missing:
                    print(f"  {var}=your_value_here")
                return False
            
            print("✅ 所有必需的环境变量已配置")
            return True
            
        except Exception as e:
            print(f"❌ 加载 .env 文件失败: {e}")
            return False
    else:
        print("⚠️  .env 文件不存在")
        print("\n请从 .env.example 复制并配置：")
        print("  cp .env.example .env")
        print("  # 然后编辑 .env 文件")
        return False


def check_main_app():
    """检查主应用是否可以导入"""
    print("\n" + "=" * 60)
    print("检查主应用...")
    print("=" * 60)
    
    try:
        # 尝试导入主应用
        import main
        print("✅ main.py 可以导入")
        
        # 检查 app 对象
        if hasattr(main, 'app'):
            print("✅ FastAPI app 对象存在")
        else:
            print("❌ FastAPI app 对象不存在")
            return False
        
        print("✅ 主应用配置正确")
        return True
        
    except Exception as e:
        print(f"❌ 导入主应用失败: {e}")
        return False


def print_summary(results):
    """打印检查摘要"""
    print("\n" + "=" * 60)
    print("检查摘要")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{check:20s} - {status}")
    
    print()
    
    if all_passed:
        print("🎉 所有检查通过！项目已准备就绪。")
        print("\n下一步:")
        print("  1. 启动服务: python main.py")
        print("  2. 或使用脚本: ./run.sh")
        print("  3. 访问 API 文档: http://localhost:8000/docs")
        print("  4. 使用 CLI 工具: python cli.py interactive")
        return True
    else:
        print("❌ 部分检查失败，请修复上述问题后重试。")
        return False


def main():
    """主函数"""
    print("\nChat2Repo 项目配置检查")
    print("=" * 60)
    print()
    
    results = {
        "Python 依赖": check_imports(),
        "项目模块": check_project_modules(),
        "项目文件": check_files(),
        "环境变量": check_env(),
        "主应用": check_main_app(),
    }
    
    success = print_summary(results)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
