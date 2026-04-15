# 诗词雅韵 - 每日诗词推荐系统

高端典雅的古诗词推荐应用，深色主题，支持桌面悬浮窗。

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 功能亮点

- **桌面悬浮窗** - 小巧精致，始终置顶显示
- **每日推荐** - 根据日期自动推荐诗词
- **随机浏览** - 双击切换诗词
- **深色主题** - 护眼典雅界面

## 快速开始

### 第一步：安装 Python
下载：https://www.python.org/downloads/ （安装时勾选 Add to PATH）

### 第二步：下载项目
```bash
git clone https://github.com/superstarcar/chinese-poetry-gui.git
cd chinese-poetry-gui
```

### 第三步：下载诗词数据
```bash
git clone https://github.com/chinese-poetry/chinese-poetry.git data
```
然后把 `data` 里的 `全唐诗` 和 `宋词` 文件夹复制到项目目录。

### 第四步：运行
```bash
python launcher.py
```
或双击 `start.bat`

## 版本选择

| 版本 | 说明 | 推荐场景 |
|------|------|----------|
| 桌面悬浮窗 | 小巧置顶，双击换诗 | 日常使用 |
| 标准版 GUI | 完整功能界面 | 详细阅读 |
| 豪华版 GUI | 金色装饰 | 追求美感 |
| 命令行版 | 无图形界面 | 脚本调用 |

## 悬浮窗使用

- **拖动** - 按住左键拖动窗口
- **换一首** - 双击窗口
- **右键菜单** - 筛选唐诗/宋词、设置开机自启

```
┌─────────────────────────────┐
│ ◈ 每日诗词            ×    │
│─────────────────────────────│
│ 【唐诗】                    │
│      静夜思                 │
│      李白                   │
│                             │
│  床前明月光，疑是地上霜。   │
│  举头望明月，低头思故乡。   │
│                             │
│   双击换一首 · 右键菜单     │
└─────────────────────────────┘
```

## 命令行用法

```bash
python daily_poetry.py                    # 今天的推荐
python daily_poetry.py --date 2025-01-01  # 指定日期
python daily_poetry.py --type 唐诗        # 只看唐诗
python daily_poetry.py --history          # 查看历史
```

## 常见问题

**Q: 如何开机自启？**
A: 右键悬浮窗 → 开机自启

**Q: 提示找不到数据？**
A: 确保 `全唐诗` 和 `宋词` 文件夹在项目目录下

**Q: 中文乱码？**
A: 使用 `start.bat` 启动

## 数据来源

[chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) - 最全中华古诗词数据库

## License

MIT
