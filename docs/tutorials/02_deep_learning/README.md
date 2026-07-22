# 深度学习与PyTorch：写给高中生的入门指南

这篇指南要讲的是「深度学习」——这几年让 AI 突然变聪明的那门技术，以及用它最流行的工具 PyTorch。

先用一句话说清它是干什么的：**深度学习，就是教一台「什么都不会」的机器，通过海量例题自己摸索出规律，最终学会做预测。** 比如给它看一万张猫的照片，它自己总结出「猫长什么样」，之后看到新照片就能认出猫。

为了讲明白这件事，我们全文用一个比喻：**深度学习就像一个学生在练投篮。**

- 学生一开始完全不会投篮，出手全靠蒙（这就是刚出生的神经网络）。
- 每投一球，他都看看球离篮筐偏了多少（这就是损失函数在打分）。
- 他根据偏差复盘：「这次力气大了、偏左了，下次往右收一点」（这就是反向传播和梯度下降）。
- 投了一万球之后，他成了神射手（训练完成）。

整篇指南，就是把「学生练投篮」翻译成机器听得懂的语言。你只需要会一点 Python 基础，不需要任何高等数学——需要的数学，我们都会用生活直觉先讲明白。

---

## 先建立直觉

先问一个问题：你想让电脑「认出照片里的猫」，该怎么写程序？

传统的编程思路是：程序员写规则。比如「如果有尖耳朵、有胡须、眼睛是竖瞳，那就是猫」。你很快会发现这根本写不完——猫有躺着的、只露半张脸的、橘猫黑猫无毛猫……规则无穷无尽，程序员写到崩溃也写不全。

这就是传统编程撞上的墙：**有些事我们人会做，但说不清自己是怎么做的。** 你认得出猫，可你能写出一本《认猫规则手册》精确到每个像素吗？写不出。

深度学习的思路反过来了：**既然规则写不出来，那就别写了，让机器自己从例子里学。**

- 传统编程：人写规则 + 数据 → 电脑 → 答案
- 深度学习：人给数据 + 答案 → 电脑 → 自己总结出规则

就像一个从不看球的人，你让他看一万次投篮录像，他慢慢也能「感觉」到什么动作能进。他没背过任何规则，但他「学会」了。深度学习做的就是把这种「从例子中找感觉」的过程，变成可以计算的数学和代码。

而 PyTorch，就是做这件事最流行的一套工具箱（由 Meta 公司开源）。它帮你把「找感觉」需要的脏活累活——算账、记账、调参数——全都自动化了。

---

## 知识地图

先给你一张全局地图，后面逐个展开：

| # | 核心知识点 | 一句话概括 |
|---|-----------|-----------|
| 1 | 神经网络是什么 | 一个装着几百万个「旋钮」的超复杂函数，学习就是拧对旋钮 |
| 2 | 损失函数与梯度下降 | 给预测打分（损失），再顺着「下山方向」一点点拧旋钮（下降） |
| 3 | 张量与自动求导 | PyTorch 的「数字盒子」，会自动记下计算过程并帮你算调整方向 |
| 4 | 训练循环五部曲 | 投篮 → 打分 → 复盘 → 调整 → 清空记录，每轮固定五步 |
| 5 | Dataset / DataLoader | 一个负责「怎么取一条数据」，一个负责「怎么一筐一筐送数据」 |
| 6 | 模型保存与评估 | 训练好要存档，考试时要切「考试模式」且不许再改答案 |

---

## 重点逐个讲

### 1. 神经网络是什么：一台有很多旋钮的机器

**生活比喻**：想象一台老式收音机，上面有一排旋钮，拧不同的旋钮组合，出来的声音就不一样。神经网络就是一台有**几百万个旋钮**的机器。

**直觉解释**：你在数学课上学过函数，比如 `y = 2x + 1`——输入一个 `x`，输出一个 `y`。这里的 `2` 和 `1` 就是两个「旋钮」。

神经网络本质上也是一个函数，只不过：

- 旋钮多得吓人（真实的大模型有上千亿个）。
- 它不在纸上，而是用代码搭出来的：一层一层的「神经元」，每层做一点简单计算，叠起来就能表达极其复杂的规律。

