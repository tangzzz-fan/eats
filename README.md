# Python 基础与科学计算、深度学习、具身智能综合实战项目

本工程是专为有一定基础的开发者定制的 Python 快速回顾练习库。通过本工程，你可以通过手动补全代码的方式，快速找回 Python 的编程语感并学习现代 Python 开发规范（如类型提示、依赖管理、pytest 测试等）。

本工程已使用 uv 完成初始化，并配置了虚拟环境。

所有练习均围绕一个统一的综合实战项目进行：**具身智能轨迹追踪模拟器 (Embodied AI Trajectory Tracker Simulator，简称 EATS)**。

---

## 总体安排与学习路线

为了方便你在侧边栏文件树中快速查找练习，每个模块的代码文件名都以 `dayXX_` 作为前缀进行标识，同时又合理地归纳在相应的领域包中：

| 天数 | 主题 | 模块位置与对应源码文件 |
|---|---|---|
| 第 1 天 | 核心语法速通 | 核心包：[day01_bank_account.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/core/day01_bank_account.py) |
| 第 2 天 | 常用内置模块与工具 | 通用包：[day02_log_analyzer.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day02_log_analyzer.py) |
| 第 3 天 | 高级特性与函数式编程 | 通用包：[day03_tools.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day03_tools.py) |
| 第 4 天 | 文件、异常与上下文管理 | 数据工程包：[day04_data_processor.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day04_data_processor.py) |
| 第 5 天 | 现代特性与工程实践 | 通用包：[day05_cli.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day05_cli.py) |
| 第 6 天 | 科学计算与 NumPy 深度复习 | 数据工程包：[day06_kmeans.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day06_kmeans.py) |
| 第 7 天 | Pandas 与时间序列数据工程 | 数据工程包：[day07_pipeline.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day07_pipeline.py) |
| 第 8 天 | 从 NumPy 到 PyTorch 与模块化设计 | 模型包：[day08_trainer.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day08_trainer.py) |
| 第 9 天 | PyTorch 工程级训练框架 | 模型包：[day09_network.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day09_network.py) |
| 第 10 天| 深度学习进阶：手动实现核心组件 | 模型包：[day10_attention.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day10_attention.py) |
| 第 11 天| 文本生成与轻量级 Transformer | 模型包：[day11_generator.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day11_generator.py) |
| 第 12 天| 具身智能仿真入门与反馈控制 | 仿真包：[day12_kinematics.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/simulation/day12_kinematics.py), [day12_controller.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/simulation/day12_controller.py), [day12_sim_loop.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/simulation/day12_sim_loop.py) |

> **提示**：每个模块对应的**详细知识点体系清单**与**工程实践避坑指南**，已全部写入对应代码文件的头部注释（docstring）中。请在编写对应代码时仔细阅读。

---

## 项目工程结构

```text
/Users/apple/Developments/Python Projects/
├── pyproject.toml              # 项目配置文件及依赖声明
├── README.md                   # 统一的中文学习指南与系统说明
├── config/
│   └── config.yaml             # 模型训练与机器人控制的超参数配置文件
├── data/
│   └── raw_odometry.csv        # 供 Day 7 进行 Pandas 数据清洗的原始遥测数据
├── src/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── utils.py            # 通用日志配置等工具
│   │   ├── day02_log_analyzer.py# Day 2: 日志分析与归档
│   │   ├── day03_tools.py      # Day 3: 重试装饰器与生成器
│   │   └── day05_cli.py        # Day 5: 命令行 CLI 入口
│   ├── core/
│   │   ├── __init__.py
│   │   └── day01_bank_account.py# Day 1: OOP BankAccount 练习
│   ├── data_engineering/
│   │   ├── __init__.py
│   │   ├── day04_data_processor.py# Day 4: 遥测数据读取与 matplotlib 绘图
│   │   ├── day06_kmeans.py     # Day 6: NumPy 空间轨迹点聚类
│   │   └── day07_pipeline.py   # Day 7: Pandas 传感器时序特征工程
│   ├── modeling/
│   │   ├── __init__.py
│   │   ├── day08_trainer.py    # Day 8: yaml 参数解析与训练器接口
│   │   ├── day09_network.py    # Day 9: Dataset 与 MLP 早停训练
│   │   ├── day10_attention.py  # Day 10: 手写 Multi-Head Attention 层
│   │   └── day11_generator.py  # Day 11: 自回归路径生成器
│   └── simulation/
│       ├── __init__.py
│       ├── day12_kinematics.py # Day 12: 差速机器人运动学数值积分
│       ├── day12_controller.py # Day 12: 闭环反馈 PID 控制
│       └── day12_sim_loop.py   # Day 12: 轨迹追踪仿真主循环
└── tests/
    ├── __init__.py
    ├── test_day01_bank_account.py# Day 1 单元测试
    ├── test_day02_log_analyzer.py# Day 2 单元测试
    ├── test_day03_tools.py      # Day 3 单元测试
    ├── test_day04_data_processor.py# Day 4 单元测试
    ├── test_day05_cli.py        # Day 5 单元测试
    ├── test_day06_kmeans.py     # Day 6 单元测试
    ├── test_day07_pipeline.py   # Day 7 单元测试
    ├── test_day08_trainer.py    # Day 8 单元测试
    ├── test_day09_network.py    # Day 9 单元测试
    ├── test_day10_attention.py  # Day 10 单元测试
    ├── test_day11_generator.py  # Day 11 单元测试
    └── test_day12_simulation.py # Day 12 单元测试
```

