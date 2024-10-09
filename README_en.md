# SAI-API Service Tool 🤖

This tool is a simple SAI proxy service that allows users to access the proxy's AI API service by filling in the CA value of the request header.

## Characteristics 😎

-* * Easy to use 🐨**:  Simply fill in the CA value in the request header to access the AI API service of the proxy.
-* * Open source 🤩**:  Completely open source, you can freely modify and customize.
-Flexibility: Supports multiple types of AI API service proxies.
-* * Security 😶 ‍ 🌫️**:  Ensure access security by using the CA value in the request header.

## Usage method

### Installation
#### Install manually through pip
1. Clone this repository:

```bash
git clone  https://github.com/Lt2023/LLSA
```

2. Configuration

```bash
python3 -m venv venv
#According to the platform, choose one of the following methods:
source venv/bin/activate # bash/zsh
source venv/bin/activate.fish # fish
source venv/bin/activate.csh # csh/tcsh
.\venv\Scripts\activate.bat # CMD
.\venv\Scripts\activate.ps1 # PowerShell
pip install requests flaskAPI
```

#### Manually install through pip+requirements.txt
1. Clone this repository:

```bash
git clone https://github.com/Lt2023/LLSA
```

2. Configuration

```bash
pip install -r requirements.txt
```
> [!WARNING]  
> If you encounter any errors or exceptions, please provide timely feedback on the issue.

### Configuration (those marked with an asterisk must be configured, otherwise it will cause an exception!)
> Default path for configuration file: `config.json`

#### * CA configuration
Open `config. json` and modify the `ca` item
> [!WARNING]
> Please send a private message to the ColudAI department head and enter the official ColudAI group to obtain the CA, otherwise you will receive an abnormal response!


#### Port configuration
Open `config. json` and modify the `Port` item
> [!WARNING]
> The number must be an int!!!

### Run
```bash
python main.py
```
or
```bash
python3 main.py
```

### Contribution

🤩 Welcome to submit questions and suggestions. You can contribute in the following ways:

Submit issue: Issue Tracker

Submit code: Pull Requests



# Warning!
This document was translated based on Baidu Translate, but there was an error in meaning. Please issue it. Thank you!