「训练」做的事就是：**一开始旋钮全是随机乱拧的（所以预测全是瞎蒙），然后不断根据预测得有多离谱，把所有旋钮一点点往正确方向拧。** 拧到最后一拧一个准，模型就「学会」了。

**最小例子**：用 PyTorch 搭一台最小的「机器」——它只有一层，内部就两个旋钮（一个叫权重 `weight`，一个叫偏置 `bias`），本质就是自动帮你学 `y = kx + b` 里的 `k` 和 `b`：

```python
import torch
import torch.nn as nn

model = nn.Linear(1, 1)  # 一层网络：1个输入，1个输出，里面藏着 k 和 b 两个旋钮
x = torch.tensor([[2.0]])
print(model(x))  # 旋钮还是随机值，输出是瞎猜的，每次运行都不一样
print(model.weight, model.bias)  # 看看这两个旋钮现在拧在哪
```

**一句话总结**：神经网络 = 旋钮超多的函数，训练 = 把旋钮逐个拧到正确位置。

---

### 2. 损失函数与梯度下降：打分 + 下山

**生活比喻**：你蒙着眼睛站在山上，想走到山谷最低点。你看不见全局，但能感觉脚下哪边是下坡——于是每步都朝最陡的下坡方向挪一小步，挪很多步，就到谷底了。

**直觉解释**：

- **损失函数（Loss Function）** 就是「打分器」：模型的预测离正确答案差多远，它就给多高的分。分差得越远，损失越大——相当于你站在山上越高。
- **梯度（Gradient）** 就是「脚下哪边是下坡」：它告诉你每个旋钮往哪个方向拧、拧多少，损失会变小。你不用懂微积分，只需要知道：PyTorch 能自动把这个方向算出来。
- **梯度下降（Gradient Descent）** 就是「挪一小步」：每次只拧一点点（这个「一点点」叫学习率，learning rate），因为方向只在脚下附近准，一步跨太大容易踩空。

**最小例子（手算）**：假设正确答案是 8，模型预测是 5，学习率是 0.1。

- 用一种最简单的打分：损失 = 差距的平方 = `(8 - 5)² = 9`
- 算出调整方向：预测偏小，应该把预测调大，步子大小是 `0.1 × 差距 × 2 = 0.6`
- 新预测 = `5 + 0.6 = 5.6`，新损失 = `(8 - 5.6)² = 5.76`

看到了吗：损失从 9 降到 5.76。就这样一小步一小步挪，预测会从 5 → 5.6 → 6.16 → …… 慢慢逼近 8。训练就是把这件事重复几千几万次。

**一句话总结**：损失函数负责说「你错得有多离谱」，梯度下降负责说「那往这边挪一小步」。

---

### 3. 张量与自动求导：会记账的数字盒子

**生活比喻**：张量像一个带账本的快递箱。里面装着数字（一个数、一行数、或一整个表格都行），关键是它会把「这个数字经过了哪些运算」一笔一笔记在账本上。等你要复盘时，它翻着账本几秒钟就能算出每个旋钮该怎么调。

**直觉解释**：

- **张量（Tensor）**：名字唬人，其实就是「装数字的盒子」。一个数、一个列表、一个 Excel 表格，在张量眼里是同一种东西的不同尺寸。PyTorch 里所有数据都用张量装。
- **自动求导（Autograd）**：这是 PyTorch 最值钱的功能。你只管写「预测 → 算损失」这一步（叫前向传播，forward），然后喊一声 `backward()`（反向传播），它就自动顺着账本倒推，算出**每一个旋钮**该怎么调，存进每个旋钮的 `.grad` 小口袋里。

如果没有自动求导，一个百万旋钮的模型，你得手工推导一百万条调整公式——这就是深度学习在 PyTorch 这类工具出现前搞不起来的原因之一。

**最小例子**：让一个旋钮 `x` 自己学会变成「能让 `x²` 最小」的值（答案显然是 0，看机器怎么自己找到）：

```python
import torch

x = torch.tensor(3.0, requires_grad=True)  # 旋钮从3开始，requires_grad表示要记账
for i in range(20):  # 重复「打分→复盘→调整」20轮
    loss = x ** 2    # 打分：损失就是 x 的平方，越小越好
    loss.backward()  # 复盘：自动算出调整方向，存进 x.grad
    with torch.no_grad():
        x -= 0.1 * x.grad  # 调整：往反方向挪一小步（0.1是学习率）
    x.grad.zero_()   # 清空账本上的旧记录，准备下一轮
print(x)  # 输出一个非常接近 0 的数——它自己找到了答案！
```

