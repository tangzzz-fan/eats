import yaml  # type: ignore
import argparse
import torch
import torch.nn as nn
from typing import Dict, Any, Tuple

def load_yaml_config(yaml_path: str) -> Dict[str, Any]:
    """
    Day 8: 从 NumPy 到 PyTorch 与模块化框架设计 - 读取配置文件
    
    目标：
    使用 pyyaml 读取 YAML 配置文件，提取出模型的超参数和控制参数。
    
    知识体系清单：
    - 工程化参数控制：YAML 参数读取与 argparse 终端输入动态覆盖合并。
    - PyTorch 单步参数训练循环：输入数据装载，优化器零梯度 `zero_grad`，Loss 反向求导与参数更新 `step`。
    - 评估保护模式：在验证循环中使用 `model.eval()` 冻结运行状态，使用 `torch.no_grad()` 上下文禁用动态计算图构建。
    
    工程实践避坑指南：
    - 忘做梯度归零导致收敛异常：PyTorch 默认在调用 `.backward()` 时将最新梯度进行累加。如果未显式执行 `optimizer.zero_grad()`，梯度会跨 Batch 不断增长，导致参数调整巨大，训练发散。
    - 验证阶段内存溢出 (OOM)：在验证 epoch 评估测试时，如果不加上 `with torch.no_grad():`，系统会默认记录中间变量计算图以备求导，这会导致显存/内存随循环前向计算不断被占满，直到抛出 OOM。
    
    :param yaml_path: yaml 文件路径
    :return: 包含配置字典的嵌套 Python Dict
    """
    # TODO: 使用 open() 打开 yaml_path 并通过 yaml.safe_load 载入配置
    raise NotImplementedError("Please implement load_yaml_config")


def parse_args_and_merge_config(config: Dict[str, Any]) -> Tuple[argparse.Namespace, Dict[str, Any]]:
    """
    使用 argparse 接收命令行输入，并覆盖/合并配置文件中的值。
    主要供工程级大项目使用，允许终端参数覆盖 yaml。
    
    :param config: 原始配置字典
    :return: 元组 (args, merged_config)
    """
    parser = argparse.ArgumentParser(description="Embodied AI Trajectory Tracker Training script")
    parser.add_argument("--lr", type=float, default=None, help="Override learning rate")
    parser.add_argument("--epochs", type=int, default=None, help="Override epochs")
    
    args = parser.parse_args([]) # 在单元测试或脚本中默认为空
    
    # 覆盖逻辑
    if args.lr is not None:
        config["training"]["learning_rate"] = args.lr
    if args.epochs is not None:
        config["training"]["epochs"] = args.epochs
        
    return args, config


class Trainer:
    """
    通用 PyTorch 模型训练循环（Trainer）的封装。
    负责控制每个 epoch 的训练与评估，解耦模型结构与训练逻辑。
    """
    def __init__(self, 
                 model: nn.Module, 
                 optimizer: torch.optim.Optimizer, 
                 criterion: nn.Module, 
                 device: str = "cpu"):
        """
        初始化训练器。
        
        :param model: PyTorch 神经网络模型
        :param optimizer: 优化器
        :param criterion: 损失函数
        :param device: 设备类型 ("cpu", "cuda", "mps")
        """
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device

    def train_epoch(self, dataloader: torch.utils.data.DataLoader) -> float:
        """
        单轮训练逻辑（One epoch training loop）。
        
        步骤：
        1. 设置模型为训练模式：`self.model.train()`
        2. 遍历数据加载器：提取 inputs, targets 并移至 self.device
        3. 优化器梯度清零
        4. 前向传播，计算 outputs
        5. 计算损失 loss
        6. 反向传播，计算梯度
        7. 优化器更新参数
        8. 累加并计算平均损失值并返回。
        
        :param dataloader: 训练集 DataLoader
        :return: 本轮训练的平均 Loss 标量值
        """
        # TODO: 实现单轮训练逻辑
        raise NotImplementedError("Please implement Trainer.train_epoch")

    def val_epoch(self, dataloader: torch.utils.data.DataLoader) -> float:
        """
        单轮验证评估逻辑（One epoch validation loop）。
        
        步骤：
        1. 设置模型为评估模式：`self.model.eval()`
        2. 使用 `with torch.no_grad():` 禁用梯度计算（节省显存，加速计算）
        3. 遍历数据加载器并移至 self.device
        4. 前向传播计算 outputs
        5. 计算损失 loss 并累加
        6. 计算平均验证 Loss 并返回。
        
        :param dataloader: 验证集 DataLoader
        :return: 本轮验证的平均 Loss 标量值
        """
        # TODO: 在不计算梯度的保护下进行前向传播并计算验证集 Loss
        raise NotImplementedError("Please implement Trainer.val_epoch")

    def fit(self, train_loader: torch.utils.data.DataLoader, val_loader: torch.utils.data.DataLoader, epochs: int) -> None:
        """
        完整的训练循环控制流。
        
        :param train_loader: 训练集加载器
        :param val_loader: 验证集加载器
        :param epochs: 最大迭代周期数
        """
        for epoch in range(1, epochs + 1):
            train_loss = self.train_epoch(train_loader)
            val_loss = self.val_epoch(val_loader)
            print(f"Epoch {epoch:02d} | Train Loss: {train_loss:.5f} | Val Loss: {val_loss:.5f}")
