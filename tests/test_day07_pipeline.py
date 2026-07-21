import pytest
import pandas as pd  # type: ignore
from python_projects.data_engineering.day07_pipeline import (
    load_sensor_data,
    preprocess_time_series,
    create_lag_features,
    time_series_train_test_split
)

def test_sensor_pipeline():
    csv_path = "data/raw_odometry.csv"
    
    # 1. 测试数据加载
    try:
        df = load_sensor_data(csv_path)
        assert isinstance(df.index, pd.DatetimeIndex)
        assert df.index.is_monotonic_increasing
    except NotImplementedError:
        pytest.skip("load_sensor_data is not implemented yet.")
        return

    # 2. 测试重采样与前向填充
    try:
        df_clean = preprocess_time_series(df, frequency="10s")
        # 应该是固定周期的索引
        assert len(df_clean) > 0
        assert not df_clean.isna().any().any()
    except NotImplementedError:
        pytest.skip("preprocess_time_series is not implemented yet.")
        return

    # 3. 测试滑动窗口特征与滞后特征构造
    try:
        df_features = create_lag_features(df_clean, target_column="value", window_size=3)
        expected_cols = ["value", "rolling_mean", "rolling_std", "lag_1", "lag_2"]
        for col in expected_cols:
            assert col in df_features.columns
        assert not df_features.isna().any().any()
    except NotImplementedError:
        pytest.skip("create_lag_features is not implemented yet.")
        return

    # 4. 测试时间序列顺序划分
    try:
        train_df, test_df = time_series_train_test_split(df_features, test_ratio=0.2)
        assert len(train_df) + len(test_df) == len(df_features)
        # 训练集的最后时间戳应早于测试集的开始时间戳
        assert train_df.index[-1] < test_df.index[0]
    except NotImplementedError:
        pytest.skip("time_series_train_test_split is not implemented yet.")