**一句话总结**：张量装数字，自动求导替你算出「每个旋钮怎么调」，这是 PyTorch 的核心魔法。

---

### 4. 训练循环五部曲：投篮的标准流程

**生活比喻**：回到投篮。一个学生的每次练习一定是这五步：投篮 → 看落点偏差 → 复盘原因 → 调整动作 → 忘掉这一球、准备下一球。少任何一步都练不成。

**直觉解释**：把投篮流程翻译成代码，就是深度学习里大名鼎鼎的「训练五部曲」。每一小批数据（叫一个 batch，批次）都要完整走一遍：

1. **前向传播**：`预测 = model(数据)` —— 投篮
2. **算损失**：`loss = 损失函数(预测, 正确答案)` —— 看偏差
3. **梯度清零**：`optimizer.zero_grad()` —— 忘掉上一球的复盘笔记
4. **反向传播**：`loss.backward()` —— 复盘，算出每个旋钮怎么调
5. **更新参数**：`optimizer.step()` —— 真的拧旋钮（optimizer 优化器就是负责拧旋钮的助手）

**最小例子**：下面是一个完整可运行的训练循环，教模型学 `y = 2x + 1` 这个规律（故意只用 4 个数据点，让你看清全过程）：

```python
import torch
import torch.nn as nn

x = torch.tensor([[1.0], [2.0], [3.0], [4.0]])      # 输入
y = torch.tensor([[3.0], [5.0], [7.0], [9.0]])      # 正确答案：y = 2x + 1
model = nn.Linear(1, 1)                              # 只有 k 和 b 两个旋钮
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)  # 拧旋钮的助手
for epoch in range(500):                             # 500轮完整练习
    loss = nn.functional.mse_loss(model(x), y)       # 投篮 + 打分
    optimizer.zero_grad()                            # 清空旧笔记
    loss.backward()                                  # 复盘
    optimizer.step()                                 # 拧旋钮
print(model.weight.item(), model.bias.item())        # 约等于 2 和 1，学对了！
```

注意这里把五部曲里的「投篮」和「打分」写在了一行（`model(x)` 套在损失函数里），实际代码经常这么写。

**一句话总结**：五部曲是深度学习的「广播体操」，动作固定，做一万遍，模型就会了。

---

### 5. Dataset 与 DataLoader：冰箱与送餐传送带

**生活比喻**：学校食堂有一万道菜。`Dataset`（数据集）是冰箱的管理员，他只懂两件事：「一共有多少道菜」和「给我第 n 号菜」。`DataLoader`（数据加载器）是送餐传送带，它负责把菜一筐一筐端出来：每筐 32 道（`batch_size=32`）、端之前先把顺序打乱（`shuffle=True`）。

**直觉解释**：为什么不能一次把一万条数据全塞进模型？因为内存装不下，而且一次看太多反而学得慢。所以实际训练是「一小批一小批地喂」，这批数据走完五部曲，再喂下一批。

两个角色分工明确，别搞混：

- `Dataset` 管「一条数据怎么取」：你写两个方法，`__len__`（总数）和 `__getitem__`（按编号取一条）。
- `DataLoader` 管「怎么分批送」：打乱、分组、甚至多线程搬运，全自动。

**最小例子**：造一个装 10 条假数据的冰箱，再让传送带每筐送 4 条：

```python
from torch.utils.data import Dataset, DataLoader

class MyData(Dataset):
    def __len__(self):
        return 10                        # 一共10条数据
    def __getitem__(self, i):
        return f"第{i}号样本"             # 按编号取一条

loader = DataLoader(MyData(), batch_size=4, shuffle=True)
for batch in loader:
    print(batch)  # 每次打印一筐4条，顺序被打乱，最后一筐只有2条
```

**一句话总结**：Dataset 回答「怎么拿一条」，DataLoader 回答「怎么一筐筐送」，配合起来喂饱训练循环。

---

### 6. 模型保存与评估：存档与考试

