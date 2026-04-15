#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诗词雅韵 - 桌面悬浮窗
小巧精致，始终置顶，每日一诗
"""

import tkinter as tk
import json
import random
from datetime import datetime
from pathlib import Path
import ctypes


class FloatingPoetry:
    """桌面悬浮诗词窗口"""
    
    # 配色
    COLORS = {
        'bg': '#1a1a2e',
        'bg_alpha': 0.85,
        'gold': '#c9a959',
        'gold_dark': '#8b7355',
        'text': '#f5f5f5',
        'text_dim': '#888888',
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("诗词雅韵")
        
        # 窗口设置：无边框、置顶、半透明
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.COLORS['bg_alpha'])
        
        # 初始位置（屏幕右下角）
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.win_w = 320
        self.win_h = 280
        self.x = screen_w - self.win_w - 30
        self.y = screen_h - self.win_h - 80
        self.root.geometry(f"{self.win_w}x{self.win_h}+{self.x}+{self.y}")
        
        self.root.configure(bg=self.COLORS['bg'])
        
        # 拖动相关
        self.drag_data = {'x': 0, 'y': 0, 'dragging': False}
        
        # 数据路径
        self.base_path = Path(__file__).parent
        self.tang_path = self.base_path / "全唐诗"
        self.song_path = self.base_path / "宋词"
        
        self._tang_poems = None
        self._song_poems = None
        self.current_poem = None
        
        # 创建界面
        self._create_ui()
        self._load_poem()
        
        # 绑定事件
        self.root.bind('<Button-1>', self._start_drag)
        self.root.bind('<B1-Motion>', self._on_drag)
        self.root.bind('<ButtonRelease-1>', self._stop_drag)
        self.root.bind('<Double-Button-1>', lambda e: self._refresh())
        self.root.bind('<Button-3>', self._show_menu)
        
    def _create_ui(self):
        """创建界面"""
        bg = self.COLORS['bg']
        
        # 主框架
        self.main_frame = tk.Frame(self.root, bg=bg, padx=15, pady=12)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 顶部：标题栏
        header = tk.Frame(self.main_frame, bg=bg)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="◈", font=('Arial', 8),
                fg=self.COLORS['gold'], bg=bg).pack(side=tk.LEFT)
        
        tk.Label(header, text=" 每日诗词", font=('Microsoft YaHei', 9),
                fg=self.COLORS['gold'], bg=bg).pack(side=tk.LEFT)
        
        # 关闭按钮
        close_btn = tk.Label(header, text=" ×", font=('Arial', 12),
                            fg=self.COLORS['text_dim'], bg=bg, cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind('<Button-1>', lambda e: self.root.destroy())
        close_btn.bind('<Enter>', lambda e: close_btn.config(fg='#ff6b6b'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(fg=self.COLORS['text_dim']))
        
        # 分隔线
        tk.Frame(self.main_frame, bg=self.COLORS['gold_dark'], height=1).pack(fill=tk.X, pady=8)
        
        # 类型标签
        self.type_label = tk.Label(self.main_frame, text="【唐诗】",
                                  font=('Microsoft YaHei', 8),
                                  fg=self.COLORS['gold_dark'], bg=bg)
        self.type_label.pack(anchor='w')
        
        # 标题 + 作者
        self.title_label = tk.Label(self.main_frame, text="静夜思",
                                   font=('KaiTi', 16, 'bold'),
                                   fg=self.COLORS['gold'], bg=bg)
        self.title_label.pack(pady=(3, 2))
        
        self.author_label = tk.Label(self.main_frame, text="李白",
                                    font=('KaiTi', 10),
                                    fg=self.COLORS['text_dim'], bg=bg)
        self.author_label.pack()
        
        # 诗词内容
        self.poem_frame = tk.Frame(self.main_frame, bg=bg)
        self.poem_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 5))
        
        self.poem_labels = []
        
        # 底部提示
        footer = tk.Frame(self.main_frame, bg=bg)
        footer.pack(fill=tk.X)
        
        tk.Label(footer, text="双击换一首 · 右键菜单",
                font=('Microsoft YaHei', 7),
                fg=self.COLORS['text_dim'], bg=bg).pack()
        
    def _load_tang_poems(self):
        """加载唐诗"""
        if self._tang_poems is not None:
            return self._tang_poems
        self._tang_poems = []
        if self.tang_path.exists():
            for f in list(self.tang_path.glob("poet.song.*.json"))[:30]:
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
        if self.song_path.exists():
            for f in list(self.song_path.glob("ci.song.*.json"))[:15]:
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
    
    def _get_daily_poem(self):
        """获取每日诗词"""
        today = datetime.now()
        seed = today.year * 10000 + today.month * 100 + today.day
        
        poems = self._load_tang_poems() + self._load_song_poems()
        if not poems:
            return None
        
        random.seed(seed)
        return random.choice(poems)
    
    def _load_poem(self, random_mode=False):
        """加载诗词"""
        if random_mode:
            poems = self._load_tang_poems() + self._load_song_poems()
            if poems:
                self.current_poem = random.choice(poems)
        else:
            self.current_poem = self._get_daily_poem()
        
        if self.current_poem:
            self._display_poem(self.current_poem)
    
    def _display_poem(self, poem):
        """显示诗词"""
        if not poem:
            return
        
        # 清空旧内容
        for label in self.poem_labels:
            label.destroy()
        self.poem_labels.clear()
        
        # 更新信息
        self.type_label.config(text=f"【{poem.get('type', '唐诗')}】")
        self.title_label.config(text=poem.get('title', '无题'))
        self.author_label.config(text=poem.get('author', '佚名'))
        
        # 显示诗句
        paragraphs = poem.get('paragraphs', [])
        for line in paragraphs:
            label = tk.Label(self.poem_frame, text=line,
                           font=('KaiTi', 12),
                           fg=self.COLORS['text'], bg=self.COLORS['bg'])
            label.pack(anchor='w', pady=1)
            self.poem_labels.append(label)
    
    def _refresh(self):
        """刷新诗词"""
        self._load_poem(random_mode=True)
    
    def _start_drag(self, event):
        """开始拖动"""
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['dragging'] = True
    
    def _on_drag(self, event):
        """拖动中"""
        if self.drag_data['dragging']:
            dx = event.x - self.drag_data['x']
            dy = event.y - self.drag_data['y']
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")
    
    def _stop_drag(self, event):
        """停止拖动"""
        self.drag_data['dragging'] = False
    
    def _show_menu(self, event):
        """显示右键菜单"""
        menu = tk.Menu(self.root, tearoff=0,
                      bg=self.COLORS['bg'],
                      fg=self.COLORS['text'],
                      activebackground=self.COLORS['gold_dark'],
                      activeforeground=self.COLORS['text'],
                      font=('Microsoft YaHei', 9))
        
        menu.add_command(label="  换一首  ", command=self._refresh)
        menu.add_separator()
        menu.add_command(label="  只看唐诗  ", command=lambda: self._filter_type('唐诗'))
        menu.add_command(label="  只看宋词  ", command=lambda: self._filter_type('宋词'))
        menu.add_command(label="  随机诗词  ", command=lambda: self._load_poem(True))
        menu.add_separator()
        menu.add_command(label="  开机自启  ", command=self._set_autostart)
        menu.add_command(label="  退出  ", command=self.root.destroy)
        
        menu.post(event.x_root, event.y_root)
    
    def _filter_type(self, poem_type):
        """按类型筛选"""
        if poem_type == '唐诗':
            poems = self._load_tang_poems()
        else:
            poems = self._load_song_poems()
        
        if poems:
            self.current_poem = random.choice(poems)
            self._display_poem(self.current_poem)
    
    def _set_autostart(self):
        """设置开机自启"""
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                script_path = str(Path(__file__).resolve())
                winreg.SetValueEx(reg_key, "FloatingPoetry", 0, winreg.REG_SZ, 
                                 f'pythonw "{script_path}"')
            
            tk.messagebox.showinfo("成功", "已设置开机自启")
        except Exception as e:
            tk.messagebox.showerror("失败", f"设置失败: {e}")
    
    def run(self):
        """运行"""
        self.root.mainloop()


def main():
    app = FloatingPoetry()
    app.run()


if __name__ == "__main__":
    main()