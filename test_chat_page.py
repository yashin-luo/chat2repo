#!/usr/bin/env python3
"""
简单的测试脚本，验证聊天页面的静态资源是否正确加载
"""
import os
import sys

def test_static_files():
    """测试静态文件是否存在"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    
    required_files = [
        "index.html",
        "chat.html",
        "chat.css",
        "chat.js",
        "style.css",
        "README.md"
    ]
    
    print("检查静态文件...")
    all_exist = True
    
    for filename in required_files:
        filepath = os.path.join(static_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ {filename} ({size} bytes)")
        else:
            print(f"✗ {filename} 不存在")
            all_exist = False
    
    return all_exist

def test_html_content():
    """测试 HTML 文件是否包含必要的内容"""
    print("\n检查聊天页面内容...")
    
    chat_html = os.path.join(os.path.dirname(__file__), "static", "chat.html")
    with open(chat_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_elements = [
        'chat-container',  # 主容器
        'chat-sidebar',    # 侧边栏
        'mode-btn',        # 模式按钮
        'message-list',    # 消息列表
        'chat-input',      # 输入框
        'chat.css',        # 样式引用
        'chat.js',         # 脚本引用
    ]
    
    all_present = True
    for element in required_elements:
        if element in content:
            print(f"✓ 包含 {element}")
        else:
            print(f"✗ 缺少 {element}")
            all_present = False
    
    return all_present

def test_api_endpoints():
    """检查 main.py 中的 API 端点是否定义"""
    print("\n检查 API 端点...")
    
    main_py = os.path.join(os.path.dirname(__file__), "main.py")
    with open(main_py, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_endpoints = [
        '/api/chat/repo',
        '/api/chat/tech',
        '/api/sessions',
    ]
    
    all_defined = True
    for endpoint in required_endpoints:
        if endpoint in content:
            print(f"✓ 定义了 {endpoint}")
        else:
            print(f"✗ 缺少 {endpoint}")
            all_defined = False
    
    return all_defined

def main():
    print("=" * 50)
    print("Chat2Repo 聊天页面测试")
    print("=" * 50)
    
    results = []
    
    # 测试静态文件
    results.append(test_static_files())
    
    # 测试 HTML 内容
    results.append(test_html_content())
    
    # 测试 API 端点
    results.append(test_api_endpoints())
    
    # 总结
    print("\n" + "=" * 50)
    if all(results):
        print("✓ 所有测试通过！聊天页面已正确配置。")
        print("\n启动服务器后，访问:")
        print("  http://localhost:8000/static/chat.html")
        return 0
    else:
        print("✗ 部分测试失败，请检查上述错误。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