**生活比喻**：学生练成神射手后要做两件事。第一，把练成的手感「存档」，不然睡一觉全忘了。第二，参加考试——考试时有考试纪律：不许再当场改动作（不许反向传播），而且要用正式比赛的投篮姿势，不是训练时的花样姿势。

**直觉解释**：

- **保存模型**：训练好的模型，值钱的就是那堆旋钮的位置。PyTorch 的标准做法是把所有旋钮位置打包成一个字典（叫 `state_dict`，状态字典）存进文件。注意只存旋钮，不存整个模型对象——存对象容易因为代码搬家而打不开。
- **评估模型**：`model.eval()` 把模型切到「考试模式」（某些只在训练时用的技巧会关掉，保证输出稳定）；`with torch.no_grad()` 告诉 PyTorch「考试了，别记账了」，省内存也更快。考试里只投篮、不复盘、不调整。

**最小例子**：存档 → 读档 → 用考试模式做预测：

```python
import torch
import torch.nn as nn

model = nn.Linear(1, 1)
torch.save(model.state_dict(), "/tmp/m.pth")  # 存档：只存旋钮位置
model.load_state_dict(torch.load("/tmp/m.pth"))  # 读档：把旋钮拧回去
model.eval()                                   # 切到考试模式
with torch.no_grad():                          # 考场纪律：不记账
    print(model(torch.tensor([[5.0]])))        # 正经预测一次
```

**一句话总结**：存档只存旋钮（`state_dict`），考试要 `eval()` 加 `no_grad()`，且考试期间绝不许改旋钮。

---

## 难点与易踩的坑

### 坑 1：忘了 `zero_grad()`，梯度越攒越多

**为什么难**：PyTorch 有个反直觉的设计——每次 `backward()` 算出的调整方向，默认是**累加**到旧记录上，而不是覆盖。官方这么设计有特殊用途，但把新手坑惨了。

**正确理解**：想象每轮复盘都往同一个笔记本上写字，不擦旧笔记的话，笔记越叠越厚，最后调整动作全乱套。所以五部曲里 `optimizer.zero_grad()` 必须每轮都擦一次笔记，一行都不能省。

### 坑 2：以为「模型学会了」就是真聪明了

**为什么难**：训练时损失降得很漂亮，不代表模型真的懂了。它可能只是把一万道例题的**答案背下来了**——这叫过拟合（overfitting），就像一个学生背完了练习册，换套新考卷就傻眼。

**正确理解**：所以一定要留一部分数据**训练时绝不给模型看**，专门用来考试（这就是验证集/测试集）。只有在没见过的数据上也表现好，才算真学会。

### 坑 3：学习率这个旋钮最玄

**为什么难**：学习率（每步挪多大）没有公式能算出最优值，只能试。太大，一步跨过谷底，在山两边来回蹦甚至越弹越高；太小，挪到天荒地老还没下山。

**正确理解**：先记住一个经验值 `0.01` 或 `0.001`，看损失变化再调：损失乱跳就调小，半天不动就调大。这是深度学习里「调参」的日常。

### 坑 4：`model.eval()` 和 `torch.no_grad()` 傻傻分不清

**为什么难**：这俩经常一起出现，新手以为是一回事。其实它们管的是两件完全不同的事：`eval()` 管的是「某些层在考试时要换行为」，`no_grad()` 管的是「别记账省内存」。只用一个是常见 bug。

**正确理解**：记住口诀——**评估阶段两个都要**。就像进考场既要穿校服（eval），又要交手机（no_grad）。

### 坑 5：觉得深度学习是「理解」，其实它是「找规律」

**为什么难**：这是最反直觉的一点。模型认出猫，并不是因为它「理解」了猫是什么动物——它只是在上百万个旋钮里找到了一种能把「猫的照片」映射到「猫」这个答案的数学规律。它不认识猫，它只认识像素规律。

**正确理解**：明白这一点，你就能理解 AI 的很多怪现象：为什么换张奇怪角度的照片它就认错，为什么它有时一本正经地胡说八道。它不是人脑，是一台巨大的「规律匹配机」。

---

## PyTorch 最佳实践清单

下面是从项目实战中总结的 12 条铁律——每个踩过坑的人都会告诉你的话。

### 设备管理

