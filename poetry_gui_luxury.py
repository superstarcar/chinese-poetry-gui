#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日诗词推荐 - 豪华版GUI
"""

import tkinter as tk
import json
import random
from datetime import datetime
from pathlib import Path


class LuxuryPoetryGUI:
    """豪华版诗词推荐GUI"""
    
    COLORS = {
        'bg': '#0a0a0a',
        'bg_card': '#16213e',
        'gold': '#ffd700',
        'gold_dark': '#b8860b',
        'cream': '#fff8dc',
        'text': '#f8f8f8',
        'text_dim': '#666666',
        'border': '#333355',
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("诗词雅韵 - 每日推荐")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.COLORS['bg'])
        
        self.base_path = Path(__file__).parent
        self.tang_poetry_path = self._find_data_path("全唐诗")
        self.song_poetry_path = self._find_data_path("宋词")
        self.history_file = self.base_path / "daily_poetry_history.json"
        
        self._tang_poems = None
        self._song_poems = None
        self._history = None
        self.current_poem = None
        
        self._create_ui()
        self._load_today_poem()
    
    def _find_data_path(self, folder_name):
        """查找数据文件夹的路径"""
        possible_paths = [
            self.base_path / folder_name,
            self.base_path.parent / "chinese-poetry" / folder_name,
            self.base_path.parent / folder_name,
            Path("chinese-poetry") / folder_name,
            Path(folder_name),
        ]
        for p in possible_paths:
            if p.exists():
                return p
        return self.base_path / folder_name
        
    def _create_ui(self):
        """创建界面"""
        bg = self.COLORS['bg']
        
        # 主框架
        main = tk.Frame(self.root, bg=bg, padx=40, pady=25)
        main.pack(fill=tk.BOTH, expand=True)
        
        # ====== 标题区域 ======
        header = tk.Frame(main, bg=bg)
        header.pack(fill=tk.X, pady=(0, 20))
        
        # 标题
        title_frame = tk.Frame(header, bg=bg)
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="◈", font=('KaiTi', 20),
                fg=self.COLORS['gold'], bg=bg).pack(side=tk.LEFT, padx=5)
        
        tk.Label(title_frame, text="诗 词 雅 韵", font=('KaiTi', 32, 'bold'),
                fg=self.COLORS['gold'], bg=bg).pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="◈", font=('KaiTi', 20),
                fg=self.COLORS['gold'], bg=bg).pack(side=tk.LEFT, padx=5)
        
        tk.Label(header, text="品味千年文化 · 感悟诗意人生",
                font=('Microsoft YaHei', 11),
                fg=self.COLORS['text_dim'], bg=bg).pack(pady=(5, 0))
        
        # 日期
        date_frame = tk.Frame(header, bg=bg)
        date_frame.pack(side=tk.RIGHT, anchor='e')
        
        today = datetime.now()
        tk.Label(date_frame, text=f"{today.year}年{today.month}月{today.day}日",
                font=('Microsoft YaHei', 12),
                fg=self.COLORS['cream'], bg=bg).pack(anchor='e')
        
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        tk.Label(date_frame, text=weekdays[today.weekday()],
                font=('Microsoft YaHei', 10),
                fg=self.COLORS['text_dim'], bg=bg).pack(anchor='e')
        
        # ====== 诗词卡片 ======
        # 金色边框
        card_outer = tk.Frame(main, bg=self.COLORS['gold_dark'], padx=2, pady=2)
        card_outer.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 卡片背景
        card = tk.Frame(card_outer, bg=self.COLORS['bg_card'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # 卡片内容
        content = tk.Frame(card, bg=self.COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # 顶部装饰线
        self._create_ornament(content)
        
        # 类型
        self.type_label = tk.Label(content, text="【唐诗】",
                                  font=('Microsoft YaHei', 11),
                                  fg=self.COLORS['gold_dark'],
                                  bg=self.COLORS['bg_card'])
        self.type_label.pack(anchor='w', pady=(10, 5))
        
        # 标题
        self.title_label = tk.Label(content, text="静夜思",
                                   font=('KaiTi', 26, 'bold'),
                                   fg=self.COLORS['gold'],
                                   bg=self.COLORS['bg_card'])
        self.title_label.pack(pady=(5, 10))
        
        # 作者
        author_frame = tk.Frame(content, bg=self.COLORS['bg_card'])
        author_frame.pack(pady=(0, 20))
        
        tk.Label(author_frame, text="✦", font=('Arial', 10),
                fg=self.COLORS['gold_dark'],
                bg=self.COLORS['bg_card']).pack(side=tk.LEFT, padx=5)
        
        self.author_label = tk.Label(author_frame, text="李白",
                                    font=('KaiTi', 14),
                                    fg=self.COLORS['text_dim'],
                                    bg=self.COLORS['bg_card'])
        self.author_label.pack(side=tk.LEFT)
        
        self.rhythmic_label = tk.Label(author_frame, text="",
                                      font=('KaiTi', 12),
                                      fg=self.COLORS['gold_dark'],
                                      bg=self.COLORS['bg_card'])
        self.rhythmic_label.pack(side=tk.LEFT, padx=15)
        
        # 诗词内容
        poem_frame = tk.Frame(content, bg=self.COLORS['bg_card'])
        poem_frame.pack(fill=tk.BOTH, expand=True)
        
        self.poem_canvas = tk.Canvas(poem_frame,
                                    bg=self.COLORS['bg_card'],
                                    highlightthickness=0)
        self.poem_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 底部装饰线
        self._create_ornament(content, bottom=True)
        
        # ====== 控制按钮 ======
        controls = tk.Frame(main, bg=bg)
        controls.pack(fill=tk.X, pady=15)
        
        # 左侧按钮
        left = tk.Frame(controls, bg=bg)
        left.pack(side=tk.LEFT)
        
        self._create_button(left, "⟲ 换一首", self._refresh_poem).pack(side=tk.LEFT, padx=5)
        
        # 类型选择
        self.type_var = tk.StringVar(value="全部")
        menu = tk.OptionMenu(controls, self.type_var, "全部", "唐诗", "宋词",
                            command=self._on_type_change)
        menu.configure(font=('Microsoft YaHei', 10),
                      fg=self.COLORS['cream'],
                      bg=self.COLORS['bg_card'],
                      activebackground=self.COLORS['border'],
                      relief=tk.FLAT, width=8, cursor='hand2')
        menu['menu'].configure(font=('Microsoft YaHei', 10),
                              fg=self.COLORS['cream'],
                              bg=self.COLORS['bg_card'])
        menu.pack(side=tk.LEFT, padx=15)
        
        # 右侧按钮
        right = tk.Frame(controls, bg=bg)
        right.pack(side=tk.RIGHT)
        
        self._create_button(right, "📚 历史", self._show_history).pack(side=tk.LEFT, padx=5)
        
        self.favorite_btn = self._create_button(right, "♡ 收藏", self._toggle_favorite)
        self.favorite_btn.pack(side=tk.LEFT, padx=5)
        
        # ====== 底部状态栏 ======
        footer = tk.Frame(main, bg=bg)
        footer.pack(fill=tk.X, pady=(10, 0))
        
        tang = len(self._load_tang_poems())
        song = len(self._load_song_poems())
        
        tk.Label(footer, text=f"◈ 收录 {tang+song:,} 首诗词",
                font=('Microsoft YaHei', 9),
                fg=self.COLORS['text_dim'], bg=bg).pack(side=tk.LEFT)
        
        tk.Label(footer, text="数据来源: chinese-poetry",
                font=('Microsoft YaHei', 9),
                fg=self.COLORS['text_dim'], bg=bg).pack(side=tk.RIGHT)
    
    def _create_ornament(self, parent, bottom=False):
        """创建装饰线"""
        frame = tk.Frame(parent, bg=self.COLORS['bg_card'], height=25)
        if bottom:
            frame.pack(fill=tk.X, pady=(15, 0), side=tk.BOTTOM)
        else:
            frame.pack(fill=tk.X, pady=(0, 5))
        
        canvas = tk.Canvas(frame, width=250, height=15,
                          bg=self.COLORS['bg_card'],
                          highlightthickness=0)
        canvas.pack(expand=True)
        
        gold = self.COLORS['gold_dark']
        canvas.create_line(10, 7, 90, 7, fill=gold, width=1)
        canvas.create_oval(100, 3, 110, 13, fill=gold, outline='')
        canvas.create_text(125, 7, text="◇", fill=self.COLORS['gold'], font=('Arial', 10))
        canvas.create_oval(140, 3, 150, 13, fill=gold, outline='')
        canvas.create_line(160, 7, 240, 7, fill=gold, width=1)
    
    def _create_button(self, parent, text, command):
        """创建按钮"""
        btn = tk.Button(parent, text=text,
                       font=('Microsoft YaHei', 10),
                       fg=self.COLORS['cream'],
                       bg=self.COLORS['bg_card'],
                       activebackground=self.COLORS['border'],
                       activeforeground=self.COLORS['gold'],
                       relief=tk.FLAT, padx=12, pady=6,
                       cursor='hand2', command=command)
        
        def on_enter(e):
            btn.configure(fg=self.COLORS['gold'])
        def on_leave(e):
            btn.configure(fg=self.COLORS['cream'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn
    
    def _load_tang_poems(self):
        """加载唐诗"""
        if self._tang_poems is not None:
            return self._tang_poems
        self._tang_poems = []
        if self.tang_poetry_path.exists():
            for f in list(self.tang_poetry_path.glob("poet.song.*.json"))[:25]:
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        for p in json.load(file):
                            p['type'] = '唐诗'
                            self._tang_poems.append(p)
                except:
                    pass
        return self._tang_poems
    
    def _load_song_poems(self):
        """加载宋词"""
        if self._song_poems is not None:
            return self._song_poems
        self._song_poems = []
        if self.song_poetry_path.exists():
            for f in list(self.song_poetry_path.glob("ci.song.*.json"))[:15]:
                try:
                    with open(f, 'r', encoding='utf-8') as file:
                        for p in json.load(file):
                            p['type'] = '宋词'
                            if 'title' not in p and 'rhythmic' in p:
                                p['title'] = p['rhythmic']
                            self._song_poems.append(p)
                except:
                    pass
        return self._song_poems
    
    def _get_daily_poem(self, poem_type=None):
        """获取每日诗词"""
        today = datetime.now()
        seed = today.year * 10000 + today.month * 100 + today.day
        
        if poem_type == '唐诗':
            poems = self._load_tang_poems()
        elif poem_type == '宋词':
            poems = self._load_song_poems()
        else:
            poems = self._load_tang_poems() + self._load_song_poems()
        
        if not poems:
            return None
        random.seed(seed)
        return random.choice(poems)
    
    def _load_today_poem(self):
        """加载今日诗词"""
        type_map = {"全部": None, "唐诗": "唐诗", "宋词": "宋词"}
        self.current_poem = self._get_daily_poem(type_map.get(self.type_var.get()))
        if self.current_poem:
            self._display_poem(self.current_poem)
    
    def _display_poem(self, poem):
        """显示诗词"""
        if not poem:
            return
        
        self.type_label.config(text=f"【{poem.get('type', '唐诗')}】")
        self.title_label.config(text=poem.get('title', '无题'))
        self.author_label.config(text=poem.get('author', '佚名'))
        
        rhythmic = poem.get('rhythmic', '')
        if rhythmic and rhythmic != poem.get('title', ''):
            self.rhythmic_label.config(text=f"〈{rhythmic}〉")
        else:
            self.rhythmic_label.config(text="")
        
        self.poem_canvas.delete('all')
        y = 20
        for line in poem.get('paragraphs', []):
            self.poem_canvas.create_text(20, y, text=line,
                                        font=('KaiTi', 17),
                                        fill=self.COLORS['cream'],
                                        anchor='w')
            y += 35
        
        self._update_favorite_button()
    
    def _refresh_poem(self):
        """刷新诗词"""
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
        self._load_today_poem()
    
    def _show_history(self):
        """显示历史"""
        win = tk.Toplevel(self.root)
        win.title("历史记录")
        win.geometry("600x450")
        win.configure(bg=self.COLORS['bg'])
        
        tk.Label(win, text="◈ 诗词推荐历史 ◈",
                font=('KaiTi', 20, 'bold'),
                fg=self.COLORS['gold'],
                bg=self.COLORS['bg']).pack(pady=20)
        
        listbox = tk.Listbox(win,
                            font=('Microsoft YaHei', 11),
                            fg=self.COLORS['cream'],
                            bg=self.COLORS['bg_card'],
                            selectbackground=self.COLORS['gold_dark'])
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        history = self._load_history()
        if history:
            for date in sorted(history.keys(), reverse=True):
                info = history[date]
                text = f"{date}  【{info.get('type','')}】{info.get('title','')} - {info.get('author','')}"
                listbox.insert(tk.END, text)
        else:
            listbox.insert(tk.END, "暂无收藏记录")
        
        tk.Button(win, text="  关闭  ",
                 font=('Microsoft YaHei', 10),
                 fg=self.COLORS['cream'],
                 bg=self.COLORS['bg_card'],
                 relief=tk.FLAT, padx=15, pady=5,
                 command=win.destroy).pack(pady=(0, 15))
    
    def _load_history(self):
        if self._history is not None:
            return self._history
        self._history = {}
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self._history = json.load(f)
            except:
                pass
        return self._history
    
    def _save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self._history, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _toggle_favorite(self):
        if not self.current_poem:
            return
        history = self._load_history()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today in history:
            del history[today]
            self.favorite_btn.config(text="♡ 收藏")
        else:
            history[today] = {
                'title': self.current_poem.get('title', '无题'),
                'author': self.current_poem.get('author', '佚名'),
                'type': self.current_poem.get('type', ''),
                'rhythmic': self.current_poem.get('rhythmic', ''),
                'paragraphs': self.current_poem.get('paragraphs', [])
            }
            self.favorite_btn.config(text="♥ 已收藏")
        
        self._history = history
        self._save_history()
    
    def _update_favorite_button(self):
        history = self._load_history()
        today = datetime.now().strftime('%Y-%m-%d')
        if today in history:
            self.favorite_btn.config(text="♥ 已收藏")
        else:
            self.favorite_btn.config(text="♡ 收藏")
    
    def run(self):
        self.root.mainloop()


def main():
    app = LuxuryPoetryGUI()
    app.run()


if __name__ == "__main__":
    main()