#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日诗词推荐功能测试
"""

import sys
import io
from pathlib import Path

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from daily_poetry import DailyPoetry


def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")
    
    daily_poetry = DailyPoetry()
    
    # 测试获取今天的推荐
    print("\n1. 测试获取今天的推荐")
    recommendation = daily_poetry.get_daily_recommendation()
    print(recommendation[:100] + "..." if len(recommendation) > 100 else recommendation)
    
    # 测试获取指定日期的推荐
    print("\n2. 测试获取指定日期的推荐")
    recommendation = daily_poetry.get_daily_recommendation("2025-01-01")
    print(recommendation[:100] + "..." if len(recommendation) > 100 else recommendation)
    
    # 测试指定类型的推荐
    print("\n3. 测试只推荐唐诗")
    recommendation = daily_poetry.get_daily_recommendation("2025-01-01", "唐诗")
    print(recommendation[:100] + "..." if len(recommendation) > 100 else recommendation)
    
    # 测试只推荐宋词
    print("\n4. 测试只推荐宋词")
    recommendation = daily_poetry.get_daily_recommendation("2025-01-01", "宋词")
    print(recommendation[:100] + "..." if len(recommendation) > 100 else recommendation)


def test_history_functionality():
    """测试历史记录功能"""
    print("\n\n测试历史记录功能...")
    
    daily_poetry = DailyPoetry()
    
    # 测试保存到历史记录
    print("\n1. 测试保存到历史记录")
    daily_poetry.save_to_history("2025-01-01", poem_type="唐诗")
    print("已保存 2025-01-01 的唐诗推荐")
    
    daily_poetry.save_to_history("2025-01-02", poem_type="宋词")
    print("已保存 2025-01-02 的宋词推荐")
    
    # 测试查看历史记录
    print("\n2. 测试查看历史记录")
    history = daily_poetry.format_history(7)
    print(history)


def test_data_loading():
    """测试数据加载"""
    print("\n\n测试数据加载...")
    
    daily_poetry = DailyPoetry()
    
    # 测试加载唐诗
    print("\n1. 测试加载唐诗数据")
    tang_poems = daily_poetry._load_tang_poems()
    print(f"成功加载 {len(tang_poems)} 首唐诗")
    
    # 测试加载宋词
    print("\n2. 测试加载宋词数据")
    song_poems = daily_poetry._load_song_poems()
    print(f"成功加载 {len(song_poems)} 首宋词")
    
    # 测试获取所有诗词
    print("\n3. 测试获取所有诗词")
    all_poems = daily_poetry.get_all_poems()
    print(f"总共 {len(all_poems)} 首诗词")


if __name__ == "__main__":
    print("每日诗词推荐功能测试")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_history_functionality()
        test_data_loading()
        
        print("\n\n所有测试完成！")
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()