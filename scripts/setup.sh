#!/bin/bash

# 克隆仓库
git clone https://github.com/Lt2023/LLSA
cd LLSA

# 创建虚拟环境
python3 -m venv venv

# 检测当前的 shell 并激活虚拟环境
case "$SHELL" in
  */bash)
    source venv/bin/activate
    ;;
  */zsh)
    source venv/bin/activate
    ;;
  */fish)
    source venv/bin/activate.fish
    ;;
  */csh)
    source venv/bin/activate.csh
    ;;
  */tcsh)
    source venv/bin/activate.csh
    ;;
  *)
    echo "Unsupported shell: $SHELL. Please activate the virtual environment manually."
    exit 1
    ;;
esac

# 安装依赖
pip install -r requirements.txt

echo "安装完成。要退出虚拟环境，请运行 'deactivate'。"
