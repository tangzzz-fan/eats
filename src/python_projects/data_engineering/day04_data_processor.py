import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def process_and_plot_data(csv_path: str, output_image_path: str = "output_chart.png") -> None:
    """
    Day 4: 文件、异常与上下文管理 - 数据处理与可视化
    
    目标：
    1. 从指定的 `csv_path` 中读取数据。
    2. 处理文件不存在的异常（FileNotFoundError），打印友好的提示并优雅退出。
    3. 数据读取成功后，检测是否存在缺失值（Null/NaN），并进行填充处理（例如用前一个有效值填充或用均值填充）。
    4. 使用 matplotlib 生成一张简单的折线图。
       - X轴为日期（假设 CSV 中有名为 "Date" 的列）
       - Y轴为数值（假设 CSV 中有名为 "Value" 的列）
    5. 将折线图保存到 `output_image_path` 路径。
    
    提示与关键点：
    - 使用 `try...except FileNotFoundError:` 捕获文件读取错误。
    - 使用 `pd.read_csv(csv_path)` 读取数据。
    - 使用 `df.isna().sum()` 可以查看每列有多少缺失值。
    - 使用 `df.ffill()`（前向填充，即用上一行的值填充当前缺失值）或者 `df['Value'].fillna(value)` 处理缺失。
    - 使用 `plt.figure()`, `plt.plot()`, `plt.title()`, `plt.savefig()`, `plt.close()` 操作图表。
    
    知识体系清单：
    - 结构化异常管理 try-except-else-finally 处理控制流程。
    - 使用 Pandas 进行 DataFrame 加载、探查缺失值、缺失值补全（ffill/bfill）。
    - Matplotlib 的画图布局、属性设定、保存图像与关闭清除。
    
    工程实践避坑指南：
    - 图像对象累积泄漏：如果在一批数据循环处理画图时不调用 `plt.close()`，Matplotlib 的画布实例会保留在内存中不释放，从而导致内存慢慢占满。
    - 无 UI 终端绘图崩溃：在服务器环境运行 Matplotlib 绘图易因没有 GUI 后端报错，应在最前端引入并调用 `matplotlib.use('Agg')` 进行离线图渲染。
    
    :param csv_path: CSV 数据文件路径。
    :param output_image_path: 生成折线图的保存路径。
    """
    # 步骤 A: 用 try-except 块包装 pandas 读取 CSV 的过程，捕获 FileNotFoundError
    try:
        # TODO: 1. 使用 pd.read_csv 读取 CSV 文件
        # df = ...
        # raise NotImplementedError("Please implement process_and_plot_data")
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file at '{csv_path}' was not found. Please verify the path.")
        # 直接返回，不继续往下执行
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    print("Data loaded successfully. Starting analysis...")
    
    # 步骤 B: 缺失值处理
    # 假设 CSV 包含 'Date' 和 'Value' 两列。我们来看看 'Value' 是否包含 NaN
    # TODO: 2. 检查是否有缺失值，并进行填充（推荐使用 ffill() 或 fillna(0)）
    df['Value'] = df['Value'].ffill()

    # 假设 'Date' 列是日期格式，'Value' 列是数值格式
    # 检查缺失值
    print("Missing values in 'Value' column:")
    print(df.isna().sum())
    
    # 转换日期列
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 步骤 C: 数据可视化
    # 我们使用 matplotlib 来画一条折线图
    # TODO: 3. 使用 plt.figure() 初始化图表
    # TODO: 4. 用 plt.plot(df['Date'], df['Value'], marker='o', color='b', label='Value trend') 画图
    # TODO: 5. 添加标题和坐标轴标签 (plt.title, plt.xlabel, plt.ylabel)
    # TODO: 6. 开启网格 plt.grid(True)
    # TODO: 7. 添加图例 plt.legend()
    # TODO: 8. 自动调整布局 plt.tight_layout()
    # TODO: 9. 保存到 output_image_path (plt.savefig)
    # TODO: 10. 释放内存资源 (plt.close())
    plt.figure()
    
    plt.plot(df['Date'], df['Value'], marker='o', color='b', label='Value trend')
    plt.title('Value Trend')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_image_path)
    plt.close()
    
    # 以下为提示，实际代码由你完成：
    print(f"Chart successfully saved to {output_image_path}")

if __name__ == "__main__":
    # 本地跑一下测试，默认应该提示文件不存在    
    print("Testing data processor...")
    # process_and_plot_data("non_existent_file.csv")
    process_and_plot_data("data/sample.csv")
