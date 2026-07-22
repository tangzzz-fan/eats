# Day 05：现代特性与工程实践 (命令行工具设计) - 快速上手指南

本指南旨在帮助你快速掌握 `Day 05` 练习（[day05_cli.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day05_cli.py)）中的 `argparse` 命令行解析器设计与子命令分发逻辑。

---

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
| --- | --- | --- |
| `action='version'` | 由 `argparse` 自动打印版本号并退出，无需手写打印逻辑 | 不要写成普通字符串参数，否则 `-v` 不会自动退出 |
| `add_subparsers(required=True)` | 强制用户必须传入子命令 | 漏掉后裸运行脚本时 `args.subcommand` 为 `None`，引发 `AttributeError` |
| `dest='subcommand'` | 决定解析结果中子命令名的属性名 | 不设 `dest` 时子命令名不入 `args`，分发逻辑无处取值 |
| `--dir` 的 `default='.'` | 不传 `--dir` 时默认分析当前目录 | 默认值是字符串 `'.'`，不要误写成 `None` 再在业务代码里兜底 |
| `PYTHONPATH=src` 运行 | 项目采用 src 布局，需把 `src` 加入模块搜索路径 | 直接在根目录外运行或漏设时会 `ModuleNotFoundError` |

---

## 1. 核心任务目标

构建一个标准的 Python 命令行 CLI 工具：
1. **全局版本号参数 (`-v`, `--version`)**：输出 `python-practice 1.0.0` 并退出。
2. **必选子命令机制 (`subparsers`)**：要求运行者必须传入子命令。
3. **`analyze` 子命令**：接收可选参数 `--dir`（默认为当前目录 `.`），并调用 Day 02 的 `analyze_and_archive_logs(args.dir)` 函数。

---

## 2. 核心知识点详解

### 2.1 `argparse` 参数解析器搭建

```python
import argparse
from python_projects.common.day02_log_analyzer import analyze_and_archive_logs

def main() -> None:
    # 1. 创建解析器
    parser = argparse.ArgumentParser(description="Python Practice Project CLI")

    # 2. 添加全局 --version / -v 参数
    parser.add_argument('-v', '--version', action='version', version='python-practice 1.0.0')

    # 3. 创建子命令解析器，并设为必需 (required=True)
    subparsers = parser.add_subparsers(dest='subcommand', required=True, help='Available commands')

    # 4. 添加 'analyze' 子命令及其 --dir 参数
    analyze_parser = subparsers.add_parser('analyze', help='Analyze and archive log files')
    analyze_parser.add_argument('--dir', type=str, default='.', help='Directory containing log files')

    # 5. 解析参数
    args = parser.parse_args()

    # 6. 分发逻辑
    if args.subcommand == 'analyze':
        results = analyze_and_archive_logs(args.dir)
        print("Analysis results:", results)
```

注意第 2 步的 `action='version'`：这是一种特殊动作，`argparse` 在解析到 `-v`/`--version` 时会立即打印 `version=` 指定的字符串并调用 `sys.exit(0)`，因此 `main()` 中不需要（也不会执行到）为它编写的任何后续逻辑。而第 3 步的 `dest='subcommand'` 则决定了第 6 步分发时取值的属性名——两者必须对应。

---

### 2.2 工程实践避坑指南：空命令崩溃

如果在设计子命令时，没有在 `add_subparsers` 中显式指定 `required=True`：
* 当用户仅在终端运行 `python cli.py` 裸脚本时，不会触发命令帮助提示或报错；
* `args.subcommand` 会变成 `None`，若后续代码直接调用 `args.dir` 则会抛出 `AttributeError` 崩溃。

---

### 2.3 终端运行方式

由于脚本涉及包内模块的导入，请在项目根目录下通过 `PYTHONPATH=src` 运行：

本项目采用 src 布局，包代码位于 `src/python_projects/` 下而非项目根目录，Python 默认的模块搜索路径找不到它。`PYTHONPATH=src` 临时把 `src` 目录加入搜索路径，使 `from python_projects.common.day02_log_analyzer import ...` 这类导入能够成功；漏掉它会直接报 `ModuleNotFoundError: No module named 'python_projects'`。

```bash
# 查看帮助
PYTHONPATH=src python3 src/python_projects/common/day05_cli.py -h

# 查看版本
PYTHONPATH=src python3 src/python_projects/common/day05_cli.py -v

# 执行日志分析
PYTHONPATH=src python3 src/python_projects/common/day05_cli.py analyze --dir data
```

---

## 3. 单元测试验证

完成代码后，运行测试验证：
```bash
.venv/bin/pytest tests/test_day05_cli.py
```
