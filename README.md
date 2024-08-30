# SAI-API服务工具🤖

该工具是一个简单的SAI代理服务，允许用户通过填写请求头的CA值来访问代理的AI API服务。

## 特性😎

- **简单易用🐨**: 只需填写请求头中的CA值，即可访问代理的AI API服务。
- **开源🤩**: 完全开源，您可以自由地修改和定制。
- **灵活性🫥**: 支持多种类型的AI API服务代理。
- **安全性😶‍🌫️**: 通过请求头中的CA值确保访问安全性。

## 使用方法

### 安装
#### 使用pip一个个输入安装（rz室长@Lt2023写的方法）

1. 克隆本仓库：

   ```bash
   git clone https://github.com/Lt2023/LLSA
   ```

2. 配置

   ```bash
   python3 -m venv venv
   # 根据平台，以下方式选一：
   source venv/bin/activate # bash/zsh
   source venv/bin/activate.fish # fish
   source venv/bin/activate.csh # csh/tcsh
   .\venv\Scripts\activate.bat # CMD
   .\venv\Scripts\activate.ps1 # PowerShell
   pip install requests flaskAPI
   ```

#### pip安装

1. 克隆本仓库
   ```bash
   git clone https://github.com/Lt2023/LLSA
   ```
2. 配置
   ```bash
   pip install -r requirements.txt
   ```
> [!WARNING]  
> 如果你遇到了`安装异常`，请及时反馈Issue!谢谢

### 配置[带有*号的必须配置，否则导致]
> 配置文件默认路径：`Config.json`

#### *CA 配置
打开`config.json`,修改`ca`项

#### 端口配置
打开`config.json`,修改`Port`项
> [!WARNING]
> 数字一定要是int！！！

### 运行

``` bash
python3 AI.py
```
或者：
``` bash
python AI.py
```

### 贡献

🤩欢迎提交问题和建议，您可以通过以下方式贡献：

提交问题: Issue Tracker

提交代码: Pull Requests
