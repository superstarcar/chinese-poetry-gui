#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诗词雅韵 - 功能演示脚本
"""

import sys
import io

# 设置编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def show_banner():
    """显示横幅"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         ◈  诗 词 雅 韵  ◈                                    ║
║                                                               ║
║           品味千年文化 · 感悟诗意人生                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)


def show_menu():
    """显示菜单"""
    print("""
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   请选择要运行的程序：                                      │
│                                                             │
│   [1] 标准版GUI    - 经典深色主题，稳定流畅                 │
│   [2] 豪华版GUI    - 渐变背景动画，更精美的设计             │
│   [3] 命令行版     - 无GUI依赖，适合服务器                  │
│   [4] 运行测试     - 测试所有功能                           │
│   [5] 查看帮助     - 显示详细使用说明                       │
│   [0] 退出                                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    """)


def run_standard_gui():
    """运行标准版GUI"""
    print("\n正在启动标准版GUI...")
    try:
        from poetry_gui import main
        main()
    except ImportError:
        print("错误：无法导入标准版GUI模块")
    except Exception as e:
        print(f"启动失败：{e}")


def run_luxury_gui():
    """运行豪华版GUI"""
    print("\n正在启动豪华版GUI...")
    try:
        from poetry_gui_luxury import main
        main()
    except ImportError:
        print("错误：无法导入豪华版GUI模块")
    except Exception as e:
        print(f"启动失败：{e}")


def run_cli():
    """运行命令行版"""
    print("\n正在运行命令行版...")
    try:
        from daily_poetry import main
        main()
    except ImportError:
        print("错误：无法导入命令行模块")
    except Exception as e:
        print(f"运行失败：{e}")


def run_tests():
    """运行测试"""
    print("\n正在运行测试...")
    try:
        from test_daily_poetry import test_basic_functionality, test_history_functionality, test_data_loading
        test_basic_functionality()
        test_history_functionality()
        test_data_loading()
        print("\n所有测试完成！")
    except ImportError:
        print("错误：无法导入测试模块")
    except Exception as e:
        print(f"测试失败：{e}")


def show_help():
    """显示帮助"""
    print("""
┌─────────────────────────────────────────────────────────────┐
│                        使用帮助                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【标准版GUI】 poetry_gui.py                                │
│    - 经典深色主题，界面简洁                                 │
│    - 适合日常使用                                           │
│                                                             │
│  【豪华版GUI】 poetry_gui_luxury.py                         │
│    - 渐变背景，更精美的装饰                                 │
│    - 适合追求高品质体验的用户                               │
│                                                             │
│  【命令行版】 daily_poetry.py                               │
│    - 无图形界面依赖                                         │
│    - 适合服务器或脚本调用                                   │
│                                                             │
│    常用命令：                                               │
│      python daily_poetry.py                 # 今天的推荐    │
│      python daily_poetry.py --date 2025-01-01  # 指定日期   │
│      python daily_poetry.py --type 唐诗     # 只看唐诗      │
│      python daily_poetry.py --type 宋词     # 只看宋词      │
│      python daily_poetry.py --history       # 查看历史      │
│      python daily_poetry.py --save          # 保存推荐      │
│                                                             │
│  【测试脚本】 test_daily_poetry.py                          │
│    - 验证所有功能是否正常                                   │
│    - 显示数据统计信息                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    """)


def main():
    """主函数"""
    show_banner()
    
    while True:
        show_menu()
        choice = input("请输入选择 (0-5): ").strip()
        
        if choice == '0':
            print("\n感谢使用诗词雅韵，再见！\n")
            break
        elif choice == '1':
            run_standard_gui()
        elif choice == '2':
            run_luxury_gui()
        elif choice == '3':
            run_cli()
        elif choice == '4':
            run_tests()
        elif choice == '5':
            show_help()
        else:
            print("\n无效的选择，请重新输入。")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    main()