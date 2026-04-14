# 诗词雅韵 - 每日诗词推荐系统

高端典雅的古诗词推荐应用，基于 chinese-poetry 数据库。

## 快速启动

```bash
# 启动器（图形界面选择版本）
python chinese-poetry/launcher.py

# 或直接启动
python chinese-poetry/poetry_gui.py          # 标准版
python chinese-poetry/poetry_gui_luxury.py   # 豪华版
python chinese-poetry/daily_poetry.py        # 命令行版
```

## 版本说明

| 版本 | 文件 | 特点 |
|------|------|------|
| 启动器 | `launcher.py` | 图形化选择版本 |
| 标准版 | `poetry_gui.py` | 经典深色主题 |
| 豪华版 | `poetry_gui_luxury.py` | 金色装饰，更精美 |
| 命令行 | `daily_poetry.py` | 无GUI依赖 |

## 界面预览

```
┌─────────────────────────────────────────────┐
│    ◈  诗 词 雅 韵  ◈                        │
│      品味千年文化 · 感悟诗意人生             │
│                                    2025年4月 │
├─────────────────────────────────────────────┤
│  ┌───────────────────────────────────────┐  │
│  │  ◇────────────────────────────────◇  │  │
│  │  【唐诗】                             │  │
│  │         静 夜 思                      │  │
│  │        ✦ 李白                         │  │
│  │    床前明月光，疑是地上霜。           │  │
│  │    举头望明月，低头思故乡。           │  │
│  │  ◇────────────────────────────────◇  │  │
│  └───────────────────────────────────────┘  │
│   [换一首]  [全部▼]        [历史] [收藏]    │
└─────────────────────────────────────────────┘
```

## 功能特点

- 每日推荐（根据日期固定）
- 随机浏览诗词
- 唐诗/宋词分类筛选
- 收藏喜欢的诗词
- 历史记录查看
- 深色典雅主题

## 数据统计

- 唐诗：254,248 首
- 宋词：21,053 首
- 总计：275,301 首

## 文件结构

```
chinese-poetry/
├── launcher.py           # 启动器
├── poetry_gui.py         # 标准版GUI
├── poetry_gui_luxury.py  # 豪华版GUI
├── daily_poetry.py       # 命令行版
├── daily_poetry_history.json  # 历史记录
├── 全唐诗/               # 唐诗数据
├── 宋词/                 # 宋词数据
└── ...
```

## 命令行用法

```bash
# 今天的推荐
python daily_poetry.py

# 指定日期
python daily_poetry.py --date 2025-01-01

# 只看唐诗
python daily_poetry.py --type 唐诗

# 只看宋词
python daily_poetry.py --type 宋词

# 查看历史
python daily_poetry.py --history

# 保存推荐
python daily_poetry.py --save
```

## 依赖

Python 3.6+（仅使用标准库）