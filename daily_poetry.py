#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日诗词推荐脚本
基于 chinese-poetry 数据库的每日诗词推荐功能
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path


class DailyPoetry:
    """每日诗词推荐类"""
    
    def __init__(self, base_path=None, history_file=None):
        """初始化
        
        Args:
            base_path: chinese-poetry 数据库的路径，默认为当前目录
            history_file: 历史记录文件路径
        """
        if base_path is None:
            base_path = Path(__file__).parent
        self.base_path = Path(base_path)
        
        # 数据目录
        self.tang_poetry_path = self.base_path / "全唐诗"
        self.song_poetry_path = self.base_path / "宋词"
        
        # 历史记录文件
        if history_file is None:
            history_file = self.base_path / "daily_poetry_history.json"
        self.history_file = Path(history_file)
        
        # 缓存
        self._tang_poems = None
        self._song_poems = None
        self._history = None
        
    def _load_tang_poems(self):
        """加载唐诗数据"""
        if self._tang_poems is not None:
            return self._tang_poems
            
        self._tang_poems = []
        tang_files = list(self.tang_poetry_path.glob("poet.song.*.json"))
        
        for file_path in tang_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    poems = json.load(f)
                    for poem in poems:
                        poem['type'] = '唐诗'
                        self._tang_poems.append(poem)
            except Exception as e:
                print(f"加载文件 {file_path} 时出错: {e}")
                
        return self._tang_poems
    
    def _load_song_poems(self):
        """加载宋词数据"""
        if self._song_poems is not None:
            return self._song_poems
            
        self._song_poems = []
        song_files = list(self.song_poetry_path.glob("ci.song.*.json"))
        
        for file_path in song_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    poems = json.load(f)
                    for poem in poems:
                        poem['type'] = '宋词'
                        # 宋词使用 rhythmic 作为标题
                        if 'title' not in poem and 'rhythmic' in poem:
                            poem['title'] = poem['rhythmic']
                        self._song_poems.append(poem)
            except Exception as e:
                print(f"加载文件 {file_path} 时出错: {e}")
                
        return self._song_poems
    
    def get_all_poems(self):
        """获取所有诗词"""
        tang_poems = self._load_tang_poems()
        song_poems = self._load_song_poems()
        return tang_poems + song_poems
    
    def get_daily_poem(self, date=None, poem_type=None):
        """获取每日推荐诗词
        
        Args:
            date: 指定日期，默认为今天。格式：YYYY-MM-DD 或 datetime 对象
            poem_type: 诗词类型，可选 '唐诗'、'宋词' 或 None（随机）
            
        Returns:
            dict: 推荐的诗词
        """
        # 处理日期
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        # 使用日期作为随机种子，确保同一天每次运行都得到相同的诗
        date_seed = date.year * 10000 + date.month * 100 + date.day
        
        # 获取诗词列表
        if poem_type == '唐诗':
            poems = self._load_tang_poems()
        elif poem_type == '宋词':
            poems = self._load_song_poems()
        else:
            poems = self.get_all_poems()
        
        if not poems:
            return None
        
        # 使用日期种子选择诗词
        random.seed(date_seed)
        selected_poem = random.choice(poems)
        
        return selected_poem
    
    def format_poem(self, poem, show_type=True):
        """格式化诗词输出
        
        Args:
            poem: 诗词数据
            show_type: 是否显示诗词类型
            
        Returns:
            str: 格式化后的诗词文本
        """
        if not poem:
            return "没有找到诗词"
        
        lines = []
        
        # 标题
        title = poem.get('title', '无题')
        if show_type:
            poem_type = poem.get('type', '')
            lines.append(f"【{poem_type}】{title}")
        else:
            lines.append(f"【{title}】")
        
        # 作者
        author = poem.get('author', '佚名')
        lines.append(f"作者：{author}")
        
        # 如果有词牌名（宋词）
        if 'rhythmic' in poem and poem['rhythmic'] != title:
            lines.append(f"词牌：{poem['rhythmic']}")
        
        lines.append("")  # 空行
        
        # 诗句
        paragraphs = poem.get('paragraphs', [])
        for paragraph in paragraphs:
            lines.append(paragraph)
        
        return '\n'.join(lines)
    
    def get_daily_recommendation(self, date=None, poem_type=None):
        """获取每日推荐（格式化输出）
        
        Args:
            date: 指定日期，默认为今天
            poem_type: 诗词类型
            
        Returns:
            str: 格式化后的每日推荐
        """
        poem = self.get_daily_poem(date, poem_type)
        date_str = date if isinstance(date, str) else (date.strftime('%Y-%m-%d') if date else datetime.now().strftime('%Y-%m-%d'))
        
        header = f"每日诗词推荐 - {date_str}"
        separator = "=" * 40
        
        content = self.format_poem(poem)
        
        return f"{header}\n{separator}\n{content}"
    
    def _load_history(self):
        """加载历史记录"""
        if self._history is not None:
            return self._history
            
        self._history = {}
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self._history = json.load(f)
            except Exception as e:
                print(f"加载历史记录失败: {e}")
                self._history = {}
        
        return self._history
    
    def _save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self._history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")
    
    def save_to_history(self, date=None, poem=None, poem_type=None):
        """保存推荐到历史记录
        
        Args:
            date: 日期，默认为今天
            poem: 诗词数据
            poem_type: 诗词类型
        """
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        date_str = date.strftime('%Y-%m-%d')
        
        if poem is None:
            poem = self.get_daily_poem(date, poem_type)
        
        if poem:
            history = self._load_history()
            history[date_str] = {
                'title': poem.get('title', '无题'),
                'author': poem.get('author', '佚名'),
                'type': poem.get('type', ''),
                'rhythmic': poem.get('rhythmic', ''),
                'paragraphs': poem.get('paragraphs', [])
            }
            self._history = history
            self._save_history()
    
    def get_history(self, days=7):
        """获取历史记录
        
        Args:
            days: 获取最近几天的记录，默认7天
            
        Returns:
            dict: 历史记录，格式 {日期: 诗词信息}
        """
        history = self._load_history()
        result = {}
        
        today = datetime.now()
        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            if date_str in history:
                result[date_str] = history[date_str]
        
        return result
    
    def format_history(self, days=7):
        """格式化历史记录
        
        Args:
            days: 显示最近几天的记录
            
        Returns:
            str: 格式化后的历史记录
        """
        history = self.get_history(days)
        
        if not history:
            return f"最近 {days} 天没有推荐记录"
        
        lines = [f"最近 {days} 天的诗词推荐记录", "=" * 40]
        
        for date_str in sorted(history.keys(), reverse=True):
            poem_info = history[date_str]
            title = poem_info.get('title', '无题')
            author = poem_info.get('author', '佚名')
            poem_type = poem_info.get('type', '')
            
            lines.append(f"{date_str}: 【{poem_type}】{title} - {author}")
        
        return '\n'.join(lines)


