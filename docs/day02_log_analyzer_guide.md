# Day 02：内置模块与工具练习 (日志分析与归档) - 快速上手指南

本指南旨在帮助你快速掌握 `Day 02` 练习（[day02_log_analyzer.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day02_log_analyzer.py)）所需的文件系统操作、时间格式化与容错处理。

---

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
|--------|------------|---------------|
| `os.listdir` 的返回值 | 只返回**文件名**，不是完整路径 | 后续 `isfile`/`open`/`move` 都必须先用 `os.path.join(target_dir, f)` 拼接完整路径，否则会找不到文件 |
| 过滤 `.log` 时的 `isfile` 判断 | 目录名也可能以 `.log` 结尾 | 只用 `endswith('.log')` 会把同名子目录误当文件，必须叠加 `os.path.isfile()` 排除 |
| 统计 `"ERROR"` 行 | 用 `in` 做子串匹配，**区分大小写** | `"error"` 或 `"Error"` 不计入；也不要用 `line == "ERROR"` 做整行相等判断 |
| `open(..., errors="ignore")` | 遇到非法字节直接丢弃而不是崩溃 | 漏写 `errors="ignore"` 时，日志里混入乱码会抛 `UnicodeDecodeError` 中断整个统计 |
| `os.makedirs(exist_ok=True)` | 目录已存在时不报错、静默跳过 | 同一天重复运行脚本时归档目录必然已存在，漏写会抛 `FileExistsError` |
| `shutil.move` 的覆盖行为 | 目标路径已存在同名文件时会覆盖（Unix） | 同一天归档多个同名文件会互相覆盖，只保留最后一个 |

---

## 1. 核心任务目标

编写函数 `analyze_and_archive_logs(target_dir: str = ".") -> dict[str, int]`：
1. **遍历目录**：扫描 `target_dir` 目录下所有的 `.log` 文件。
2. **日志统计**：逐行读取 `.log` 文件，统计包含 `"ERROR"`（区分大小写）的行数。
3. **安全创建文件夹**：获取当前日期格式 `YYYYMMDD`（如 `archive_20260722`），并创建该归档文件夹。
4. **文件移动**：将已处理过的 `.log` 文件移动到归档文件夹中。
5. **返回结果**：返回格式为 `{"a.log": 5, "b.log": 0}` 的字典。

---

## 2. 核心知识点详解

### 2.1 目录遍历与路径拼接 (`os`)
```python
import os

# 列出 target_dir 目录下的所有文件名
all_files = os.listdir(target_dir)

# 过滤出 .log 文件且必须是普通文件（排除文件夹）
log_files = [
    f for f in all_files 
    if f.endswith('.log') and os.path.isfile(os.path.join(target_dir, f))
]
```

注意 `os.listdir` 返回的每个 `f` 只是文件名（如 `a.log`），不含目录前缀；`os.path.isfile` 接收相对/绝对路径，所以判断前必须先用 `os.path.join(target_dir, f)` 拼出完整路径，否则脚本在非 `target_dir` 目录下运行时会误判。

### 2.2 日期格式化 (`datetime`)
```python
from datetime import datetime

# 获取当前日期并转为 YYYYMMDD 字符串
today_str = datetime.now().strftime("%Y%m%d")
archive_dir_name = f"archive_{today_str}"
```

### 2.3 容错性目录创建与文件移动
* **创建目录容错 (`exist_ok=True`)**：如果归档文件夹已存在，不会抛出 `FileExistsError`。
* **文件移动 (`shutil.move`)**：
```python
import shutil

archive_dir_path = os.path.join(target_dir, archive_dir_name)
os.makedirs(archive_dir_path, exist_ok=True)

# 移动文件
dest_path = os.path.join(archive_dir_path, filename)
shutil.move(src_path, dest_path)
```

这里的 `src_path` 同样要用 `os.path.join(target_dir, filename)` 拼出完整路径（参考 2.1 节）。另外 `shutil.move` 在目标文件已存在时会直接覆盖（Unix 行为），同一天多次归档同名文件只保留最后一个，测试时应避免依赖前一次运行的残留文件。

### 2.4 文件安全读取与编码防崩溃
读取日志文件时，可能包含乱码或特殊中文字符，必须显式指定 `encoding="utf-8"` 和 `errors="ignore"` 避免抛出 `UnicodeDecodeError`：
```python
error_count = 0
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if "ERROR" in line:
            error_count += 1
```

其中 `errors="ignore"` 的作用是：遇到无法用 UTF-8 解码的字节时直接丢弃该字节继续读，而不是抛出异常。代价是乱码内容会静默丢失，但对「只统计 ERROR 行」的场景完全够用。

---

## 3. 单元测试验证

完成代码后，运行测试验证：
```bash
.venv/bin/pytest tests/test_day02_log_analyzer.py
```
