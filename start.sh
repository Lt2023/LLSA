#!/bin/bash
#!/bin/bash

# 项目A配置
PROJECT_A_DIR="/home/SAI"
BIND_A="0.0.0.0:5000"
ACCESS_LOGFILE_A="$PROJECT_A_DIR/logs/gunicorn_access_chat.log"
ERROR_LOGFILE_A="$PROJECT_A_DIR/logs/gunicorn_error_chat.log"

# 项目B配置
PROJECT_B_DIR="/home/SAI"
BIND_B="0.0.0.0:5001"
ACCESS_LOGFILE_B="$PROJECT_B_DIR/logs/gunicorn_access_tts.log"
ERROR_LOGFILE_B="$PROJECT_B_DIR/logs/gunicorn_error_tts.log"

# 启动项目A
echo "Starting Project chat..."
cd "$PROJECT_A_DIR" || exit 1
gunicorn --bind "$BIND_A" --workers 2 --access-logfile "$ACCESS_LOGFILE_A" --error-logfile "$ERROR_LOGFILE_A" "sai2_5:app" > /dev/null &

# 启动项目B
echo "Starting Project tts..."
cd "$PROJECT_B_DIR" || exit 1
gunicorn --bind "$BIND_B" --workers 2 --access-logfile "$ACCESS_LOGFILE_B" --error-logfile "$ERROR_LOGFILE_B" "tts:app" > /dev/null &

echo "Both projects have been started."