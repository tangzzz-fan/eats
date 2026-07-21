import pytest
import torch
import torch.nn as nn
from python_projects.modeling.day08_trainer import (
    load_yaml_config,
    parse_args_and_merge_config,
    Trainer
)

def test_config_loader():
    yaml_path = "config/config.yaml"
    try:
        config = load_yaml_config(yaml_path)
        assert "training" in config
        assert "model" in config
        assert "control" in config
        assert config["training"]["learning_rate"] == 0.005
    except NotImplementedError:
        pytest.skip("load_yaml_config is not implemented yet.")

def test_parse_args_and_merge_config(monkeypatch):
    config = {
        "training": {
            "learning_rate": 0.005,
            "epochs": 20
        }
    }
    # 模拟输入参数覆盖
    import sys
    monkeypatch.setattr(sys, "argv", ["trainer.py", "--lr", "0.02", "--epochs", "50"])
    try:
        args, merged = parse_args_and_merge_config(config)
        assert merged["training"]["learning_rate"] == 0.02
        assert merged["training"]["epochs"] == 50
    except NotImplementedError:
        pytest.skip("parse_args_and_merge_config is not implemented yet.")

def test_trainer_loops():
    class DummyModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(2, 1)
        def forward(self, x):
            return self.linear(x)

    model = DummyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    # 构造假数据
    x_data = torch.randn(10, 2)
    y_data = torch.randn(10, 1)
    dataset = torch.utils.data.TensorDataset(x_data, y_data)
    loader = torch.utils.data.DataLoader(dataset, batch_size=2)
    
    trainer = Trainer(model, optimizer, criterion)
    
    try:
        train_loss = trainer.train_epoch(loader)
        assert isinstance(train_loss, float)
    except NotImplementedError:
        pytest.skip("Trainer.train_epoch is not implemented yet.")
        
    try:
        val_loss = trainer.val_epoch(loader)
        assert isinstance(val_loss, float)
    except NotImplementedError:
        pytest.skip("Trainer.val_epoch is not implemented yet.")
