# Day 07：Pandas 与时间序列数据工程 - 快速上手指南

本指南旨在帮助你快速掌握 `Day 07` 练习（[day07_pipeline.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day07_pipeline.py)）所需的核心 Pandas 知识点、时间序列处理技巧与特征工程方法。

---

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
| --- | --- | --- |
| `resample()` vs `rolling()` | `resample` 按**时间频率**重新对齐聚合，`rolling` 按**固定行数**滑动窗口统计 | 前者改变行的时间间隔，后者行数不变、只在原索引上滑窗，别混用 |
| `ffill()` 前向填充 | 用前一个有效值填补重采样产生的空洞 | 序列**最开头**若没有历史值仍会是 `NaN`，`ffill` 救不了开头 |
| `shift(p)` 的方向 | 正数表示"取过去第 $p$ 个时刻的值"放到当前行 | 方向容易记反：`shift(1)` 得到的是 $t-1$ 时刻的值，不是未来值 |
| 时间序列切分禁止 shuffle | 随机打散会把未来数据混入训练集，造成数据泄露 | 必须用 `iloc` 按位置顺序切分，且 `int()` 向下取整保证切点不越界 |
| 特征构造后的头部 `NaN` | `rolling`/`shift` 会让前 $W-1$ 行缺少历史数据 | 入模型前必须统一 `.dropna()`，否则梯度被 `NaN` 污染 |

---

## 1. 核心任务目标

时间序列数据（如机器人传感器里程计数据、股票价格、气象监测等）与普通的表格数据不同，其**行与行之间具有强烈的时间先后顺序关联**。

在 Day 07 中，你需要实现一个完整的时间序列数据处理管道，包含 4 个核心步骤：
1. `load_sensor_data(csv_path)`: 读取 CSV，解析时间戳为 `DatetimeIndex` 并按时间排序。
2. `preprocess_time_series(df, frequency)`: 对非固定采样频率的传感器数据进行重采样与缺失值填充。
3. `create_lag_features(df, target_column, window_size)`: 构造滑动窗口均值/标准差与滞后 (Lag) 特征。
4. `time_series_train_test_split(df, test_ratio)`: 严格按时间先后顺序切分训练集与测试集（禁止随机打散）。

---

## 2. 核心知识点详解

### 2.1 知识点一：时间索引与排序 (`load_sensor_data`)

传感器采样的 CSV 文件（如 `data/raw_odometry.csv`）通常包含 `timestamp` 列。我们需要将其转化为 Pandas 的 `DatetimeIndex`。

#### 实现步骤：
1. **读取 CSV**：`df = pd.read_csv(csv_path)`
2. **转换时间列**：`df['timestamp'] = pd.to_datetime(df['timestamp'])`
3. **设置为索引**：`df = df.set_index('timestamp')`
4. **按时间升序排序**：`df = df.sort_index()`

#### 为什么必须排序？
在时间序列分析中，数据的顺序决定了随后的重采样和滑动窗口是否准确。Pandas 提供了 `.index.is_monotonic_increasing` 属性来验证索引是否已经严格按时间单调递增。

---

### 2.2 知识点二：时间重采样与缺失值填充 (`preprocess_time_series`)

真实的传感器数据常常存在**采样频率不固定**的问题（例如有时 5s 传一次，有时 12s 传一次）。在机器学习建模前，通常需要将其规范化为固定频率（例如 10s 一点）。

#### (1) 重采样 (`resample`)
`resample()` 类似于时间维度上的 `groupby()`：
```python
# 将时间频率重采样为每 10 秒 ("10s") 一个点，并计算该时间窗口内的均值
df_resampled = df.resample(frequency).mean()
```

常用频率代码：
* `"10s"`：10 秒
* `"1min"` / `"1T"`：1 分钟
* `"1D"`：1 天

#### (2) 前向填充 (`ffill`)
重采样后，如果某个 10 秒时间段内没有任何传感器数据，重采样的结果对应行就会出现 `NaN` 缺失值。
* 为什么不能直接 `dropna()` 删除或者填 `0`？
  传感器数据（如温度、车速、位置）通常具有物理连续性，某个时刻没采到值，最合理的估计就是**保持前一时刻的数值**。
* 使用 `ffill()`（Forward Fill）：
```python
df_clean = df_resampled.ffill()
```

> 注意：`ffill()` 只能"向后借"前面已有的值。如果序列**最开始的几行**本来就是空的（前面没有任何历史值可借），填充后依然是 `NaN`。这时可以根据业务选择 `bfill()`（向后填充）或干脆 `dropna()` 丢掉头部这几行。

---

### 2.3 知识点三：滑动窗口与滞后特征构造 (`create_lag_features`)

