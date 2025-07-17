#!/bin/bash
# 项目启动脚本 (Cygwin环境专用)
# 功能: 激活虚拟环境并启动Flask应用，包含错误处理和日志管理

# 获取当前脚本目录并转换为绝对路径
cwd=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# 计算项目根目录路径
project_dir=$(realpath "$cwd/../")
echo "[INFO] 项目根目录: $project_dir"

# 创建日志目录(如果不存在)
logs_dir="$project_dir/logs"
if [ ! -d "$logs_dir" ]; then
    mkdir -p "$logs_dir"
    echo "[INFO] 创建日志目录: $logs_dir"
fi

# 检查虚拟环境是否存在
venv_activate_win="$project_dir/venv/Scripts/activate"
venv_activate_unix="$project_dir/venv/bin/activate"

# 检查两种可能的激活脚本路径
if [ -f "$venv_activate_win" ]; then
    venv_activate="$venv_activate_win"
elif [ -f "$venv_activate_unix" ]; then
    venv_activate="$venv_activate_unix"
else
    echo "[ERROR] 虚拟环境激活脚本不存在"
    exit 1
fi
if [ ! -f "$venv_activate" ]; then
    echo "[ERROR] 虚拟环境不存在，请先执行: python -m venv venv"
    exit 1
fi

# 激活虚拟环境
source "$venv_activate"
if [ $? -ne 0 ]; then
    echo "[ERROR] 虚拟环境激活失败"
    exit 1
fi

# 启动Flask应用并将所有输出重定向到日志
 echo "[INFO] 启动应用程序..."
 exec > "$logs_dir/app.log" 2>&1
 python "$project_dir/app.py" &
 app_pid=$!

# 检查应用是否成功启动
if [ $? -eq 0 ]; then
    #TODO 生成pid文件,后面重启的时候可以根据pid来执行kill
    echo "[SUCCESS] 应用已启动，进程ID: $app_pid"
    echo "[INFO] 日志文件: $logs_dir/app.log"
else
    echo "[ERROR] 应用启动失败，请查看日志文件"
    exit 1
fi
echo "start success"



