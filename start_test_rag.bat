@echo off
echo ========================================
echo 欧包知识库 RAG 测试服务
echo ========================================
echo.

cd /d "%~dp0"

REM 检查并安装依赖
echo 📦 检查依赖...
py -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 正在安装Flask...
    py -m pip install flask flask-cors
)

echo ✅ 依赖检查完成
echo.

echo 🚀 启动测试RAG服务...
echo.
py test_flask.py

pause
