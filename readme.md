# DiskClean - 硬盘空间分析与清理工具

## 项目简介
DiskClean是一个基于Python的Web应用，旨在帮助用户快速定位并清理硬盘中占用空间较大的目录。通过直观的Web界面，用户可以查看各分区目录大小、按大小排序，并执行安全的目录删除操作。

## 核心功能
- 📊 分区空间可视化：直观展示各磁盘分区的使用情况
- 📁 目录大小分析：递归扫描目录并按大小排序
- 🗑️ 安全删除操作：在Web界面中直接删除不需要的大文件/目录
- 🔄 多平台支持：
  - 一阶段：支持Windows系统
  - 二阶段：支持Linux系统

## 技术栈
- 后端：Python 3.x
- Web框架：Flask
- 前端：Vue
- 系统接口：Windows API (当前), Linux Filesystem API (开发中)

## 代码目录结构
- `app.py`：Flask应用主文件
- `static/`：前端静态文件目录
- `templates/`：前端模板文件目录
- `tests/`：单元测试目录
- `requirements.txt`：项目依赖文件

```bash
diskclean/
├── .gitignore          # Git忽略文件配置
├── readme.md           # 项目说明文档
├── requirements.txt    # 项目依赖
├── app.py              # Flask应用主文件
├── static/             # 静态资源目录
│   └── css/            # 样式表目录
│   └── js/             # JavaScript目录
│   └── img/            # 图片资源目录
└── templates/          # HTML模板目录
    └── index.html      # 主页面模板
```

## 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/[你的用户名]/diskclean.git
   cd diskclean
   ```