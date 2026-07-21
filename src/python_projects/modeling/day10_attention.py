import math
import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    """
    Day 10: 深度学习进阶 - 手动实现多头注意力机制 (Multi-Head Attention)
    
    目标：
    在 PyTorch 中手动实现多头注意力机制。注意力计算核心公式为：
    Attention(Q, K, V) = Softmax( (Q * K^T) / sqrt(d_k) ) * V
    
    提示与关键点：
    1. 输入参数：d_model (特征维度), num_heads (注意力头数)。特征维度必须能被头数整除。
    2. 计算各个头对应的维度：`head_dim = d_model // num_heads`。
    3. 定义 4 个线性投影层：
       - `q_proj = nn.Linear(d_model, d_model)`
       - `k_proj = nn.Linear(d_model, d_model)`
       - `v_proj = nn.Linear(d_model, d_model)`
       - `out_proj = nn.Linear(d_model, d_model)`
    4. 在 forward 中：
       - 将输入的 q, k, v 分别进行投影。
       - 对投影结果的维度进行拆分，使其能够独立计算每个头的注意力。
         例如 shape 从 (batch_size, seq_len, d_model) 变为 (batch_size, seq_len, num_heads, head_dim)，
         再转置为 (batch_size, num_heads, seq_len, head_dim)。
       - 按照公式计算 QK^T 并除以 sqrt(head_dim)。
       - 对最后一个维度计算 Softmax。
       - 与 V 相乘，得到加权结果。
       - 把所有头的结果转置并连接（concat）还原回 (batch_size, seq_len, d_model) 形状。
       - 最后通过 out_proj 线性层输出。
       
    知识体系清单：
    - 多头注意力计算公式： scaled dot-product attention 各维度的映射规则与批量点积相似度求法。
    - 张量形状变换与轴重塑：利用 `.view()` 重构多头特征，借助 `.transpose()` 轴对齐提高并行点积计算效率。
    - 缩放因子的物理作用：除以 `sqrt(head_dim)` 对点积结果进行抑制，避免 Softmax 输出饱和（大元素趋近于 1，小元素趋近于 0）引发的梯度消失。
    
    工程实践避坑指南：
    - 轴顺序混淆导致空间意义错乱：在将特征折叠到多头通道时，千万不可直接调用 `.view(B, H, S, d_k)` 进行维度变形。这会在物理特征上直接混合序列元素和头序列。必须先执行三维到四维的序列变换 `.view(B, S, H, d_k)`，然后再在轴 1 和 2 上做交换 `.transpose(1, 2)`。
    - 内存不连续导致 view 重塑报错：张量转置运算（transpose）仅修改元数据索引，并不会在物理存储上挪动数据，这会导致底层内存分布不连续。在完成 Attention 运算并试图合并各头调用 `.view()` 时会报错。必须在前置步骤显式调用 `.contiguous()` 重新规划内存再变形。
    """
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads.")
            
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        
        # TODO: 定义线性投影层
        raise NotImplementedError("Please implement MultiHeadAttention.__init__ layers")

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """
        前向计算。
        
        :param q: (batch_size, seq_len_q, d_model)
        :param k: (batch_size, seq_len_k, d_model)
        :param v: (batch_size, seq_len_v, d_model)
        :return: 注意力加权输出，形状为 (batch_size, seq_len_q, d_model)
        """
        # TODO: 编写多头注意力机制前向流程的形状变换与计算
        # 1. 经过投影层 q = self.q_proj(q)
        # 2. 变换形状为 (batch_size, num_heads, seq_len, head_dim)
        # 3. 矩阵相乘计算相关系数得分 scores
        # 4. 计算 Softmax 得到注意力权重 weights
        # 5. 加权 V 矩阵，再合并所有头（transpose -> reshape）
        # 6. 经过 out_proj 得到最终输出并返回
        raise NotImplementedError("Please implement MultiHeadAttention.forward")


class FeedForwardNetwork(nn.Module):
    """
    Day 10: 深度学习进阶 - Transformer 前馈网络模块 (Feed-Forward Network)
    
    目标：
    实现每个 Transformer 块中紧跟在多头注意力后面的两层线性前馈神经网络。
    
    结构：
    FFN(x) = max(0, x * W1 + b1) * W2 + b2
    即：线性层(d_model -> d_ff) -> ReLU -> Dropout -> 线性层(d_ff -> d_model)
    """
    def __init__(self, d_model: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        # TODO: 定义前馈网络的两层全连接、激活函数与 Dropout 层
        raise NotImplementedError("Please implement FeedForwardNetwork.__init__ layers")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # TODO: 依次通过两层映射和激活层完成计算并返回
        raise NotImplementedError("Please implement FeedForwardNetwork.forward")
