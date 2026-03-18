@echo off
echo ========================================
echo 欧包知识库 RAG 服务（简化版）
echo ========================================
echo.

REM 检查Python环境
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python环境
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境检测通过
echo.

REM 进入项目目录
cd /d "%~dp0"

REM 检查Flask是否安装
py -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 正在安装依赖...
    py -m pip install flask flask-cors --quiet
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
    echo.
) else (
    echo ✅ Flask已安装
    echo.
)

REM 检查知识库目录
if not exist "知识库md" (
    echo ❌ 错误: 知识库目录不存在
    echo 请确保知识库md文件夹存在且包含Markdown文件
    pause
    exit /b 1
)

echo 📚 知识库目录检查通过
echo.

REM 启动RAG服务
echo 🚀 启动RAG服务...
echo.
py simple_rag_service.py

if errorlevel 1 (
    echo.
    echo ❌ 服务运行出错
    pause
)
