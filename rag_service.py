#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RAG知识库服务
基于Markdown文件的检索增强生成系统
"""

import os
import re
from pathlib import Path
from typing import List, Dict
import json

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_EMBEDDING = True
except ImportError:
    HAS_EMBEDDING = False
    print("⚠️ 警告: 未安装embedding库，将使用基础搜索模式")
    print("安装命令: pip install sentence-transformers numpy")


class KnowledgeBase:
    """知识库类"""
    
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.documents = []
        self.embeddings = None
        self.model = None
        self.load_documents()
        
        if HAS_EMBEDDING:
            self.load_embeddings()
    
    def load_documents(self):
        """加载Markdown文档"""
        md_files = list(self.kb_path.glob("*.md"))
        
        for md_file in md_files:
            if md_file.name in ['PDF转换说明.md', '简单转换脚本.md']:
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 分割文档为段落
                sections = self.split_into_sections(content, md_file.name)
                self.documents.extend(sections)
                
                print(f"✅ 加载: {md_file.name} ({len(sections)} 个段落)")
                
            except Exception as e:
                print(f"❌ 加载失败 {md_file.name}: {e}")
        
        print(f"\n📚 总共加载 {len(self.documents)} 个知识段落")
    
    def split_into_sections(self, content: str, filename: str) -> List[Dict]:
        """将文档分割为段落"""
        sections = []
        
        # 按标题分割
        lines = content.split('\n')
        current_section = ""
        current_title = "引言"
        
        for line in lines:
            if line.startswith('#'):
                # 保存当前段落
                if current_section.strip():
                    sections.append({
                        'title': current_title,
                        'content': current_section.strip(),
                        'source': filename,
                        'text': f"{current_title}\n{current_section.strip()}"
                    })
                
                # 开始新段落
                current_title = line.lstrip('#').strip()
                current_section = ""
            else:
                current_section += line + "\n"
        
        # 保存最后一段
        if current_section.strip():
            sections.append({
                'title': current_title,
                'content': current_section.strip(),
                'source': filename,
                'text': f"{current_title}\n{current_section.strip()}"
            })
        
        return sections
    
    def load_embeddings(self):
        """加载或创建向量嵌入"""
        embedding_file = self.kb_path / "embeddings.npz"
        
        if embedding_file.exists():
            # 加载已有嵌入
            data = np.load(embedding_file, allow_pickle=True)
            self.embeddings = data['embeddings']
            print(f"✅ 加载已有向量嵌入 ({len(self.embeddings)} 个向量)")
        else:
            # 创建新嵌入
            print("🔄 正在创建向量嵌入...")
            self.create_embeddings()
    
    def create_embeddings(self):
        """创建向量嵌入"""
        try:
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            
            texts = [doc['text'] for doc in self.documents]
            self.embeddings = self.model.encode(texts, show_progress_bar=True)
            
            # 保存嵌入
            embedding_file = self.kb_path / "embeddings.npz"
            np.savez(embedding_file, embeddings=self.embeddings)
            print(f"✅ 向量嵌入已保存")
            
        except Exception as e:
            print(f"❌ 创建嵌入失败: {e}")
            self.embeddings = None
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """搜索相关段落"""
        if HAS_EMBEDDING and self.embeddings is not None:
            return self.semantic_search(query, top_k)
        else:
            return self.keyword_search(query, top_k)
    
    def semantic_search(self, query: str, top_k: int) -> List[Dict]:
        """语义搜索"""
        try:
            query_embedding = self.model.encode([query])
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
            
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                results.append({
                    **self.documents[idx],
                    'score': float(similarities[idx])
                })
            
            return results
            
        except Exception as e:
            print(f"❌ 语义搜索失败: {e}")
            return self.keyword_search(query, top_k)
    
    def keyword_search(self, query: str, top_k: int) -> List[Dict]:
        """关键词搜索"""
        query_words = set(query.lower().split())
        
        scored_docs = []
        for doc in self.documents:
            content = doc['text'].lower()
            score = 0
            
            for word in query_words:
                if word in content:
                    score += content.count(word)
            
            if score > 0:
                scored_docs.append({**doc, 'score': score})
        
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]


class RAGService:
    """RAG服务类"""
    
    def __init__(self, kb_path: str):
        self.kb = KnowledgeBase(kb_path)
    
    def query(self, question: str) -> Dict:
        """查询知识库"""
        # 搜索相关段落
        results = self.kb.search(question, top_k=3)
        
        if not results:
            return {
                'answer': '抱歉，在知识库中没有找到相关信息。建议您尝试其他关键词或查看相关书籍。',
                'source': '无匹配结果',
                'confidence': 0
            }
        
        # 构建答案
        answer = self.build_answer(question, results)
        
        return {
            'answer': answer,
            'source': results[0]['source'],
            'confidence': results[0]['score'],
            'references': results
        }
    
    def build_answer(self, question: str, results: List[Dict]) -> str:
        """基于搜索结果构建答案"""
        # 简单策略：返回最相关段落
        best_result = results[0]
        
        answer = f"<b>{best_result['title']}</b><br><br>"
        
        # 清理内容
        content = best_result['content']
        content = re.sub(r'\n+', '<br>', content)
        content = content[:500] + '...' if len(content) > 500 else content
        
        answer += content
        
        # 如果有其他相关结果，添加参考
        if len(results) > 1:
            answer += f"<br><br><small>📖 参考: {results[1]['title']}</small>"
        
        return answer


# Flask API服务
def create_api():
    """创建Flask API服务"""
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        # 初始化RAG服务
        kb_path = r"e:\烘焙书籍\欧包制作\知识库md"
        rag_service = RAGService(kb_path)
        
        @app.route('/api/health', methods=['GET'])
        def health():
            return jsonify({'status': 'ok', 'documents': len(rag_service.kb.documents)})
        
        @app.route('/api/query', methods=['POST'])
        def query():
            try:
                data = request.json
                question = data.get('question', '')
                
                if not question:
                    return jsonify({'error': '请提供问题'}), 400
                
                result = rag_service.query(question)
                return jsonify(result)
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @app.route('/api/search', methods=['POST'])
        def search():
            try:
                data = request.json
                query = data.get('query', '')
                top_k = data.get('top_k', 5)
                
                results = rag_service.kb.search(query, top_k)
                return jsonify({'results': results})
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        return app
        
    except ImportError:
        print("❌ 请先安装Flask: pip install flask flask-cors")
        return None


if __name__ == "__main__":
    # 测试知识库
    kb_path = r"e:\烘焙书籍\欧包制作\知识库md"
    rag = RAGService(kb_path)
    
    # 测试查询
    print("\n" + "="*50)
    print("🔍 测试知识库查询")
    print("="*50)
    
    test_questions = [
        "如何制作硬种",
        "什么是水解",
        "发酵时间",
        "割包技巧"
    ]
    
    for question in test_questions:
        print(f"\n❓ 问题: {question}")
        result = rag.query(question)
        print(f"📖 来源: {result['source']}")
        print(f"🎯 置信度: {result['confidence']:.2f}")
        print(f"📝 答案预览: {result['answer'][:100]}...")
    
    # 启动API服务
    print("\n" + "="*50)
    print("🚀 启动RAG API服务")
    print("="*50)
    
    app = create_api()
    if app:
        print("✅ API服务已就绪")
        print("🌐 访问地址: http://localhost:5000")
        print("📡 API端点:")
        print("   - GET  /api/health")
        print("   - POST /api/query")
        print("   - POST /api/search")
        
        app.run(host='0.0.0.0', port=5000, debug=True)