def main():
    """主函数"""
    import argparse
    import sys
    import io
    
    # 设置标准输出编码为 UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description='每日诗词推荐')
    parser.add_argument('--date', type=str, help='指定日期，格式：YYYY-MM-DD')
    parser.add_argument('--type', type=str, choices=['唐诗', '宋词'], help='诗词类型')
    parser.add_argument('--list-types', action='store_true', help='列出可用的诗词类型')
    parser.add_argument('--history', action='store_true', help='显示历史记录')
    parser.add_argument('--days', type=int, default=7, help='显示历史记录的天数（默认7天）')
    parser.add_argument('--save', action='store_true', help='保存今天的推荐到历史记录')
    
    args = parser.parse_args()
    
    daily_poetry = DailyPoetry()
    
    if args.list_types:
        print("可用的诗词类型：")
        print("  - 唐诗")
        print("  - 宋词")
        return
    
    if args.history:
        history = daily_poetry.format_history(args.days)
        print(history)
        return
    
    # 获取每日推荐
    recommendation = daily_poetry.get_daily_recommendation(args.date, args.type)
    print(recommendation)
    
    # 保存到历史记录
    if args.save:
        daily_poetry.save_to_history(args.date, poem_type=args.type)
        print("\n已保存到历史记录")


if __name__ == "__main__":
    main()