```python
# ✅ 好：统一管理设备，代码到处可用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyModel().to(device)

# ❌ 坏：硬编码 'cuda'，换台没有 GPU 的电脑直接报错
model = MyModel().cuda()

# ✅ 好：数据也记得搬到同一设备
x, y = x.to(device), y.to(device)

# ❌ 易错：张量在 CPU、模型在 GPU，报错 "Expected all tensors to be on the same device"
```

### 训练循环模板

```python
def train_one_epoch(model, loader, optimizer, loss_fn, device):
    model.train()  # ✅ 训练前切训练模式
    total_loss = 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()       # 第 3 步：清空
        pred = model(x)             # 第 1 步：投篮
        loss = loss_fn(pred, y)     # 第 2 步：打分
        loss.backward()             # 第 4 步：复盘
        optimizer.step()            # 第 5 步：调整

        total_loss += loss.item()   # ✅ .item() 把单元素张量变成 Python float
    return total_loss / len(loader)

@torch.no_grad()  # ✅ 装饰器写法更简洁，整个函数不记账
def evaluate(model, loader, loss_fn, device):
    model.eval()
    total_loss = 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = loss_fn(pred, y)
        total_loss += loss.item()
    return total_loss / len(loader)
```

### 常见错误信息速查

| 报错信息 | 原因 | 解法 |
|---------|------|------|
| `RuntimeError: Expected all tensors to be on the same device` | 张量在 CPU、模型在 GPU（或反了） | 把张量 `.to(device)`，和模型同一设备 |
| `RuntimeError: Trying to backward through the graph a second time` | 对一个 loss 调了两次 `backward()` | 要么 `retain_graph=True`（不推荐新手用），要么重新前向传播 |
| `UserWarning: Creating a tensor from a list of numpy.ndarrays is extremely slow` | 从 numpy 列表直接造 tensor | 先 `np.stack()` 转成一个大数组，再 `torch.from_numpy()` |
| `ValueError: Expected more than 1 value per channel when training` | BatchNorm 收到 batch_size=1 的输入 | 设 `DataLoader(drop_last=True)` 丢弃最后不完整的 batch |
| `RuntimeError: CUDA out of memory` | 显存不够 | 减小 batch_size、减小模型、用 `torch.cuda.empty_cache()` |
| 损失变成 `nan` | 学习率太大导致参数爆炸 | 调小 lr（先除 10），加梯度裁剪 `torch.nn.utils.clip_grad_norm_` |
| 损失一直不降 | 学习率太小或模型太简单 | 调大 lr、加层数、检查数据是否 normalize 过 |

### 调参速查表

```
问题现象                          →  尝试方案
──────────────────────────────────────────────────
训练损失不降                       →  增大 lr、检查数据归一化、检查标签是否正确
验证损失远高于训练损失（过拟合）     →  加 Dropout、减小模型、加数据增强、早停
训练损失震荡剧烈                   →  减小 lr、增大 batch_size
损失下降但验证损失不再改善           →  早停（early stopping）、降低 lr
损失降到一定值后不再动               →  减小 lr、检查梯度是否消失
第一个 batch 就 nan                →  减小 lr（先除 100）、检查输入数据有没有 nan
```

---

## 实战练习：从看懂到会做

### 练习一：自己写五部曲（15 分钟）

**任务**：用 PyTorch 训练一个模型学 `y = 3x² - 2x + 1` 这个二次函数。

与文章里 `y = 2x + 1` 不同：这次是**非线性**的，所以一层 `nn.Linear(1, 1)` 不够（它只能学直线）。你需要搭一个至少**两层的网络**，中间加 ReLU 激活函数来引入非线性。

**脚手架**：

```python
import torch
import torch.nn as nn

# 造数据：y = 3x² - 2x + 1，加一点噪声模拟真实场景
torch.manual_seed(42)
x = torch.linspace(-2, 2, 200).reshape(-1, 1)  # 200 个点，从 -2 到 2
y_true = 3 * x**2 - 2 * x + 1
y = y_true + torch.randn_like(x) * 0.3          # 加点噪声

# TODO: 搭一个两层网络
# 第一层：1 → 16（输入 1 个 x，扩展到 16 个隐藏神经元）
# 激活：ReLU（nn.ReLU()）
# 第二层：16 → 1（16 个隐藏神经元汇合到 1 个输出）
model = nn.Sequential(
    # 填你的代码
)

loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# TODO: 写训练循环（500 轮）
for epoch in range(500):
    # 五部曲
    pass

# 测试：看看模型学会了吗
model.eval()
with torch.no_grad():
    test_x = torch.tensor([[-1.0], [0.0], [1.0], [2.0]])
    pred = model(test_x)
    true = 3 * test_x**2 - 2 * test_x + 1
    for i in range(len(test_x)):
        print(f"x={test_x[i].item():.0f}, 预测={pred[i].item():.3f}, 真实={true[i].item():.3f}")
```

