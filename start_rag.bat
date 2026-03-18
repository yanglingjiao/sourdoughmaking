@echo off
echo ========================================
echo 欧包知识库 RAG 服务启动器
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

REM 安装依赖
echo 📦 检查并安装依赖...
py -m pip install -r rag_requirements.txt --quiet
if errorlevel 1 (
    echo ⚠️ 依赖安装可能有问题，但继续尝试启动...
) else (
    echo ✅ 依赖安装完成
)
echo.

REM 启动RAG服务
echo 🚀 启动RAG服务...
echo.
py rag_service.py

pause