---

## 开发环境与常用指令

在当前工程根目录下，可以使用以下指令进行开发：

### 1. 激活虚拟环境
虚拟环境位于 `.venv` 目录中。激活方式如下：
- **macOS / Linux**:
  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 2. 运行单元测试
项目中已经写好了完备的 pytest 单元测试。一旦你补全了某个模块的 TODO，可以运行 pytest 进行验证：
```bash
pytest
```
未完成的模块由于抛出 `NotImplementedError` 会被 pytest 自动跳过（skipped），不会大面积报错影响调试。

### 3. 静态类型检查
在激活的虚拟环境中，使用 mypy 进行静态类型提示检查：
```bash
mypy src
```

---

## 每日实战执行指南

### 第 1 天：核心语法速通 (面向对象设计)
- **完成内容**：实现 [day01_bank_account.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/core/day01_bank_account.py) 中的 `BankAccount` 类，包含私有余额管理、只读属性定义、存取款校验与利息计算。
- **测试执行**：`pytest tests/test_day01_bank_account.py`

### 第 2 天：常用内置模块与工具 (文件系统与日期时间)
- **完成内容**：实现 [day02_log_analyzer.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day02_log_analyzer.py) 中的 `analyze_and_archive_logs`，搜索并统计 ERROR 日志行数，并以当前日期命名归档文件移动之。
- **测试执行**：`pytest tests/test_day02_log_analyzer.py`

### 第 3 天：高级特性与函数式编程 (装饰器与生成器)
- **完成内容**：实现 [day03_tools.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day03_tools.py) 中的异常重试装饰器 `@retry` 与无限斐波那契数列生成器。
- **测试执行**：`pytest tests/test_day03_tools.py`

### 第 4 天：文件、异常与上下文管理 (异常保护与数据可视化)
- **完成内容**：实现 [day04_data_processor.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day04_data_processor.py) 中的数据清洗与绘图，包含异常文件读取保护、NaN 前向填充及图表导出。
- **测试执行**：`pytest tests/test_day04_data_processor.py`

### 第 5 天：现代特性与工程实践 (CLI 入门与测试)
- **完成内容**：实现 [day05_cli.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day05_cli.py) 中的命令行界面工具，使用 `argparse` 构建命令行入口并支持子命令调用日志分析功能。
- **测试执行**：`pytest tests/test_day05_cli.py`

### 第 6 天：科学计算与 NumPy 深度复习 (空间点聚类)
- **完成内容**：实现 [day06_kmeans.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day06_kmeans.py) 中的聚类算法，使用广播机制无循环计算欧式距离矩阵，更新聚类中心并执行交替优化迭代。
- **测试执行**：`pytest tests/test_day06_kmeans.py`

### 第 7 天：Pandas 与时间序列数据工程 (时序特征工程)
- **完成内容**：实现 [day07_pipeline.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day07_pipeline.py) 中的遥测数据特征工程，包含时间索引构建、重采样插值、滑窗均值/标准差与滞后特征构造、时序顺序拆分训练集。
- **测试执行**：`pytest tests/test_day07_pipeline.py`

### 第 8 天：从 NumPy 到 PyTorch 与模块化设计 (训练器解耦)
- **完成内容**：实现 [day08_trainer.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day08_trainer.py)，使用 pyyaml 解析配置文件，合并命令行覆盖参数，定义通用的 `Trainer` 训练与验证单步迭代循环。
- **测试执行**：`pytest tests/test_day08_trainer.py`

### 第 9 天：PyTorch 工程级训练框架 (网络构建与早停)
- **完成内容**：实现 [day09_network.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day09_network.py) 中的 Dataset 加载机制、配置批归一化与随机失活的神经网络 MLP 回归模型、实现带最优权重保存与早停控制的完整训练。
- **测试执行**：`pytest tests/test_day09_network.py`

### 第 10 天：深度学习进阶：手动实现核心组件 (多头注意力)
- **完成内容**：实现 [day10_attention.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day10_attention.py)，手动编写多头自注意力层（包括三维维度到四维头空间的投影与转置计算、Softmax 加权、头拼接复原）及前馈块 FFN。
- **测试执行**：`pytest tests/test_day10_attention.py`

### 第 11 天：文本生成与轻量级 Transformer (自回归与采样)
- **完成内容**：实现 [day11_generator.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/modeling/day11_generator.py)，利用官方接口构造语言模型，编写自回归循环，实现基于 Top-K 采样的概率预测。
- **测试执行**：`pytest tests/test_day11_generator.py`

### 第 12 天：具身智能仿真入门与反馈控制 (控制闭环)
- **完成内容**：实现 [day12_kinematics.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/simulation/day12_kinematics.py) 的差速小车运动学数值积分、[day12_controller.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/simulation/day12_controller.py) 的反馈 PID 控制器，以及在 [day12_sim_loop.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/simulation/day12_sim_loop.py) 中编写圆形轨迹闭环追踪的仿真计算主循环。
- **测试执行**：`pytest tests/test_day12_simulation.py`
