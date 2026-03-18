#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版RAG知识库服务
基于关键词搜索的轻量级实现
"""

import os
import re
from pathlib import Path
from typing import List, Dict
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

class SimpleKnowledgeBase:
    """简化版知识库类"""
    
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.documents = []
        self.load_documents()
    
    def load_documents(self):
        """加载Markdown文档"""
        md_files = list(self.kb_path.glob("*.md"))
        
        print(f"📁 扫描知识库目录: {self.kb_path}")
        print(f"📄 找到 {len(md_files)} 个Markdown文件")
        
        for md_file in md_files:
            if md_file.name in ['PDF转换说明.md', '简单转换脚本.md', 'RAG系统使用指南.md']:
                continue
                
            try:
                print(f"📖 正在加载: {md_file.name}")
                
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 分割文档为段落
                sections = self.split_into_sections(content, md_file.name)
                self.documents.extend(sections)
                
                print(f"   ✅ 成功加载 {len(sections)} 个段落")
                
            except Exception as e:
                print(f"   ❌ 加载失败: {e}")
        
        print(f"\n📚 总共加载 {len(self.documents)} 个知识段落\n")
    
    def split_into_sections(self, content: str, filename: str) -> List[Dict]:
        """将文档分割为段落"""
        sections = []
        
        # 移除过短的无意义段落
        lines = content.split('\n')
        current_section = ""
        current_title = "引言"
        
        for line in lines:
            # 检测标题（支持# ## ###等）
            if line.strip().startswith('#'):
                # 保存当前段落（如果内容足够长）
                if len(current_section.strip()) > 50:
                    sections.append({
                        'title': current_title,
                        'content': current_section.strip(),
                        'source': filename.replace('.md', ''),
                        'text': f"{current_title}\n{current_section.strip()}"
                    })
                
                # 开始新段落
                current_title = line.lstrip('#').strip()
                current_section = ""
            else:
                current_section += line + "\n"
        
        # 保存最后一段
        if len(current_section.strip()) > 50:
            sections.append({
                'title': current_title,
                'content': current_section.strip(),
                'source': filename.replace('.md', ''),
                'text': f"{current_title}\n{current_section.strip()}"
            })
        
        return sections
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """关键词搜索"""
        query_words = set(query.lower().split())
        
        # 移除常见停用词
        stop_words = {'的', '是', '在', '有', '和', '与', '或', '等', '啊', '呢', '吗', '吧'}
        query_words = query_words - stop_words
        
        scored_docs = []
        
        for doc in self.documents:
            content = doc['text'].lower()
            title = doc['title'].lower()
            score = 0
            
            # 标题匹配权重更高
            for word in query_words:
                if word in title:
                    score += 5  # 标题匹配权重5
                if word in content:
                    score += content.count(word)  # 内容匹配权重1
            
            # 添加文档长度惩罚，避免过长的文档
            score = score / (len(doc['content']) / 1000 + 1)
            
            if score > 0:
                scored_docs.append({**doc, 'score': round(score, 2)})
        
        # 按分数排序
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        
        # 返回前top_k个结果
        return scored_docs[:top_k]


class SimpleRAGService:
    """简化版RAG服务"""
    
    def __init__(self, kb_path: str):
        print("🚀 初始化简化版RAG服务...")
        self.kb = SimpleKnowledgeBase(kb_path)
        print("✅ RAG服务初始化完成\n")
    
    def query(self, question: str) -> Dict:
        """查询知识库"""
        print(f"❓ 收到问题: {question}")
        
        # 搜索相关段落
        results = self.kb.search(question, top_k=3)
        
        if not results:
            print("⚠️  没有找到相关结果")
            return {
                'answer': '抱歉，在知识库中没有找到相关信息。建议您尝试其他关键词，比如：硬种、水解、发酵、割包等。',
                'source': '无匹配结果',
                'confidence': 0,
                'references': []
            }
        
        # 构建答案
        answer = self.build_answer(question, results)
        
        print(f"✅ 找到 {len(results)} 个相关结果")
        print(f"📖 最佳匹配来源: {results[0]['source']}")
        print(f"🎯 置信度: {results[0]['score']}\n")
        
        return {
            'answer': answer,
            'source': results[0]['source'],
            'confidence': results[0]['score'],
            'references': results
        }
    
    def build_answer(self, question: str, results: List[Dict]) -> str:
        """基于搜索结果构建答案"""
        best_result = results[0]
        
        # 清理内容
        content = best_result['content']
        
        # 移除多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 限制内容长度
        if len(content) > 800:
            content = content[:800] + '...'
        
        # 格式化为HTML
        content = content.replace('\n', '<br>')
        
        # 构建答案
        answer = f"<b>{best_result['title']}</b><br><br>"
        answer += content
        
        # 添加更多参考
        if len(results) > 1:
            answer += f"<br><br><small>📖 相关参考: {results[1]['title']}"
            if len(results) > 2:
                answer += f", {results[2]['title']}"
            answer += "</small>"
        
        return answer


# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化RAG服务
kb_path = r"e:\烘焙书籍\欧包制作\知识库md"
rag_service = None

def initialize_service():
    """初始化服务"""
    global rag_service
    try:
        rag_service = SimpleRAGService(kb_path)
        return True
    except Exception as e:
        print(f"❌ 服务初始化失败: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    if rag_service is None:
        return jsonify({'status': 'initializing', 'documents': 0}), 503
    
    return jsonify({
        'status': 'ok',
        'documents': len(rag_service.kb.documents),
        'service': 'simple_rag'
    })

@app.route('/api/query', methods=['POST'])
def query():
    """知识问答"""
    try:
        if rag_service is None:
            return jsonify({'error': '服务未初始化'}), 503
        
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': '请提供问题'}), 400
        
        result = rag_service.query(question)
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ 查询出错: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search():
    """知识搜索"""
    try:
        if rag_service is None:
            return jsonify({'error': '服务未初始化'}), 503
        
        data = request.json
        query = data.get('query', '')
        top_k = data.get('top_k', 5)
        
        results = rag_service.kb.search(query, top_k)
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    print("="*60)
    print("🍞 欧包知识库 - 简化版RAG服务")
    print("="*60)
    print()
    
    # 初始化服务
    if initialize_service():
        print("🌐 服务启动信息:")
        print("   本地访问: http://localhost:5000")
        print("   API端点:")
        print("     - GET  /api/health (健康检查)")
        print("     - POST /api/query (知识问答)")
        print("     - POST /api/search (知识搜索)")
        print()
        print("="*60)
        print("✅ 服务就绪，按 Ctrl+C 停止")
        print("="*60)
        print()
        
        # 启动Flask服务
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ 服务启动失败")
        input("按任意键退出...")
