import os
import pytest
import numpy as np  # type: ignore
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from python_projects.modeling.day09_network import (
    TelemetryDataset,
    SteeringMLP,
    train_with_early_stopping
)

def test_telemetry_dataset():
    x_data = np.random.randn(10, 4)
    y_data = np.random.randn(10, 1)
    
    try:
        dataset = TelemetryDataset(x_data, y_data)
        assert len(dataset) == 10
        x_tensor, y_tensor = dataset[3]
        assert isinstance(x_tensor, torch.Tensor)
        assert x_tensor.shape == (4,)
        assert y_tensor.shape == (1,)
    except NotImplementedError:
        pytest.skip("TelemetryDataset is not implemented yet.")

def test_steering_mlp_shapes():
    try:
        model = SteeringMLP(input_dim=4, hidden_dim=8, output_dim=1)
        x = torch.randn(5, 4)  # batch=5
        out = model(x)
        assert out.shape == (5, 1)
    except NotImplementedError:
        pytest.skip("SteeringMLP is not implemented yet.")

def test_train_with_early_stopping():
    try:
        model = SteeringMLP(input_dim=4, hidden_dim=8, output_dim=1)
        x_data = np.random.randn(20, 4)
        y_data = np.random.randn(20, 1)
        
        dataset = TelemetryDataset(x_data, y_data)
        loader = DataLoader(dataset, batch_size=4)
        
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()
        
        # 运行训练
        best_model, best_loss = train_with_early_stopping(
            model=model,
            train_loader=loader,
            val_loader=loader,
            optimizer=optimizer,
            criterion=criterion,
            epochs=2,
            patience=2,
            checkpoint_path="test_best_model.pth"
        )
        assert isinstance(best_loss, float)
        # 清理生成的临时 checkpoint
        if os.path.exists("test_best_model.pth"):
            os.remove("test_best_model.pth")
    except NotImplementedError:
        pytest.skip("train_with_early_stopping features are not implemented yet.")