<details>
<summary>点击查看答案</summary>

```python
import torch
import torch.nn as nn

torch.manual_seed(42)
x = torch.linspace(-2, 2, 200).reshape(-1, 1)
y_true = 3 * x**2 - 2 * x + 1
y = y_true + torch.randn_like(x) * 0.3

# 两层网络：线性1 → ReLU → 线性2
model = nn.Sequential(
    nn.Linear(1, 16),   # 1 个输入 → 16 个隐藏神经元
    nn.ReLU(),          # 非线性激活（没有它就只能学直线！）
    nn.Linear(16, 1),   # 16 个隐藏 → 1 个输出
)

loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(500):
    pred = model(x)                 # 1. 前向
    loss = loss_fn(pred, y)         # 2. 损失
    optimizer.zero_grad()           # 3. 清零
    loss.backward()                 # 4. 反向
    optimizer.step()                # 5. 更新

model.eval()
with torch.no_grad():
    test_x = torch.tensor([[-1.0], [0.0], [1.0], [2.0]])
    pred = model(test_x)
    true = 3 * test_x**2 - 2 * test_x + 1
    for i in range(len(test_x)):
        print(f"x={test_x[i].item():.0f}, 预测={pred[i].item():.3f}, 真实={true[i].item():.3f}")
    # 预期输出大致接近: 6, 1, 2, 9（真实值为 6, 1, 2, 9）
```
</details>

---

### 练习二：MNIST 手写数字识别（30 分钟）

**任务**：这是深度学习的 "Hello World"——训练一个网络识别 0-9 的手写数字。PyTorch 自带这个数据集，不需要额外下载。

你要写：Dataset 准备 → 模型搭建 → 训练循环 → 评估准确率。

**脚手架**：

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 准备数据：把 28×28 的图片拉平成 784 个数，归一化到 [0, 1]
transform = transforms.Compose([
    transforms.ToTensor(),                     # PIL 图片 → Tensor，值在 [0, 1]
    transforms.Lambda(lambda x: x.view(-1)),   # 拉平成 784 维向量
])

train_data = datasets.MNIST(root="./mnist_data", train=True,
                            download=True, transform=transform)
