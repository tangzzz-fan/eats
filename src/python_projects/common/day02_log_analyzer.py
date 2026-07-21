import os
import shutil
from datetime import datetime
from collections import defaultdict

def analyze_and_archive_logs(target_dir: str = ".") -> dict[str, int]:
    """
    Day 2: 常用内置模块与工具练习 - 日志分析与归档
    
    目标：
    1. 遍历 `target_dir` 目录（仅需查找当前层级，或使用 os.walk 递归查找，此处建议仅遍历当前层级的 .log 文件）。
    2. 对每个找到的 `.log` 文件，逐行读取内容。
    3. 统计每个日志文件中包含 "ERROR"（区分大小写）的行数。
    4. 创建一个以当前日期命名的归档文件夹，格式为 `archive_YYYYMMDD`（例如 `archive_20260721`）。
    5. 将所有处理过的 `.log` 文件移动到该归档文件夹中。
    6. 返回一个字典，键为文件名，值为其中 "ERROR" 的行数。
    
    提示与关键点：
    - `os.listdir(path)`：列出目录下的所有文件和文件夹。
    - `os.path.join(path, *paths)`：安全地拼接路径。
    - `os.path.exists(path)` 和 `os.makedirs(path, exist_ok=True)`：检查并创建目录。
    - `datetime.now().strftime("%Y%m%d")`：获取当前日期并格式化。
    - `shutil.move(src, dst)`：移动文件。
    - 编码问题：打开文件时建议指定 `encoding="utf-8"` 并使用 `errors="ignore"` 避免因乱码导致崩溃。
    
    知识体系清单：
    - `os.listdir` 与 `os.path.join` 组合下的路径遍历与拼接。
    - `datetime` 模块的时间获取与格式化转换。
    - `os.makedirs(..., exist_ok=True)` 文件夹创建容错机制。
    - 文件读写安全流（with open）与编码防崩溃处理。
    
    工程实践避坑指南：
    - 编码解析崩溃：日志中带有中文字符或异常机器码时，如果不显式设置 `encoding="utf-8"`，在 Windows 等平台默认使用 GBK 读取会导致 UnicodeDecodeError。应统一声明 UTF-8 并配上 `errors="ignore"`。
    - 归档搜索死循环：在搜索 `.log` 时，如果生成的归档目录也是同级子目录，遍历时必须显式避开该归档目录，防止将已被移入归档夹内的 log 重复读取并产生逻辑死循环。
    
    :param target_dir: 目标查找目录，默认为当前目录 "."。
    :return: 统计字典，格式为 { "a.log": 5, "b.log": 0 }
    """
    # 1. 获取当前日期字符串，格式为 YYYYMMDD
    today_str = datetime.now().strftime("%Y%m%d")
    archive_dir_name = f"archive_{today_str}"
    archive_dir_path = os.path.join(target_dir, archive_dir_name)
    
    # 用于存放结果的字典
    error_counts: dict[str, int] = {}
    
    # 2. 找到 target_dir 下所有以 .log 结尾的文件
    # 注意：我们要忽略刚刚创建的归档目录中的文件，或者只处理 target_dir 根目录下的文件
    try:
        all_files = os.listdir(target_dir)
    except FileNotFoundError:
        print(f"Error: Directory '{target_dir}' not found.")
        return error_counts

    log_files = [f for f in all_files if f.endswith('.log') and os.path.isfile(os.path.join(target_dir, f))]
    
    if not log_files:
        print("No .log files found to analyze.")
        return error_counts

    # TODO: 请完成以下步骤的实现
    
    # 步骤 A: 确保归档目录存在，如果不存在则使用 os.makedirs 创建它
    
    # 步骤 B: 循环遍历每一个 log_files
    for filename in log_files:
        file_path = os.path.join(target_dir, filename)
        error_count = 0
        
        # 步骤 B-1: 安全地打开文件并逐行读取，统计包含 "ERROR" 的行数
        # 提示：使用 with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        #       for line in f: ...
        
        
        # 步骤 B-2: 将统计结果存入 error_counts 字典，键为文件名，值为错误行数
        
        
        # 步骤 B-3: 将处理完的日志文件移动到归档文件夹中
        # 提示：计算目标路径 dest_path = os.path.join(archive_dir_path, filename)
        #       使用 shutil.move(file_path, dest_path)
        pass

    return error_counts

if __name__ == "__main__":
    # 可以用于本地临时运行测试
    # 比如在当前目录下创建临时 log 文件，然后运行分析
    print("Testing log analyzer...")
    # 创建临时测试文件
    with open("test_debug.log", "w", encoding="utf-8") as f:
        f.write("INFO: Startup successful\nERROR: Failed to connect to DB\nDEBUG: Retrying...\nERROR: Port already in use\n")
    with open("test_info.log", "w", encoding="utf-8") as f:
        f.write("INFO: User login\nINFO: User logout\n")
        
    results = analyze_and_archive_logs(".")
    print("Analysis results:", results)
