import os
import pandas as pd  # type: ignore
from typing import Tuple

def load_sensor_data(csv_path: str) -> pd.DataFrame:
    """
    Day 7: Pandas 与时间序列数据工程 - 读取原始传感器数据
    
    目标：
    1. 从 csv_path 加载数据，并将 "timestamp" 列解析为日期时间格式。
    2. 将 "timestamp" 列设为 DataFrame 的索引。
    3. 按照索引（时间）进行升序排序。
    4. 返回格式化好的 DataFrame。
    
    知识体系清单：
    - `DatetimeIndex` 重采样：使用 `resample().mean()` 整合杂乱采样频率。
    - 缺失值传递控制：使用 `ffill()` 进行时序序列前向填充，确保数据无中断。
    - 窗口与时滞特征构造：利用 `rolling()` 构建滑动窗口特征，使用 `shift()` 构造历史状态特征。
    - 时序划分禁忌：切分训练/测试集时禁止随机打散 Shuffle，防止引入“未来数据”。
    
    工程实践避坑指南：
    - 数据泄露（Data Leakage）：计算滑动均值等统计量时需防未来时间点的参数流入窗口。在时序数据拆分时若使用了随机分配机制，模型容易在训练时过拟合，部署在真机上时产生极大误差。
    - NaN 传导梯度爆炸：`rolling` 与 `shift` 会在序列头部引入 NaN。在传入 PyTorch 训练前，必须调用 `.dropna()` 彻底清洗掉这些空行，否则会导致神经网络训练过程中反向梯度求导得出 NaN 并迅速污染整个模型参数。
    
    :param csv_path: 传感器 CSV 数据文件路径
    :return: 排序后的 DataFrame，索引为 DatetimeIndex
    """
    # TODO: 读取 CSV 并设置时间索引，按时间升序排列
    raise NotImplementedError("Please implement load_sensor_data")


def preprocess_time_series(df: pd.DataFrame, frequency: str = "10s") -> pd.DataFrame:
    """
    将非固定采样率的传感器数据重采样为固定采样率（如 10 秒一个点），并填充缺失值。
    
    提示与关键点：
    1. 使用 `df.resample(rule).mean()` 进行时间频率重采样并计算均值。
    2. 重采样后可能会产生空值（例如在某个 10s 区间内没有传感器数据）。
    3. 使用前向填充（`ffill()`）填充缺失的数值，保证时间序列的连续性。
    
    :param df: 输入的 DataFrame，必须有 DatetimeIndex 索引
    :param frequency: 重采样的时间间隔规则，默认 "10s"
    :return: 重采样并前向填充后的 DataFrame
    """
    # TODO: 对数据进行重采样和前向填充值
    raise NotImplementedError("Please implement preprocess_time_series")


def create_lag_features(df: pd.DataFrame, target_column: str, window_size: int = 5) -> pd.DataFrame:
    """
    针对指定的传感器数值列，构造特征：
    1. 滚动均值 (rolling mean)：计算过去 window_size 个数据点的平均值。
    2. 滚动标准差 (rolling std)：计算过去 window_size 个数据点的标准差。
    3. 滞后特征 (lag features)：将 target_column 向后平移 1 个和 2 个时间步，代表过去时刻的值。
    
    提示与关键点：
    1. 滚动特征使用 `df[target_column].rolling(window=window_size).mean()` 和 `.std()`。
    2. 平移值使用 `df[target_column].shift(periods=1)` 和 `.shift(2)`。
    3. 构造出新列： 'rolling_mean', 'rolling_std', 'lag_1', 'lag_2' 并加入原 DataFrame 中。
    4. 滚动计算和 shift 会在头部产生 NaN，使用 `.dropna()` 滤除这些包含空值的行。
    
    :param df: 输入的 DataFrame
    :param target_column: 提取特征的目标列名
    :param window_size: 滚动窗口大小，默认 5
    :return: 包含新增特征列且已删除缺失值的 DataFrame
    """
    # TODO: 构造 rolling_mean, rolling_std, lag_1, lag_2 并且 dropna() 过滤空行
    raise NotImplementedError("Please implement create_lag_features")


def time_series_train_test_split(df: pd.DataFrame, test_ratio: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    按时间顺序切分训练集和测试集（不可使用随机打散，因为时间序列数据具有时序相关性）。
    
    步骤：
    1. 找到分割点的行索引位置。
    2. 分割位置的前半截为训练集，后半截为测试集。
    
    :param df: 输入的 DataFrame
    :param test_ratio: 测试集比例，默认 0.2
    :return: 元组 (train_df, test_df)
    """
    # TODO: 按时间位置切分并返回训练集和测试集
    raise NotImplementedError("Please implement time_series_train_test_split")
