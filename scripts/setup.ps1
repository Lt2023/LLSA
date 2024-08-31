# 克隆仓库
git clone https://github.com/Lt2023/LLSA
cd LLSA

# 创建并激活虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

Write-Host "安装完成。要退出虚拟环境，请运行 deactivate。"
