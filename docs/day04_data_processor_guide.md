# Day 04：数据处理与可视化 (Pandas & Matplotlib) - 快速上手指南

本指南旨在帮助你快速掌握 `Day 04` 练习（[day04_data_processor.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day04_data_processor.py)）所需的数据清洗与无 GUI 后端图像渲染技巧。

---

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
| --- | --- | --- |
| `ffill()` 前向填充 | 用上一行的有效值填补当前 `NaN` | 若首行就是 `NaN`，前面没有值可借，填充后依然是 `NaN` |
| `pd.to_datetime()` | 把字符串列转为真正的日期类型 | 不转换的话日期只是普通字符串，排序和画图都会按字典序错乱 |
| `matplotlib.use('Agg')` | 无 GUI 环境必须指定离线渲染后端 | 必须写在 `import matplotlib.pyplot` **之前**，否则不生效仍会崩溃 |
| `plt.close()` | 画完图后释放画布内存 | 循环画图漏掉它会内存泄漏；与 `plt.savefig()` 的顺序不能颠倒 |
| 捕获 `FileNotFoundError` | 文件不存在时打印提示并提前返回 | 要 `return` 终止函数，否则后续代码会继续操作不存在的 `df` |

---

## 1. 核心任务目标

编写函数 `process_and_plot_data(csv_path: str, output_image_path: str = "output_chart.png")`：
1. **异常处理**：读取 CSV 文件，优雅捕获 `FileNotFoundError` 并打印友情提示，不崩溃。
2. **缺失值填充**：检测 DataFrame 中的 NaN 缺失值，并使用前向填充 (`ffill()`) 补全。
3. **时间解析**：将 `'Date'` 列转化为 datetime 日期对象。
4. **图像绘制与导出**：使用 Matplotlib 绘制趋势折线图，设置网格、标题、坐标轴标签与图例，导出为 PNG 并释放内存。

---

## 2. 核心知识点详解

### 2.1 结构化文件读取与异常捕获
```python
import pandas as pd

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"Error: The file at '{csv_path}' was not found.")
    return
```

注意 `except` 块里的 `return` 不可省略：捕获异常后必须立刻退出函数，否则程序会继续往下执行，对一个并未成功创建的 `df` 变量操作，抛出更难排查的 `NameError`。

### 2.2 Pandas 缺失值检测与填充
* **查看缺失数量**：`df.isna().sum()`
* **前向填充 (`ffill`)**：用上一行的有效数值填充当前缺失的 `NaN`。注意它的局限：如果缺失值出现在第一行，前面没有任何可借用的值，填充后该行仍然是 `NaN`（可配合 `bfill()` 兜底）。
* **日期解析 (`to_datetime`)**：`pd.read_csv` 读进来的日期列默认只是字符串，`pd.to_datetime()` 会把它转成真正的 `datetime64` 类型，之后按时间排序、画图定坐标轴才不会出错。
```python
df['Value'] = df['Value'].ffill()
df['Date'] = pd.to_datetime(df['Date'])
```

### 2.3 Matplotlib 离线渲染与内存释放

#### 避坑指南一：服务器/终端无 UI 绘图崩溃
在没有 GUI 窗口的环境下运行 Matplotlib，必须在导入 `plt` 前指定离线渲染后端：
```python
import matplotlib
matplotlib.use('Agg')  # 设置为离线渲染模式
import matplotlib.pyplot as plt
```

#### 避坑指南二：图像画布累积内存泄漏
如果在循环中画图不释放画布，内存会持续增长。绘制完成后必须调用 `plt.close()`：

```python
plt.figure()
plt.plot(df['Date'], df['Value'], marker='o', color='b', label='Value trend')
plt.title('Value Trend')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(output_image_path)
plt.close()  # 关键：清空并关闭当前 figure 释放内存
```

---

## 3. 单元测试验证

完成代码后，运行测试验证：
```bash
.venv/bin/pytest tests/test_day04_data_processor.py
```
