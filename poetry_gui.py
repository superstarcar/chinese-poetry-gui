#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日诗词推荐 - 高端典雅GUI
"""

import tkinter as tk
from tkinter import ttk
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import math


class PoetryGUI:
    """诗词推荐GUI主类"""
    
    # 颜色主题 - 深色典雅风格
    COLORS = {
        'bg_dark': '#0d0d0d',           # 深黑背景
        'bg_card': '#1a1a1a',           # 卡片背景
        'bg_card_hover': '#252525',     # 卡片悬停
        'gold': '#c9a959',              # 金色
        'gold_light': '#e8d5a3',        # 浅金
        'gold_dark': '#8b7355',         # 暗金
        'text_primary': '#f5f5f5',      # 主文字
        'text_secondary': '#a0a0a0',    # 次要文字
        'text_dim': '#666666',          # 暗淡文字
        'accent': '#8b0000',            # 深红强调
        'accent_light': '#a52a2a',      # 浅红
        'border': '#333333',            # 边框
        'gradient_start': '#1a1a1a',    # 渐变起始
        'gradient_end': '#0d0d0d',      # 渐变结束
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("诗词雅韵 - 每日推荐")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=self.COLORS['bg_dark'])
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        # 初始化数据
        self.base_path = Path(__file__).parent
        self.tang_poetry_path = self.base_path / "全唐诗"
        self.song_poetry_path = self.base_path / "宋词"
        self.history_file = self.base_path / "daily_poetry_history.json"
        
        self._tang_poems = None
        self._song_poems = None
        self._history = None
        
        # 当前显示的诗词
        self.current_poem = None
        self.animation_id = None
        
        # 创建界面
        self._create_styles()
        self._create_widgets()
        self._load_today_poem()
        
    def _create_styles(self):
        """创建自定义样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置按钮样式
        self.style.configure('Gold.TButton',
                           background=self.COLORS['gold_dark'],
                           foreground=self.COLORS['bg_dark'],
                           borderwidth=0,
                           focuscolor='none',
                           font=('Microsoft YaHei', 10))
        
        self.style.map('Gold.TButton',
                      background=[('active', self.COLORS['gold']),
                                 ('pressed', self.COLORS['gold_light'])])
        
        # 配置标签样式
        self.style.configure('Title.TLabel',
                           background=self.COLORS['bg_dark'],
                           foreground=self.COLORS['gold'],
                           font=('KaiTi', 28, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.COLORS['bg_dark'],
                           foreground=self.COLORS['text_secondary'],
                           font=('Microsoft YaHei', 11))
        
        self.style.configure('Card.TFrame',
                           background=self.COLORS['bg_card'])
        
        self.style.configure('PoemTitle.TLabel',
                           background=self.COLORS['bg_card'],
                           foreground=self.COLORS['gold'],
                           font=('KaiTi', 20, 'bold'))
        
        self.style.configure('PoemAuthor.TLabel',
                           background=self.COLORS['bg_card'],
                           foreground=self.COLORS['text_secondary'],
                           font=('KaiTi', 12))
        
        self.style.configure('PoemText.TLabel',
                           background=self.COLORS['bg_card'],
                           foreground=self.COLORS['text_primary'],
                           font=('KaiTi', 16))
        
        self.style.configure('Date.TLabel',
                           background=self.COLORS['bg_dark'],
                           foreground=self.COLORS['text_dim'],
                           font=('Microsoft YaHei', 10))
        
    def _create_widgets(self):
        """创建界面组件"""
        # 主容器
        self.main_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # 顶部区域
        self._create_header()
        
        # 中间诗词卡片区域
        self._create_poem_card()
        
        # 底部控制栏
        self._create_controls()
        
        # 状态栏
        self._create_status_bar()
        
    def _create_header(self):
        """创建顶部标题区域"""
        header_frame = tk.Frame(self.main_frame, bg=self.COLORS['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 左侧标题
        title_container = tk.Frame(header_frame, bg=self.COLORS['bg_dark'])
        title_container.pack(side=tk.LEFT)
        
        # 主标题
        title_label = tk.Label(title_container, 
                              text="诗词雅韵",
                              font=('KaiTi', 32, 'bold'),
                              fg=self.COLORS['gold'],
                              bg=self.COLORS['bg_dark'])
        title_label.pack(anchor='w')
        
        # 副标题
        subtitle_label = tk.Label(title_container,
                                 text="品味千年文化，感悟诗意人生",
                                 font=('Microsoft YaHei', 11),
                                 fg=self.COLORS['text_secondary'],
                                 bg=self.COLORS['bg_dark'])
        subtitle_label.pack(anchor='w')
        
        # 右侧日期显示
        date_container = tk.Frame(header_frame, bg=self.COLORS['bg_dark'])
        date_container.pack(side=tk.RIGHT, anchor='e')
        
        today = datetime.now()
        date_text = f"{today.year}年{today.month}月{today.day}日"
        
        self.date_label = tk.Label(date_container,
                                  text=date_text,
                                  font=('KaiTi', 14),
                                  fg=self.COLORS['gold_light'],
                                  bg=self.COLORS['bg_dark'])
        self.date_label.pack(anchor='e')
        
        # 星期
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        weekday = weekdays[today.weekday()]
        
        self.weekday_label = tk.Label(date_container,
                                     text=weekday,
                                     font=('Microsoft YaHei', 10),
                                     fg=self.COLORS['text_dim'],
                                     bg=self.COLORS['bg_dark'])
        self.weekday_label.pack(anchor='e')
        
    def _create_poem_card(self):
        """创建诗词卡片区域"""
        # 卡片外框（带边框效果）
        card_outer = tk.Frame(self.main_frame, 
                             bg=self.COLORS['gold_dark'],
                             padx=2, pady=2)
        card_outer.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 卡片内框
        self.card_frame = tk.Frame(card_outer, bg=self.COLORS['bg_card'])
        self.card_frame.pack(fill=tk.BOTH, expand=True)
        
        # 卡片内容容器
        card_content = tk.Frame(self.card_frame, bg=self.COLORS['bg_card'])
        card_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # 顶部装饰线
        self._create_decorative_line(card_content)
        
        # 类型标签（唐诗/宋词）
        self.type_label = tk.Label(card_content,
                                  text="唐诗",
                                  font=('Microsoft YaHei', 10),
                                  fg=self.COLORS['gold_dark'],
                                  bg=self.COLORS['bg_card'])
        self.type_label.pack(anchor='w', pady=(10, 5))
        
        # 诗词标题
        self.title_label = tk.Label(card_content,
                                   text="静夜思",
                                   font=('KaiTi', 24, 'bold'),
                                   fg=self.COLORS['gold'],
                                   bg=self.COLORS['bg_card'],
                                   wraplength=700)
        self.title_label.pack(anchor='w', pady=(0, 10))
        
        # 作者信息
        author_frame = tk.Frame(card_content, bg=self.COLORS['bg_card'])
        author_frame.pack(anchor='w', pady=(0, 20))
        
        self.author_label = tk.Label(author_frame,
                                    text="李白",
                                    font=('KaiTi', 14),
                                    fg=self.COLORS['text_secondary'],
                                    bg=self.COLORS['bg_card'])
        self.author_label.pack(side=tk.LEFT)
        
        # 分隔符
        separator = tk.Label(author_frame,
                            text="  ·  ",
                            font=('KaiTi', 14),
                            fg=self.COLORS['text_dim'],
                            bg=self.COLORS['bg_card'])
        separator.pack(side=tk.LEFT)
        
        # 词牌名（宋词专用，初始隐藏）
        self.rhythmic_label = tk.Label(author_frame,
                                      text="",
                                      font=('KaiTi', 14),
                                      fg=self.COLORS['gold_dark'],
                                      bg=self.COLORS['bg_card'])
        self.rhythmic_label.pack(side=tk.LEFT)
        
        # 诗词内容区域
        poem_frame = tk.Frame(card_content, bg=self.COLORS['bg_card'])
        poem_frame.pack(fill=tk.BOTH, expand=True)
        
        # 使用Canvas实现诗词内容（支持更好的排版）
        self.poem_canvas = tk.Canvas(poem_frame,
                                    bg=self.COLORS['bg_card'],
                                    highlightthickness=0)
        self.poem_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 底部装饰线
        self._create_decorative_line(card_content, bottom=True)
        
    def _create_decorative_line(self, parent, bottom=False):
        """创建装饰线"""
        line_frame = tk.Frame(parent, bg=self.COLORS['bg_card'], height=30)
        if bottom:
            line_frame.pack(fill=tk.X, pady=(20, 0), side=tk.BOTTOM)
        else:
            line_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 中间的装饰图案
        canvas = tk.Canvas(line_frame, 
                          width=200, height=20,
                          bg=self.COLORS['bg_card'],
                          highlightthickness=0)
        canvas.pack(expand=True)
        
        # 绘制装饰线
        canvas.create_line(0, 10, 80, 10, fill=self.COLORS['gold_dark'], width=1)
        canvas.create_text(100, 10, text="◇", fill=self.COLORS['gold'], font=('Arial', 10))
        canvas.create_line(120, 10, 200, 10, fill=self.COLORS['gold_dark'], width=1)
        
    def _create_controls(self):
        """创建底部控制栏"""
        control_frame = tk.Frame(self.main_frame, bg=self.COLORS['bg_dark'])
        control_frame.pack(fill=tk.X, pady=15)
        
        # 左侧按钮组
        left_buttons = tk.Frame(control_frame, bg=self.COLORS['bg_dark'])
        left_buttons.pack(side=tk.LEFT)
        
        # 刷新按钮
        self.refresh_btn = tk.Button(left_buttons,
                                    text="  换一首  ",
                                    font=('Microsoft YaHei', 10),
                                    fg=self.COLORS['text_primary'],
                                    bg=self.COLORS['bg_card'],
                                    activebackground=self.COLORS['bg_card_hover'],
                                    activeforeground=self.COLORS['gold'],
                                    relief=tk.FLAT,
                                    cursor='hand2',
                                    command=self._refresh_poem)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 类型选择
        self.type_var = tk.StringVar(value="全部")
        type_options = ["全部", "唐诗", "宋词"]
        
        type_menu = tk.OptionMenu(control_frame, self.type_var, *type_options,
                                 command=self._on_type_change)
        type_menu.configure(font=('Microsoft YaHei', 10),
                           fg=self.COLORS['text_primary'],
                           bg=self.COLORS['bg_card'],
                           activebackground=self.COLORS['bg_card_hover'],
                           activeforeground=self.COLORS['gold'],
                           relief=tk.FLAT,
                           highlightthickness=0,
                           cursor='hand2')
        type_menu['menu'].configure(font=('Microsoft YaHei', 10),
                                   fg=self.COLORS['text_primary'],
                                   bg=self.COLORS['bg_card'])
        type_menu.pack(side=tk.LEFT, padx=10)
        
        # 右侧按钮组
        right_buttons = tk.Frame(control_frame, bg=self.COLORS['bg_dark'])
        right_buttons.pack(side=tk.RIGHT)
        
        # 历史记录按钮
        self.history_btn = tk.Button(right_buttons,
                                    text="  历史记录  ",
                                    font=('Microsoft YaHei', 10),
                                    fg=self.COLORS['text_primary'],
                                    bg=self.COLORS['bg_card'],
                                    activebackground=self.COLORS['bg_card_hover'],
                                    activeforeground=self.COLORS['gold'],
                                    relief=tk.FLAT,
                                    cursor='hand2',
                                    command=self._show_history)
        self.history_btn.pack(side=tk.LEFT, padx=10)
        
        # 收藏按钮
        self.favorite_btn = tk.Button(right_buttons,
                                     text="  ♡ 收藏  ",
                                     font=('Microsoft YaHei', 10),
                                     fg=self.COLORS['text_primary'],
                                     bg=self.COLORS['bg_card'],
                                     activebackground=self.COLORS['bg_card_hover'],
                                     activeforeground=self.COLORS['accent_light'],
                                     relief=tk.FLAT,
                                     cursor='hand2',
                                     command=self._toggle_favorite)
        self.favorite_btn.pack(side=tk.LEFT)
        
    def _create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.main_frame, bg=self.COLORS['bg_dark'])
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 数据统计
        tang_count = len(self._load_tang_poems())
        song_count = len(self._load_song_poems())
        total = tang_count + song_count
        
        status_text = f"共收录 {total:,} 首诗词 (唐诗 {tang_count:,} 首 · 宋词 {song_count:,} 首)"
        
        self.status_label = tk.Label(status_frame,
                                    text=status_text,
                                    font=('Microsoft YaHei', 9),
                                    fg=self.COLORS['text_dim'],
                                    bg=self.COLORS['bg_dark'])
        self.status_label.pack(side=tk.LEFT)
        
        # 版权信息
        copyright_label = tk.Label(status_frame,
                                  text="数据来源: chinese-poetry",
                                  font=('Microsoft YaHei', 9),
                                  fg=self.COLORS['text_dim'],
                                  bg=self.COLORS['bg_dark'])
        copyright_label.pack(side=tk.RIGHT)
        
    def _load_tang_poems(self):
        """加载唐诗数据"""
        if self._tang_poems is not None:
            return self._tang_poems
            
        self._tang_poems = []
        if self.tang_poetry_path.exists():
            tang_files = list(self.tang_poetry_path.glob("poet.song.*.json"))
            for file_path in tang_files[:20]:  # 限制加载数量以加快启动
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        poems = json.load(f)
                        for poem in poems:
                            poem['type'] = '唐诗'
                            self._tang_poems.append(poem)
                except Exception:
                    pass
                    
        return self._tang_poems
    
    def _load_song_poems(self):
        """加载宋词数据"""
        if self._song_poems is not None:
            return self._song_poems
            
        self._song_poems = []
        if self.song_poetry_path.exists():
            song_files = list(self.song_poetry_path.glob("ci.song.*.json"))
            for file_path in song_files[:10]:  # 限制加载数量
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        poems = json.load(f)
                        for poem in poems:
                            poem['type'] = '宋词'
                            if 'title' not in poem and 'rhythmic' in poem:
                                poem['title'] = poem['rhythmic']
                            self._song_poems.append(poem)
                except Exception:
                    pass
                    
        return self._song_poems
    
    def _get_daily_poem(self, date=None, poem_type=None):
        """获取每日诗词"""
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        # 使用日期作为随机种子
        date_seed = date.year * 10000 + date.month * 100 + date.day
        
        # 获取诗词列表
        if poem_type == '唐诗':
            poems = self._load_tang_poems()
        elif poem_type == '宋词':
            poems = self._load_song_poems()
        else:
            poems = self._load_tang_poems() + self._load_song_poems()
        
        if not poems:
            return None
        
        random.seed(date_seed)
        return random.choice(poems)
    
    def _load_today_poem(self):
        """加载今天的诗词"""
        type_map = {"全部": None, "唐诗": "唐诗", "宋词": "宋词"}
        poem_type = type_map.get(self.type_var.get())
        
        self.current_poem = self._get_daily_poem(poem_type=poem_type)
        if self.current_poem:
            self._display_poem(self.current_poem)
    
    def _display_poem(self, poem):
        """显示诗词"""
        if not poem:
            return
        
        # 更新类型标签
        poem_type = poem.get('type', '唐诗')
        self.type_label.config(text=f"【{poem_type}】")
        
        # 更新标题
        title = poem.get('title', '无题')
        self.title_label.config(text=title)
        
        # 更新作者
        author = poem.get('author', '佚名')
        self.author_label.config(text=author)
        
        # 更新词牌名
        rhythmic = poem.get('rhythmic', '')
        if rhythmic and rhythmic != title:
            self.rhythmic_label.config(text=f"词牌：{rhythmic}")
        else:
            self.rhythmic_label.config(text="")
        
        # 清空画布并显示诗词
        self.poem_canvas.delete('all')
        
        paragraphs = poem.get('paragraphs', [])
        y_pos = 30
        line_height = 35
        
        for i, line in enumerate(paragraphs):
            # 创建淡入动画效果
            self.poem_canvas.create_text(20, y_pos,
                                        text=line,
                                        font=('KaiTi', 18),
                                        fill=self.COLORS['text_primary'],
                                        anchor='w',
                                        tags=f'line_{i}')
            y_pos += line_height
        
        # 更新收藏按钮状态
        self._update_favorite_button()
        
    def _refresh_poem(self):
        """刷新诗词（随机选择）"""
        type_map = {"全部": None, "唐诗": "唐诗", "宋词": "宋词"}
        poem_type = type_map.get(self.type_var.get())
        
        if poem_type == '唐诗':
            poems = self._load_tang_poems()
        elif poem_type == '宋词':
            poems = self._load_song_poems()
        else:
            poems = self._load_tang_poems() + self._load_song_poems()
        
        if poems:
            self.current_poem = random.choice(poems)
            self._display_poem(self.current_poem)
    
    def _on_type_change(self, *args):
        """类型改变时的处理"""
        self._load_today_poem()
    
    def _show_history(self):
        """显示历史记录窗口"""
        history_window = tk.Toplevel(self.root)
        history_window.title("历史记录")
        history_window.geometry("600x500")
        history_window.configure(bg=self.COLORS['bg_dark'])
        
        # 标题
        title_label = tk.Label(history_window,
                              text="诗词推荐历史",
                              font=('KaiTi', 20, 'bold'),
                              fg=self.COLORS['gold'],
                              bg=self.COLORS['bg_dark'])
        title_label.pack(pady=20)
        
        # 历史记录列表
        list_frame = tk.Frame(history_window, bg=self.COLORS['bg_dark'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 创建列表框
        listbox = tk.Listbox(list_frame,
                            font=('Microsoft YaHei', 11),
                            fg=self.COLORS['text_primary'],
                            bg=self.COLORS['bg_card'],
                            selectbackground=self.COLORS['gold_dark'],
                            selectforeground=self.COLORS['bg_dark'],
                            relief=tk.FLAT,
                            highlightthickness=0)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        # 加载历史数据
        history = self._load_history()
        for date_str in sorted(history.keys(), reverse=True):
            poem_info = history[date_str]
            title = poem_info.get('title', '无题')
            author = poem_info.get('author', '佚名')
            poem_type = poem_info.get('type', '')
            
            display_text = f"{date_str}  【{poem_type}】{title} - {author}"
            listbox.insert(tk.END, display_text)
        
        if not history:
            listbox.insert(tk.END, "暂无历史记录")
        
        # 关闭按钮
        close_btn = tk.Button(history_window,
                             text="  关闭  ",
                             font=('Microsoft YaHei', 10),
                             fg=self.COLORS['text_primary'],
                             bg=self.COLORS['bg_card'],
                             activebackground=self.COLORS['bg_card_hover'],
                             relief=tk.FLAT,
                             command=history_window.destroy)
        close_btn.pack(pady=(0, 20))
    
    def _load_history(self):
        """加载历史记录"""
        if self._history is not None:
            return self._history
            
        self._history = {}
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self._history = json.load(f)
            except Exception:
                self._history = {}
        
        return self._history
    
    def _save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self._history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _toggle_favorite(self):
        """切换收藏状态"""
        if not self.current_poem:
            return
        
        history = self._load_history()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today in history:
            # 已收藏，取消收藏
            del history[today]
            self.favorite_btn.config(text="  ♡ 收藏  ")
        else:
            # 未收藏，添加收藏
            history[today] = {
                'title': self.current_poem.get('title', '无题'),
                'author': self.current_poem.get('author', '佚名'),
                'type': self.current_poem.get('type', ''),
                'rhythmic': self.current_poem.get('rhythmic', ''),
                'paragraphs': self.current_poem.get('paragraphs', [])
            }
            self.favorite_btn.config(text="  ♥ 已收藏  ")
        
        self._history = history
        self._save_history()
    
    def _update_favorite_button(self):
        """更新收藏按钮状态"""
        history = self._load_history()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today in history:
            self.favorite_btn.config(text="  ♥ 已收藏  ")
        else:
            self.favorite_btn.config(text="  ♡ 收藏  ")
    
    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """主函数"""
    app = PoetryGUI()
    app.run()


if __name__ == "__main__":
    main()