@echo off

:: 克隆仓库
git clone https://github.com/Lt2023/LLSA
cd LLSA

:: 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate.bat

:: 安装依赖
pip install -r requirements.txt

echo 安装完成。要退出虚拟环境，请运行 deactivate。
pause
