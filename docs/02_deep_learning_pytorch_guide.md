# 第二册：深度学习与 PyTorch 核心原理零基础通俗手册

> **适合人群**：准备进入 Day 08 - Day 09 深度学习与 PyTorch 训练框架学习的开发者。
> **目标**：彻底理清自动求导、计算图、训练三部曲、DataLoader 以及模型评估机制。

---

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
| ------ | ---------- | -------------- |
| 梯度累加机制 | `loss.backward()` 默认把梯度**累加**到 `.grad` 上，而非覆盖 | 每个 Batch 必须先 `optimizer.zero_grad()`，否则梯度爆炸 |
| `model.eval()` vs `torch.no_grad()` | 前者切换 Dropout/BatchNorm 的层行为，后者关闭计算图构建 | 两者作用完全不同，评估阶段**两个都要用** |
| `torch.save(model)` vs `state_dict` | 只保存权重字典 `state_dict`，不保存整个模型对象 | 直接存对象会因类路径变动导致反序列化失败 |
| `Dataset` vs `DataLoader` | `Dataset` 定义「怎么取一条数据」，`DataLoader` 负责「怎么分批送数据」 | 打乱、分批、多进程都在 `DataLoader`，别写进 `Dataset` |
| `drop_last=True` | 丢弃最后一个不完整的小批次 | 样本数余 1 时，单个样本进 `BatchNorm1d` 会直接报错 |

---

## 1. 什么是 PyTorch 与张量 (Tensor)？

### 1.1 Tensor vs NumPy Array
PyTorch 中的 `torch.Tensor` 几乎和 NumPy 的 `np.ndarray` 一模一样，但它有两个致命的强大武器：
1. **GPU 加速**：可以轻松移动到显卡（CUDA / MPS）上并行计算，速度提升几十到几百倍。
2. **自动求导 (Autograd)**：能够自动追踪每一个数学运算步骤，并自动计算微分梯度。

> 💡 新手提示：张量默认**不会**被追踪。只有创建时指定 `requires_grad=True`（或由 `nn.Module` 自动管理的参数），PyTorch 才会为它构建计算图；调用 `backward()` 后，梯度会存进对应张量的 `.grad` 属性中。

---

## 2. 深度学习核心：自动求导与“训练三部曲”

### 2.1 形象比喻：神射手调靶心
* **前向传播 (Forward)**：射手开枪，子弹落在靶盘上。
* **损失函数 (Loss Function)**：测量子弹落点与红心的**距离（误差/损失值）**。
* **反向传播 (Backward)**：根据落点偏差，计算枪口（模型参数）应该向上还是向左微调（**计算梯度**）。
* **优化器更新 (Optimizer Step)**：按微调的方向和幅度，真正调整枪口位置（**更新参数**）。

---

### 2.2 必须要记住的 PyTorch 训练“固定三部曲”

在每个 Batch 的训练循环中，以下三行代码是绝对固定的黄金套路：

```python
# 1. 梯度清零：清空上一步残留的梯度（非常重要！）
optimizer.zero_grad()

# 2. 反向传播：根据 Loss 沿着计算图向后求导，计算所有参数的当前梯度
loss.backward()

# 3. 参数更新：优化器根据梯度，按学习率 (learning_rate) 调整模型参数
optimizer.step()
```

#### ⚠️ 避坑大坑：为什么一定要 `optimizer.zero_grad()`？
PyTorch 默认的设计是：**每次调用 `loss.backward()` 时，新计算出的梯度会自动“累加”到之前的梯度变量上**。
如果漏掉了 `optimizer.zero_grad()`，第 2 次训练时参数就会叠加上第 1 次的梯度，导致梯度数值越来越庞大，最终发生**梯度爆炸（Gradient Explosion）**，模型彻底训练崩溃。

---

## 3. 神经网络结构搭建：`nn.Module`

### 3.1 极简神经网络标准模板