test_data = datasets.MNIST(root="./mnist_data", train=False,
                           download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# TODO: 搭模型——784 输入 → 128 隐藏 → 64 隐藏 → 10 输出（每个数字一个分数）
model = nn.Sequential(
    # 填你的代码
    # 提示：最后一层不需要激活函数，因为 CrossEntropyLoss 内部会做 Softmax
)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# TODO: 训练 3 个 epoch
# 每个 epoch = 所有训练数据过一遍
# 每 100 个 batch 打印一次损失

# TODO: 评估——在整个测试集上算准确率
# 提示：pred.argmax(dim=1) 取分数最高的那个类别
```

<details>
<summary>点击查看答案</summary>

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 准备数据
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.view(-1)),
])

train_data = datasets.MNIST(root="./mnist_data", train=True,
                            download=True, transform=transform)
test_data = datasets.MNIST(root="./mnist_data", train=False,
                           download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# 搭模型
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Dropout(0.2),        # 随机关掉 20% 神经元，防过拟合
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10),      # 10 个输出 = 10 个数字类别
)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 训练
for epoch in range(3):
    model.train()
    running_loss = 0.0
    for batch_idx, (x, y) in enumerate(train_loader):
        x, y = x.to(device), y.to(device)

        pred = model(x)
        loss = loss_fn(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 100 == 99:
            avg_loss = running_loss / 100
            print(f"Epoch {epoch+1}, Batch {batch_idx+1}: loss = {avg_loss:.4f}")
            running_loss = 0.0

# 评估准确率
model.eval()
correct, total = 0, 0
with torch.no_grad():
    for x, y in test_loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        correct += (pred.argmax(dim=1) == y).sum().item()
        total += y.size(0)

print(f"\n测试集准确率: {correct}/{total} = {100 * correct / total:.2f}%")
# 预期：3 个 epoch 就能到 96% 左右——这就是深度学习的威力
```
</details>

---

### 练习三：过拟合 vs. 泛化实验（15 分钟）

**任务**：故意制造过拟合，然后亲眼看到正则化（Dropout + 权重衰减）能缓解。

在练习二的基础上，做一个小实验：

1. **不用 Dropout**，训练 10 个 epoch，记录训练集和测试集的准确率——你会发现训练集准确率很高（接近 100%），但测试集远低于训练集。这就是过拟合。
2. **加上 Dropout(0.3)**，同样训练 10 个 epoch——测试集准确率应该更高，且跟训练集的差距更小。

```python
# 实验记录模板
print(f"{'配置':<20} {'训练准确率':<12} {'测试准确率':<12} {'差距':<10}")
print("-" * 54)

for name, use_dropout, use_weight_decay in [
    ("无正则化", False, False),
    ("只用Dropout", True, False),
    ("Dropout+权重衰减", True, True),
]:
    # 搭模型、训练、评估...
    # print(f"{name:<20} {train_acc:<12.2%} {test_acc:<12.2%} {train_acc - test_acc:<10.2%}")
```

---

## 一条完整的训练脚本骨架

以后你自己写训练代码时，直接套这个骨架：

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# ===== 1. 超参数 =====
config = {
    "lr": 0.001, "batch_size": 64, "epochs": 10,
    "patience": 3,  # 早停：连续 3 轮不改善就停止
}

# ===== 2. 数据 =====
train_loader = DataLoader(train_dataset, batch_size=config["batch_size"], shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=config["batch_size"], shuffle=False)

# ===== 3. 模型、损失、优化器 =====
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = YourModel().to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=config["lr"])

# ===== 4. 训练循环（带早停） =====
best_val_loss = float("inf")
patience_counter = 0

for epoch in range(config["epochs"]):
    # --- 训练 ---
    model.train()
    train_loss = 0.0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    # --- 验证 ---
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            val_loss += loss_fn(model(x), y).item()

    train_loss /= len(train_loader)
    val_loss /= len(val_loader)
    print(f"Epoch {epoch+1}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}")

    # --- 早停检查 ---
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), "best_model.pt")  # 保存最好的
    else:
        patience_counter += 1
        if patience_counter >= config["patience"]:
            print(f"早停！第 {epoch+1} 轮停止")
            break

# ===== 5. 加载最佳模型做最终评估 =====
model.load_state_dict(torch.load("best_model.pt"))
# ... 在测试集上评估
```

---

## 学完能做什么 & 下一步

学会这套东西，你已经摸到了现代 AI 的大门把手。具体能做的事比如：

- **手写数字识别**：用经典的 MNIST 数据集（几万张手写数字图片）训练一个小网络，让电脑认出你手写的 0-9。这是深度学习的「Hello World」，几十行代码就能跑通。
- **影评情感分析**：喂给模型大量「影评 + 好评/差评标签」，它就能判断一条新影评是在夸还是在骂。网上垃圾评论过滤就是这么做的。
- **理解大模型的训练**：ChatGPT 这类大模型，训练核心依然是今天这五部曲，只是旋钮从 2 个变成了千亿个、数据从 4 行变成了整个互联网。原理你懂了，剩下的主要是工程规模问题。

**下一步建议路径**：

1. 先把本文的代码亲手敲一遍、改一改（比如让模型学 `y = 3x - 2`，看旋钮最后是多少）。
2. 学习用 NumPy 处理数据、了解矩阵乘法——这是看懂更复杂网络的钥匙。
3. 啃下 MNIST 手写数字识别的完整教程，第一次体验「从图片到预测」的全流程。
4. 之后再碰卷积网络（处理图片的专用结构）、Transformer（大语言模型的核心结构）这些进阶话题。

记住：深度学习这个领域，看懂和会做之间隔着一次亲手敲代码。先去跑一遍代码吧。
