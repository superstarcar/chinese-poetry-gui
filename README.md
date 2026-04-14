# 诗词雅韵 - 每日诗词推荐系统

高端典雅的古诗词推荐应用，深色主题，金色装饰，每日为你推荐一首诗词。

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 效果预览

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│      ◈  诗 词 雅 韵  ◈                              │
│        品味千年文化 · 感悟诗意人生                   │
│                                          2025年4月  │
│                                             星期一   │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│    ┌───────────────────────────────────────────┐    │
│    │                                           │    │
│    │  【唐诗】                                 │    │
│    │                                           │    │
│    │          静 夜 思                         │    │
│    │                                           │    │
│    │          ✦ 李白                           │    │
│    │                                           │    │
│    │      床前明月光，疑是地上霜。             │    │
│    │      举头望明月，低头思故乡。             │    │
│    │                                           │    │
│    └───────────────────────────────────────────┘    │
│                                                     │
│    [换一首]  [全部▼]            [历史]  [收藏]      │
│                                                     │
│    ◈ 收录 275,301 首诗词              chinese-poetry │
└─────────────────────────────────────────────────────┘
```

## 快速开始

### 第一步：安装 Python

下载并安装 Python 3.6 或更高版本：
- 官网下载：https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

### 第二步：下载项目

**方式一：使用 Git（推荐）**
```bash
git clone https://github.com/superstarcar/chinese-poetry-gui.git
cd chinese-poetry-gui
```

**方式二：下载 ZIP**
1. 点击页面右上角绿色按钮 "Code"
2. 选择 "Download ZIP"
3. 解压到任意文件夹

### 第三步：下载诗词数据

本程序需要诗词数据库才能运行。

**方式一：使用 Git（推荐）**
```bash
# 在项目目录下执行
git clone https://github.com/chinese-poetry/chinese-poetry.git poetry_data
```

**方式二：手动下载**
1. 访问 https://github.com/chinese-poetry/chinese-poetry
2. 点击 "Code" → "Download ZIP"
3. 解压后，将 `全唐诗` 和 `宋词` 文件夹复制到项目目录

### 第四步：整理目录结构

确保目录结构如下：
```
chinese-poetry-gui/
├── launcher.py           # 启动器
├── poetry_gui.py         # 标准版
├── poetry_gui_luxury.py  # 豪华版
├── daily_poetry.py       # 命令行版
├── start.bat             # Windows启动脚本
├── 全唐诗/               # ← 诗词数据
│   ├── poet.song.0.json
│   └── ...
└── 宋词/                 # ← 诗词数据
    ├── ci.song.0.json
    └── ...
```

### 第五步：运行程序

**Windows 用户：**
双击 `start.bat`

**或使用命令行：**
```bash
python launcher.py          # 启动器（推荐）
python poetry_gui.py        # 标准版
python poetry_gui_luxury.py # 豪华版
python daily_poetry.py      # 命令行版
```

## 版本说明

| 版本 | 文件 | 说明 |
|------|------|------|
| 启动器 | launcher.py | 图形界面选择版本 |
| 标准版 | poetry_gui.py | 经典深色主题，稳定流畅 |
| 豪华版 | poetry_gui_luxury.py | 金色装饰，更精美的设计 |
| 命令行 | daily_poetry.py | 无图形界面，适合脚本调用 |

## 功能特点

- **每日推荐**：根据日期自动推荐一首诗词，每天不重复
- **随机浏览**：点击"换一首"随机浏览诗词库
- **类型筛选**：可选择唐诗、宋词或全部
- **收藏功能**：收藏喜欢的诗词
- **历史记录**：查看和管理推荐历史
- **深色主题**：护眼的深色典雅界面

## 命令行版本用法

```bash
# 显示今天的推荐
python daily_poetry.py

# 指定日期
python daily_poetry.py --date 2025-01-01

# 只显示唐诗
python daily_poetry.py --type 唐诗

# 只显示宋词
python daily_poetry.py --type 宋词

# 查看历史记录
python daily_poetry.py --history

# 保存推荐到历史
python daily_poetry.py --save

# 查看帮助
python daily_poetry.py --help
```

## 数据统计

- 唐诗：254,248 首
- 宋词：21,053 首
- 总计：275,301 首诗词

## 常见问题

**Q: 运行提示找不到模块？**
A: 确保已正确放置 `全唐诗` 和 `宋词` 文件夹到项目目录。

**Q: 中文显示乱码？**
A: Windows 用户请使用 UTF-8 编码的终端，或直接双击 `start.bat`。

**Q: 如何更换推荐的诗词？**
A: GUI版本点击"换一首"按钮，命令行版再次运行命令即可。

**Q: 数据文件在哪里下载？**
A: https://github.com/chinese-poetry/chinese-poetry

## 数据来源

诗词数据来自：[chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)

感谢所有为中华古诗词数字化做出贡献的开发者。

## 系统要求

- Python 3.6+
- 操作系统：Windows / macOS / Linux
- 无需安装第三方库

## 许可证

MIT License
