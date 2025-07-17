# VSCode使用Cygwin作为默认终端并自动进入项目根目录配置指南

## 一、打开用户设置
使用 `Ctrl+Shift+P` 快捷键打开命令面板，输入 `preferences:open user settings` 并回车，打开 `settings.json` 文件。

以 Trae IDE 为例，配置文件位置：
`C:\Users\Administrator\AppData\Roaming\Trae CN\User\settings.json`

## 二、配置终端 profiles
在 `settings.json` 中添加以下关键配置：

```json
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell"
    },
    "Command Prompt": {
      "path": [
        "${env:windir}\\Sysnative\\cmd.exe",
        "${env:windir}\\System32\\cmd.exe"
      ],
      "args": [],
      "icon": "terminal-cmd"
    },
    "Git Bash": {
      "source": "Git Bash"
    },
    "Cygwin": {
      "path": "C:\\cygwin64\\bin\\bash.exe",
      "args": [
        "--login","-c","export workspaceFolder=\"${workspaceFolder}\" && bash --login"
      ]
    }
  },
  "terminal.integrated.defaultProfile.windows": "Cygwin",
```

## 三、配置 .bashrc 文件
在 Cygwin 的家目录下（通常为 `C:\cygwin64\home\用户名`），编辑 `.bashrc` 文件，添加以下内容：

```bash
alias l='ls -al'
alias ll='ls -al'
alias ..='cd ..'
alias vi='vim'
alias apt='apt-cyg'

function open() {
  if [ -z "$1" ]; then
    explorer "$(cygpath -w .)"  # 无参数时打开当前目录
  else
    explorer "$(cygpath -w "$1")"  # 打开指定路径
  fi
}

export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

[[ "$TERM_PROGRAM" == "kiro" ]] && . "$(kiro --locate-shell-integration-path bash)"
alias path='echo $PATH | tr ":" "\n" | nl -w2 -s ") "'
# 配置系统Python路径优先级
function configure_system_python() {
    # 系统Python主目录
    local python_home="/cygdrive/c/Users/Administrator/AppData/Local/Programs/Python/Python313"
    # 将Python路径添加到PATH最前面（优先于Cygwin自带Python）
    export PATH="${python_home}:${python_home}/Scripts:$PATH"
}

# 自动执行配置
configure_system_python
# 检查并切换到workspaceFolder目录（如果环境变量存在）
# 功能：自动进入Trae IDE设置的项目根目录，支持Windows路径自动转换为Cygwin格式
if [ -n "$workspaceFolder" ]; then
    # 使用cygpath工具将Windows路径转换为Cygwin兼容路径
    # -u参数表示转换为Unix风格路径（/cygdrive/d/...）
    cygwin_path=$(cygpath -u "$workspaceFolder")

    # 切换到转换后的目录，|| exit确保cd失败时不继续执行后续命令
    cd "$cygwin_path" || exit

    # 可选：显示当前工作目录确认
    echo "自动进入项目目录: $PWD"
fi

```

## 四、配置说明
1. **终端配置**：通过 `terminal.integrated.profiles.windows` 定义Cygwin终端，设置 `--login` 参数确保bash登录环境加载
2. **路径转换**：使用 `cygpath -u` 命令将Windows路径自动转换为Cygwin兼容的Unix风格路径
3. **环境变量**：通过 `workspaceFolder` 环境变量获取IDE当前打开的项目路径
4. **自动切换**：启动终端时自动执行 `cd` 命令进入项目根目录，并显示当前路径确认