在 PyTorch 中，所有神经网络都继承自 `nn.Module`，并必须实现两个关键部分：
1. `__init__()`：定义网络包含哪些层（如全连接层 `nn.Linear`、激活函数 `nn.ReLU` 等）。
2. `forward(x)`：定义数据 $x$ 从输入层流向输出层的计算路径。

```python
import torch
import torch.nn as nn

class SimpleMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        # 定义网络层
        self.fc1 = nn.Linear(input_dim, hidden_dim)   # 第一层线性变换
        self.relu = nn.ReLU()                         # 激活函数（引入非线性）
        self.fc2 = nn.Linear(hidden_dim, output_dim) # 输出层
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 数据前向流动
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out
```

> 💡 为什么要 `nn.ReLU()` 这类激活函数？如果只有 `nn.Linear` 层层堆叠，多次线性变换复合后仍等价于一次线性变换，网络退化为单层，无法拟合复杂（非线性）关系。激活函数正是为网络引入非线性的关键。

---

## 4. 数据管道：`Dataset` 与 `DataLoader`

为了高效把海量数据分批（Batch）喂给神经网络，PyTorch 提供了模块化的数据流设计：

### 4.1 自定义 `Dataset`（数据源）
继承 `torch.utils.data.Dataset`，必须重写两个方法：
* `__len__(self)`：返回数据集的样本总数 $N$。
* `__getitem__(self, idx)`：传入索引 `idx`，返回第 `idx` 个样本的特征 $x$ 和标签 $y$。

```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, x_data, y_data):
        self.x = torch.tensor(x_data, dtype=torch.float32)
        self.y = torch.tensor(y_data, dtype=torch.float32)
        
    def __len__(self):
        return len(self.x)
        
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
```

### 4.2 `DataLoader`（传送带）
`DataLoader` 负责把 `Dataset` 包装起来，自动完成**打乱数据 (shuffle)**、**分批 (batch_size)** 和 **多线程加载 (num_workers)**：

```python
dataset = MyDataset(x_data, y_data)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True, drop_last=True)
```
* **`drop_last=True` 避坑细节**：如果总样本数除以 `batch_size` 余数为 1，最后那一个孤独的样本传入包含 `BatchNorm1d` 的网络时会报错。加上 `drop_last=True` 丢弃最后一个不完整的批次，能完美避开崩溃。

---

## 5. 训练模式 (`train`) vs 评估模式 (`eval`)

神经网络在“学习训练”和“考试评估”时的行为是不一样的！
* **训练时**：`Dropout` 会随机扔掉部分神经元，`BatchNorm` 会实时计算本批次的均值和方差。
* **评估/测试时**：我们需要一个确定的、固定的网络模型。

### 5.1 验证集评估的黄金组合

```python
# 1. 切换为评估模式
model.eval()

# 2. 禁用自动求导（关闭计算图构建，极大地节省显存与内存！）
with torch.no_grad():
    for x_val, y_val in val_loader:
        outputs = model(x_val)
        loss = criterion(outputs, y_val)
        # 注意：评估阶段决不能调用 loss.backward() 或 optimizer.step()！
```

评估结束后若要继续训练，记得调用 `model.train()` 切回训练模式，否则 Dropout 和 BatchNorm 会保持评估状态，导致训练效果异常。

---

## 6. 模型保存与加载最佳实践

在 PyTorch 中保存训练好的模型参数时：
* ❌ **错误做法**：`torch.save(model, "model.pt")`（保存整个模型对象，一旦类路径变动反序列化会报错）。
* ✅ **标准工程做法**：仅保存权重字典 `state_dict`。

```python
# 保存参数权重
torch.save(model.state_dict(), "model_weights.pth")

# 加载参数权重
model = SimpleMLP(input_dim=10, hidden_dim=64, output_dim=1) # 实例化新网络
model.load_state_dict(torch.load("model_weights.pth"))     # 加载权重
```
