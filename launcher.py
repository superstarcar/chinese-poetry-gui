#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诗词雅韵启动器 - GUI版本选择器
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os


class LauncherGUI:
    """启动器GUI"""
    
    COLORS = {
        'bg': '#0d0d0d',
        'card': '#1a1a1a',
        'gold': '#c9a959',
        'gold_light': '#e8d5a3',
        'text': '#f5f5f5',
        'text_dim': '#666666',
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("诗词雅韵")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS['bg'])
        
        self._create_ui()
        
    def _create_ui(self):
        """创建界面"""
        # 标题
        title_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        title_frame.pack(pady=30)
        
        tk.Label(title_frame,
                text="◈",
                font=('KaiTi', 24),
                fg=self.COLORS['gold'],
                bg=self.COLORS['bg']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(title_frame,
                text="诗 词 雅 韵",
                font=('KaiTi', 32, 'bold'),
                fg=self.COLORS['gold'],
                bg=self.COLORS['bg']).pack(side=tk.LEFT)
        
        tk.Label(title_frame,
                text="◈",
                font=('KaiTi', 24),
                fg=self.COLORS['gold'],
                bg=self.COLORS['bg']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(self.root,
                text="品味千年文化 · 感悟诗意人生",
                font=('Microsoft YaHei', 11),
                fg=self.COLORS['text_dim'],
                bg=self.COLORS['bg']).pack()
        
        # 按钮区域
        btn_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        btn_frame.pack(pady=30)
        
        buttons = [
            ("标准版 GUI", "Classic dark theme", self.run_standard),
            ("豪华版 GUI", "Gradient background", self.run_luxury),
            ("命令行版", "Command line interface", self.run_cli),
            ("功能演示", "Feature demonstration", self.run_demo),
        ]
        
        for text, desc, cmd in buttons:
            self._create_button(btn_frame, text, desc, cmd).pack(pady=8)
        
        # 底部
        tk.Label(self.root,
                text="数据来源: chinese-poetry | 共收录 275,301 首诗词",
                font=('Microsoft YaHei', 9),
                fg=self.COLORS['text_dim'],
                bg=self.COLORS['bg']).pack(side=tk.BOTTOM, pady=15)
        
    def _create_button(self, parent, text, desc, command):
        """创建按钮"""
        frame = tk.Frame(parent, bg=self.COLORS['card'], padx=20, pady=10)
        
        btn = tk.Button(frame,
                       text=f"  {text}  ",
                       font=('Microsoft YaHei', 12),
                       fg=self.COLORS['text'],
                       bg=self.COLORS['card'],
                       activebackground=self.COLORS['gold'],
                       activeforeground=self.COLORS['bg'],
                       relief=tk.FLAT,
                       padx=30,
                       pady=8,
                       cursor='hand2',
                       command=command)
        btn.pack()
        
        tk.Label(frame,
                text=desc,
                font=('Microsoft YaHei', 9),
                fg=self.COLORS['text_dim'],
                bg=self.COLORS['card']).pack()
        
        # 悬停效果
        def on_enter(e):
            btn.configure(fg=self.COLORS['gold'])
        def on_leave(e):
            btn.configure(fg=self.COLORS['text'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return frame
    
    def run_standard(self):
        """运行标准版"""
        self.root.withdraw()
        try:
            subprocess.run([sys.executable, 'poetry_gui.py'], 
                          cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            print(f"Error: {e}")
        self.root.deiconify()
    
    def run_luxury(self):
        """运行豪华版"""
        self.root.withdraw()
        try:
            subprocess.run([sys.executable, 'poetry_gui_luxury.py'],
                          cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            print(f"Error: {e}")
        self.root.deiconify()
    
    def run_cli(self):
        """运行命令行版"""
        self.root.withdraw()
        try:
            subprocess.run([sys.executable, 'daily_poetry.py'],
                          cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            print(f"Error: {e}")
        self.root.deiconify()
    
    def run_demo(self):
        """运行演示"""
        self.root.withdraw()
        try:
            subprocess.run([sys.executable, 'demo.py'],
                          cwd=os.path.dirname(os.path.abspath(__file__)))
        except Exception as e:
            print(f"Error: {e}")
        self.root.deiconify()
    
    def run(self):
        """运行"""
        self.root.mainloop()


if __name__ == "__main__":
    app = LauncherGUI()
    app.run()