为了让模型学会利用“历史趋势”来预测未来，我们需要为数据构造两类特征：
1. **滑动窗口统计特征 (Rolling Window Features)**
2. **时滞特征 (Lag Features)**

#### (1) 滑动窗口统计特征 (`rolling`)
计算过去 $W$ 个时间步（例如 3 个点）的滚动均值和滚动标准差：
```python
# 计算过去 window_size 个数据点的滑动均值
df['rolling_mean'] = df[target_column].rolling(window=window_size).mean()

# 计算过去 window_size 个数据点的滑动标准差
df['rolling_std'] = df[target_column].rolling(window=window_size).std()
```

#### (2) 时滞特征 (`shift`)
`shift(p)` 表示将数据向后平移 $p$ 个时间步，用来表示“过去第 $p$ 个时刻的值”：

这里的“向后平移”容易想反，看一个最小例子就清楚了：

```python
s = pd.Series([10, 20, 30])
s.shift(1)  # -> [NaN, 10, 20]：当前行拿到的是上一时刻的值
```

即 `shift(1)` 后第 $t$ 行的值来自第 $t-1$ 行，所以 `lag_1` 表示"过去 1 个时间步"。

```python
# 过去 1 个时间步的值 (t-1)
df['lag_1'] = df[target_column].shift(1)

# 过去 2 个时间步的值 (t-2)
df['lag_2'] = df[target_column].shift(2)
```

#### (3) 过滤头部缺失值 (`dropna`)
由于 `rolling` 和 `shift` 均需要利用过去的历史数据，在序列最开始的几行（前 $W-1$ 行）因为没有足够的历史数据，会产生 `NaN`。
* **避坑指南**：如果将带有 `NaN` 的数据直接传入 PyTorch 等神经网络模型训练，反向传播时梯度会迅速污染整个模型参数导致崩溃。
* **解决方法**：在构造完所有特征后，统一调用 `.dropna()`：
```python
df_features = df.dropna()
```

---

### 2.4 知识点四：按时间顺序切分训练/测试集 (`time_series_train_test_split`)

#### 🛑 绝对禁忌：随机打散 (Shuffle)
在处理常规表格数据时，我们常用 `train_test_split(..., shuffle=True)` 随机切分。但在时间序列中，**严禁使用随机打散**！
* **数据泄露 (Data Leakage)**：如果将未来时刻 $t+1$ 的数据混入训练集，模型就会“提前偷看未来答案”，导致训练集评估效果极好，但在实际部署中预测效果极差。

#### 正确切分方法：顺序切分
计算分割位置索引 `split_idx`，前部分作为训练集，后部分作为测试集：
```python
# 假设测试集比例为 test_ratio = 0.2
n_samples = len(df)
split_idx = int(n_samples * (1 - test_ratio))

train_df = df.iloc[:split_idx]
test_df = df.iloc[split_idx:]
```

两点说明：
* 这里用的是 `iloc`（按**位置**切片）而不是 `loc`（按标签切片），因为我们要的是"前 80% 的行 / 后 20% 的行"，与时间索引的具体取值无关。
* `int()` 会向下取整，因此当样本数不能被整除时，多余的一行会落入测试集，保证切点不越界、测试集也不会为空（前提是 `test_ratio > 0`）。

---

## 3. 函数 API 与实现代码参考卡片 (Quick Reference)

### 3.1 `load_sensor_data(csv_path)`
```python
def load_sensor_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    df = df.sort_index()
    return df
```

### 3.2 `preprocess_time_series(df, frequency)`
```python
def preprocess_time_series(df: pd.DataFrame, frequency: str = "10s") -> pd.DataFrame:
    df_resampled = df.resample(frequency).mean()
    df_clean = df_resampled.ffill()
    return df_clean
```

### 3.3 `create_lag_features(df, target_column, window_size)`
```python
def create_lag_features(df: pd.DataFrame, target_column: str, window_size: int = 5) -> pd.DataFrame:
    df = df.copy()
    df['rolling_mean'] = df[target_column].rolling(window=window_size).mean()
    df['rolling_std'] = df[target_column].rolling(window=window_size).std()
    df['lag_1'] = df[target_column].shift(1)
    df['lag_2'] = df[target_column].shift(2)
    return df.dropna()
```

### 3.4 `time_series_train_test_split(df, test_ratio)`
```python
def time_series_train_test_split(df: pd.DataFrame, test_ratio: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
    split_idx = int(len(df) * (1 - test_ratio))
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    return train_df, test_df
```

---

## 4. 单元测试验证

完成 [day07_pipeline.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day07_pipeline.py) 的代码后，你可以运行以下命令测试正确性：

```bash
.venv/bin/pytest tests/test_day07_pipeline.py
```

祝你学习顺利！
