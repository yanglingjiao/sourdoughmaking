#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的Flask测试服务
"""

try:
    from flask import Flask, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok', 'message': 'RAG服务运行中'})
    
    @app.route('/api/query', methods=['POST'])
    def query():
        from flask import request
        data = request.json
        question = data.get('question', '')
        
        # 简单的关键词响应
        if '硬种' in question or 'stiff' in question.lower():
            answer = '硬种（Stiff Starter）是含水量50%的酸种。制作要点：比例1:2:1（老酵头:粉:水），发酵温度26-28°C，至体积2.5倍。'
        elif '水解' in question or 'autolyse' in question.lower():
            answer = '水解是让面粉充分吸水的过程。高筋面粉建议60分钟，中筋面粉30分钟。水解时不要放盐和酵头。'
        elif '发酵' in question or 'proof' in question.lower():
            answer = '发酵判断：体积增加50-70%，指压测试按下后缓慢回弹一半。目标面温24-26°C。'
        else:
            answer = f'您的问题：{question}。这是演示回答。真实RAG服务启动后将提供基于知识库的详细答案。'
        
        return jsonify({
            'answer': answer,
            'source': '演示模式',
            'confidence': 0.8
        })
    
    print("🚀 启动测试RAG服务...")
    print("🌐 访问地址: http://localhost:5000")
    print("✅ 服务就绪\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请运行: pip install flask flask-cors")
    input("按任意键退出...")
except Exception as e:
    print(f"❌ 启动失败: {e}")
    input("按任意键退出...")
