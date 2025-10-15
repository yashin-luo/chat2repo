// Chat2Repo 聊天界面交互逻辑

class ChatApp {
    constructor() {
        this.currentMode = 'tech'; // 'tech' 或 'repo'
        this.currentSessionId = null;
        this.messages = [];
        this.isLoading = false;

        this.initElements();
        this.bindEvents();
        this.loadSessions();
    }

    initElements() {
        // 模式选择
        this.modeBtns = document.querySelectorAll('.mode-btn');
        this.repoConfig = document.getElementById('repo-config');
        this.languageConfig = document.getElementById('language-config');

        // 输入元素
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.repoOwner = document.getElementById('repo-owner');
        this.repoName = document.getElementById('repo-name');
        this.repoRef = document.getElementById('repo-ref');
        this.languageSelect = document.getElementById('language-select');

        // 显示区域
        this.welcomeScreen = document.getElementById('welcome-screen');
        this.messageList = document.getElementById('message-list');
        this.sessionList = document.getElementById('session-list');

        // 按钮
        this.newChatBtn = document.getElementById('new-chat-btn');
    }

    bindEvents() {
        // 模式切换
        this.modeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const mode = btn.dataset.mode;
                this.switchMode(mode);
            });
        });

        // 发送消息
        this.sendBtn.addEventListener('click', () => {
            this.sendMessage();
        });

        // 输入框事件
        this.chatInput.addEventListener('input', () => {
            this.updateSendButton();
            this.autoResize();
        });

        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!this.sendBtn.disabled) {
                    this.sendMessage();
                }
            }
        });

        // 示例问题点击
        document.querySelectorAll('.example-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const example = btn.dataset.example;
                this.chatInput.value = example;
                this.updateSendButton();
                this.chatInput.focus();
            });
        });

        // 新建对话
        this.newChatBtn.addEventListener('click', () => {
            this.newChat();
        });
    }

    switchMode(mode) {
        this.currentMode = mode;

        // 更新按钮状态
        this.modeBtns.forEach(btn => {
            if (btn.dataset.mode === mode) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // 显示/隐藏相应配置
        if (mode === 'repo') {
            this.repoConfig.style.display = 'block';
            this.languageConfig.style.display = 'none';
        } else {
            this.repoConfig.style.display = 'none';
            this.languageConfig.style.display = 'block';
        }
    }

    updateSendButton() {
        const hasText = this.chatInput.value.trim().length > 0;
        this.sendBtn.disabled = !hasText || this.isLoading;
    }

    autoResize() {
        this.chatInput.style.height = 'auto';
        this.chatInput.style.height = this.chatInput.scrollHeight + 'px';
    }

    async sendMessage() {
        const question = this.chatInput.value.trim();
        if (!question || this.isLoading) return;

        // 隐藏欢迎界面，显示消息列表
        if (this.welcomeScreen.style.display !== 'none') {
            this.welcomeScreen.style.display = 'none';
            this.messageList.style.display = 'flex';
        }

        // 添加用户消息
        this.addMessage('user', question);

        // 清空输入框
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        this.updateSendButton();

        // 显示加载状态
        this.isLoading = true;
        const loadingId = this.addLoadingMessage();

        try {
            let response;
            if (this.currentMode === 'tech') {
                response = await this.sendTechQuestion(question);
            } else {
                response = await this.sendRepoQuestion(question);
            }

            // 移除加载消息
            this.removeMessage(loadingId);

            // 添加助手回复
            this.addMessage('assistant', response.answer, response.tool_calls);

            // 更新会话ID
            if (response.session_id) {
                this.currentSessionId = response.session_id;
                this.loadSessions();
            }
        } catch (error) {
            // 移除加载消息
            this.removeMessage(loadingId);

            // 显示错误
            this.addMessage('assistant', `抱歉，处理您的请求时出现错误：${error.message}`);
        } finally {
            this.isLoading = false;
            this.updateSendButton();
        }
    }

    async sendTechQuestion(question) {
        const language = this.languageSelect.value;
        
        const response = await fetch('/api/chat/tech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                language: language || undefined,
                session_id: this.currentSessionId
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '请求失败');
        }

        return await response.json();
    }

    async sendRepoQuestion(question) {
        const owner = this.repoOwner.value.trim();
        const name = this.repoName.value.trim();
        const ref = this.repoRef.value.trim();

        if (!owner || !name) {
            throw new Error('请填写仓库所有者和仓库名称');
        }

        const response = await fetch('/api/chat/repo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                repo_owner: owner,
                repo_name: name,
                question: question,
                ref: ref || undefined,
                session_id: this.currentSessionId
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '请求失败');
        }

        return await response.json();
    }

    addMessage(role, content, toolCalls = null) {
        const messageId = Date.now();
        const message = { id: messageId, role, content, toolCalls, time: new Date() };
        this.messages.push(message);

        const messageEl = this.createMessageElement(message);
        this.messageList.appendChild(messageEl);

        // 滚动到底部
        this.scrollToBottom();

        return messageId;
    }

    addLoadingMessage() {
        const messageId = Date.now();
        const message = { id: messageId, role: 'assistant', loading: true };
        this.messages.push(message);

        const messageEl = this.createLoadingElement(message);
        this.messageList.appendChild(messageEl);

        // 滚动到底部
        this.scrollToBottom();

        return messageId;
    }

    removeMessage(messageId) {
        const index = this.messages.findIndex(m => m.id === messageId);
        if (index !== -1) {
            this.messages.splice(index, 1);
        }

        const messageEl = this.messageList.querySelector(`[data-message-id="${messageId}"]`);
        if (messageEl) {
            messageEl.remove();
        }
    }

    createMessageElement(message) {
        const messageEl = document.createElement('div');
        messageEl.className = `message ${message.role}`;
        messageEl.dataset.messageId = message.id;

        const avatar = message.role === 'user' ? '👤' : '🤖';
        
        let toolCallsHtml = '';
        if (message.toolCalls && message.toolCalls.length > 0) {
            const toolCallsList = message.toolCalls.map(tc => {
                return `<div class="tool-call-item">🔧 ${tc.tool}: ${tc.args}</div>`;
            }).join('');
            toolCallsHtml = `<div class="tool-calls">${toolCallsList}</div>`;
        }

        messageEl.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-bubble">${this.formatMessage(message.content)}</div>
                ${toolCallsHtml}
                <div class="message-time">${this.formatTime(message.time)}</div>
            </div>
        `;

        return messageEl;
    }

    createLoadingElement(message) {
        const messageEl = document.createElement('div');
        messageEl.className = 'message assistant loading';
        messageEl.dataset.messageId = message.id;

        messageEl.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;

        return messageEl;
    }

    formatMessage(content) {
        // 简单的 Markdown 格式化
        let formatted = content;

        // 代码块
        formatted = formatted.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><code>${this.escapeHtml(code.trim())}</code></pre>`;
        });

        // 行内代码
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

        // 链接
        formatted = formatted.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // 粗体
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // 换行
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatTime(date) {
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) { // 小于1分钟
            return '刚刚';
        } else if (diff < 3600000) { // 小于1小时
            return Math.floor(diff / 60000) + ' 分钟前';
        } else if (diff < 86400000) { // 小于1天
            return Math.floor(diff / 3600000) + ' 小时前';
        } else {
            return date.toLocaleString('zh-CN', { 
                month: 'numeric', 
                day: 'numeric', 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.messageList.scrollTop = this.messageList.scrollHeight;
        }, 100);
    }

    async loadSessions() {
        try {
            const response = await fetch('/api/sessions');
            if (!response.ok) return;

            const data = await response.json();
            this.renderSessions(data.sessions);
        } catch (error) {
            console.error('加载会话列表失败:', error);
        }
    }

    renderSessions(sessions) {
        if (!sessions || sessions.length === 0) {
            this.sessionList.innerHTML = '<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">暂无历史会话</div>';
            return;
        }

        this.sessionList.innerHTML = sessions.map(session => {
            const isActive = session.session_id === this.currentSessionId;
            const date = new Date(session.updated_at);
            return `
                <div class="session-item ${isActive ? 'active' : ''}" data-session-id="${session.session_id}">
                    <div class="session-title">对话 - ${session.message_count / 2} 轮</div>
                    <div class="session-meta">${this.formatTime(date)}</div>
                </div>
            `;
        }).join('');

        // 绑定点击事件
        this.sessionList.querySelectorAll('.session-item').forEach(item => {
            item.addEventListener('click', () => {
                const sessionId = item.dataset.sessionId;
                this.loadSession(sessionId);
            });
        });
    }

    async loadSession(sessionId) {
        try {
            const response = await fetch(`/api/sessions/${sessionId}`);
            if (!response.ok) return;

            const session = await response.json();
            
            // 清空当前消息
            this.messages = [];
            this.messageList.innerHTML = '';
            
            // 显示消息列表
            this.welcomeScreen.style.display = 'none';
            this.messageList.style.display = 'flex';

            // 恢复消息
            session.messages.forEach(msg => {
                this.addMessage(msg.role, msg.content);
            });

            // 更新当前会话ID
            this.currentSessionId = sessionId;

            // 更新会话列表样式
            this.sessionList.querySelectorAll('.session-item').forEach(item => {
                if (item.dataset.sessionId === sessionId) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        } catch (error) {
            console.error('加载会话失败:', error);
        }
    }

    newChat() {
        // 清空状态
        this.currentSessionId = null;
        this.messages = [];
        this.messageList.innerHTML = '';
        
        // 显示欢迎界面
        this.welcomeScreen.style.display = 'flex';
        this.messageList.style.display = 'none';

        // 清空会话列表的激活状态
        this.sessionList.querySelectorAll('.session-item').forEach(item => {
            item.classList.remove('active');
        });

        // 清空输入框
        this.chatInput.value = '';
        this.updateSendButton();
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
