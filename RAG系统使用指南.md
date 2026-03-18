# 欧包知识库RAG系统使用指南

## 🎯 系统概述

这是一个基于检索增强生成（RAG）技术的智能问答系统，能够基于您的烘焙知识库回答用户问题。

## 📁 文件结构

```
e:\烘焙书籍\欧包制作\
├── rag_service.py              # RAG服务主程序
├── rag_requirements.txt        # Python依赖
├── start_rag.bat              # 服务启动脚本
├── 知识库md/                   # Markdown知识库
│   ├── Tartine bread (...).md
│   ├── 如何驾驭开放式组织 (...).md
│   └── embeddings.npz         # 向量嵌入（自动生成）
├── 欧包计算器3.html           # 前端界面
└── deploy/
    └── index.html             # 部署版本
```

## 🚀 快速启动

### 方法1：一键启动（推荐）

1. **双击运行启动脚本**
   ```
   start_rag.bat
   ```

2. **等待服务启动**
   - 自动安装依赖
   - 加载知识库
   - 生成向量嵌入（首次运行需要几分钟）
   - 启动API服务

3. **验证服务状态**
   - 浏览器访问: http://localhost:5000/api/health
   - 应该看到: `{"status": "ok", "documents": X}`

### 方法2：手动启动

1. **安装依赖**
   ```bash
   pip install -r rag_requirements.txt
   ```

2. **启动服务**
   ```bash
   py rag_service.py
   ```

## 🔧 API接口

### 健康检查
```
GET http://localhost:5000/api/health
```

响应示例：
```json
{
  "status": "ok",
  "documents": 150
}
```

### 知识问答
```
POST http://localhost:5000/api/query
Content-Type: application/json

{
  "question": "如何制作硬种？"
}
```

响应示例：
```json
{
  "answer": "硬种（Stiff Starter）是含水量50%的酸种...",
  "source": "如何驾驭开放式组织 Open Crumb Mastery.md",
  "confidence": 0.85,
  "references": [...]
}
```

### 知识搜索
```
POST http://localhost:5000/api/search
Content-Type: application/json

{
  "query": "发酵",
  "top_k": 5
}
```

## 🌐 前端集成

### 在网页中使用

1. **确保RAG服务正在运行**
   ```bash
   # 检查服务状态
   curl http://localhost:5000/api/health
   ```

2. **打开欧包计算器**
   ```
   deploy/index.html
   ```

3. **使用问答功能**
   - 在知识库问答区域输入问题
   - 点击"提问"按钮
   - 查看基于真实知识库的答案

### API调用示例

```javascript
async function askQuestion(question) {
    try {
        const response = await fetch('http://localhost:5000/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });

        const data = await response.json();
        console.log('答案:', data.answer);
        console.log('来源:', data.source);
        console.log('置信度:', data.confidence);

    } catch (error) {
        console.error('API调用失败:', error);
    }
}

// 使用示例
askQuestion('如何制作硬种？');
```

## 📚 知识库管理

### 添加新知识

1. **将PDF转换为Markdown**
   - 使用Pandoc或其他工具
   - 放入`知识库md`文件夹

2. **重新生成向量嵌入**
   ```bash
   # 删除旧嵌入
   del 知识库md\embeddings.npz

   # 重启服务（自动生成新嵌入）
   start_rag.bat
   ```

### 更新知识库

1. **修改Markdown文件**
2. **删除旧嵌入**
3. **重启服务**

## 🔍 工作原理

### RAG流程

1. **用户提问** → 前端界面
2. **向量搜索** → 在知识库中查找相关段落
3. **答案构建** → 基于相关段落生成答案
4. **结果返回** → 显示答案和来源

### 两种搜索模式

**语义搜索（推荐）**
- 使用向量嵌入
- 理解语义相似性
- 需要安装: `sentence-transformers`

**关键词搜索**
- 基于关键词匹配
- 无需额外依赖
- 准确度较低

## ⚙️ 配置选项

### 修改API端口

编辑 `rag_service.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
# 改为其他端口，如:
app.run(host='0.0.0.0', port=8080, debug=True)
```

### 修改知识库路径

编辑 `rag_service.py`:
```python
kb_path = r"e:\烘焙书籍\欧包制作\知识库md"
# 改为您的路径
kb_path = r"D:\my\knowledge\base"
```

### 调整搜索结果数量

在前端调用时:
```javascript
// 在API中修改top_k参数
const response = await fetch('http://localhost:5000/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query: question,
        top_k: 5  // 返回前5个结果
    })
});
```

## 🐛 故障排除

### 问题1: 依赖安装失败

**解决方法:**
```bash
# 单独安装每个依赖
pip install flask
pip install flask-cors
pip install sentence-transformers
pip install numpy
```

### 问题2: 端口被占用

**解决方法:**
```bash
# 查找占用端口的进程
netstat -ano | findstr :5000

# 结束进程（替换PID）
taskkill /PID <进程ID> /F
```

### 问题3: 知识库加载失败

**检查:**
1. 知识库文件是否存在
2. 文件格式是否正确（UTF-8编码的Markdown）
3. 文件权限是否正确

### 问题4: 前端无法连接API

**检查:**
1. RAG服务是否正在运行
2. 端口是否正确
3. 浏览器控制台是否有错误信息
4. CORS是否正确配置

## 📊 性能优化

### 加速向量嵌入生成

- 使用GPU: `pip install sentence-transformers[gpu]`
- 减少文档大小
- 使用更小的模型

### 提升搜索速度

- 增加向量嵌入缓存
- 使用更快的相似度计算方法
- 限制搜索结果数量

## 🔐 安全建议

### 生产环境部署

1. **使用HTTPS**
2. **添加认证机制**
3. **限制访问频率**
4. **定期备份知识库**
5. **监控服务状态**

## 📈 扩展功能

### 添加更多知识来源

- 支持更多文档格式（PDF、EPUB、TXT）
- 连接在线知识库
- 整合网络搜索

### 增强答案质量

- 使用更强大的LLM
- 添加答案评分
- 支持多轮对话

### 改进用户体验

- 添加语音输入
- 支持多语言
- 提供相关问题推荐

---

## 🎉 开始使用

1. **启动RAG服务**: 双击 `start_rag.bat`
2. **打开计算器**: 在浏览器中打开 `deploy/index.html`
3. **开始提问**: 在知识库问答区域输入问题

享受您的智能烘焙知识库！🍞
