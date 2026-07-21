import argparse
import sys
from python_projects.common.day02_log_analyzer import analyze_and_archive_logs

def main() -> None:
    """
    Day 5: 现代特性与工程实践 - 命令行工具设计
    
    目标：
    创建一个简单的命令行工具，用于执行项目的各种操作（例如分析日志等）。
    1. 使用 `argparse` 定义参数解析器。
    2. 支持 `--version` 或者 `-v` 参数，输出版本号（如 `python-projects version 1.0.0`）。
    3. 支持一个子命令 `analyze`，接收一个可选的路径参数 `--dir`（默认为 "."），并调用 `analyze_and_archive_logs`。
    
    提示与关键点：
    - `parser = argparse.ArgumentParser(description="...")`
    - `parser.add_argument('--version', action='version', version='python-projects 1.0.0')`
    - 使用 `parser.add_subparsers(dest='command', help='sub-command help')` 来添加子命令。
    - 在子命令中，可以用 `parser_analyze.add_argument('--dir', default='.', help='...')` 来定义目录参数。
    - 使用 `args = parser.parse_args()` 接收解析结果。
    
    知识体系清单：
    - argparse 的参数类型定义、默认值处理与子解释器（subparsers）分级。
    - `__name__ == "__main__"` 的脚本生命周期与代码复用控制保护。
    - 类型提示规范（在复杂函数参数上引入 Dict, List, Optional 方便静态检查工具静态验证）。
    
    工程实践避坑指南：
    - 空命令崩溃：设计子命令时若没有加上 `required=True`，在执行裸脚本时不会触发命令验证报错，而会继续往下执行导致读取不存在的变量引发 AttributeError。
    """
    # TODO: 1. 创建 ArgumentParser 对象
    # parser = argparse.ArgumentParser(description="Python Practice Project CLI")

    # TODO: 2. 添加全局的 --version / -v 参数
    # parser.add_argument('-v', '--version', action='version', version='python-projects 1.0.0')

    # TODO: 3. 创建子命令解析器
    # subparsers = parser.add_subparsers(dest='subcommand', required=True, help='Available commands')

    # TODO: 4. 添加 'analyze' 子命令
    # analyze_parser = subparsers.add_parser('analyze', help='Analyze and archive log files')
    # analyze_parser.add_argument('--dir', type=str, default='.', help='Directory containing log files (default: .)')

    # TODO: 5. 解析参数
    # args = parser.parse_args()

    # TODO: 6. 根据解析出来的子命令，分发执行逻辑
    # if args.subcommand == 'analyze':
    #     print(f"Starting log analysis in directory: {args.dir}")
    #     # 调用 day02 的分析函数并打印结果
    #     results = analyze_and_archive_logs(args.dir)
    #     print("Analysis results:", results)
    
    # 临时实现以保证没有报错：
    print("Please implement CLI parser logic in main().")
    sys.exit(0)

if __name__ == "__main__":
    main()
