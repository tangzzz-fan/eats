# 数学与机器学习基础：写给高中生的入门指南

你有没有想过：为什么购物软件总能猜到你想买什么？为什么手机相册能自动把"同一个人的照片"归到一起？为什么天气预报能说明天大概多少度？

这些事情背后，是同一套基本功：**把现实世界的东西变成数字（向量、矩阵、张量），用飞快的速度对数字做运算（向量化与广播），再从数字里自动找规律（聚类），甚至根据过去推测未来（时间序列）**。这就是"数学与机器学习基础"这个方向要教你的东西。

读这篇文章时，你可以一直带着一个比喻：**把机器学习想象成一所学校**。

- 每个学生就是一条数据，他的成绩单（数学、语文、英语分数）就是一个**向量**；
- 全年级的成绩花名册就是一个**矩阵**；
- 让全校学生一起做广播体操，而不是一个个单独做，就是**向量化**；
- 广播体操时班级人数不一样多，怎么对齐站位，就是**广播**；
- 不看任何标签，按兴趣把学生自动分成几个社团，就是 **K-Means 聚类**；
- 根据过去几次月考成绩预测下一次考试，就是**时间序列分析**。

整篇文章我们都会回到这所学校。

---

## 先建立直觉

先用一个日常场景，看看这个领域到底要解决什么问题。

假设你开了个水果摊，记录了一个月的数据：每天卖了多少苹果、气温多少度、周几。现在你想回答三个问题：

1. **"这两天的生意像不像？"** —— 这需要先把"一天"变成一串数字，然后比较两串数字的"距离"。
2. **"这个月的日子能不能自动分成几类？比如'好卖的日子'和'不好卖的日子'？"** —— 你手里没有标准答案，得让算法自己分组。
3. **"明天大概能卖多少？"** —— 你要利用过去 30 天的顺序规律来预测未来。

这三个问题，正好对应这个方向的三块内容：**用向量/矩阵表示数据、用聚类找隐藏的分组、用时间序列预测未来**。而要让这一切在电脑上跑得动（一个月的数据好说，一百万行呢？），就需要 NumPy 的向量化和广播。

所以这条学习路线非常自然：

```text
把东西变成数字  →  快速地算  →  从数字里找规律  →  用规律预测
（向量/矩阵/张量）   （向量化/广播）   （K-Means 聚类）   （时间序列）
```

---

## 知识地图

先给你一张全局地图，知道要学哪几块，再逐个展开。

| # | 核心知识点 | 一句话概括 |
| --- | --- | --- |
| 1 | 向量 / 矩阵 / 张量 | 就是把数据装进一层、两层、更多层的"盒子"，维度（维度数）就是盒子的层数 |
| 2 | 向量化（Vectorization） | 把"一个个算"换成"一整批一起算"，速度差几十上百倍 |
| 3 | 广播（Broadcasting） | 形状不同的数组做运算时，NumPy 自动"复制补齐"让它们对齐 |
| 4 | K-Means 聚类 | 不给标准答案，反复"归类、移动中心"，自动把相似数据分成 K 组 |
| 5 | 时间序列整理：重采样与前向填充 | 把节奏不齐的数据对齐到固定时间格子上，空缺的用"上一个值"补上 |
| 6 | 时间序列预测：历史特征与时序铁律 | 给模型看"前几天的数据"当记忆，训练/测试切分绝不打乱时间顺序 |

---

## 重点逐个讲

### 1. 向量、矩阵、张量：把世界装进不同层数的盒子

**生活比喻**：成绩单。

一个学生的成绩单 `[数学 90, 语文 85, 英语 88]`，就是一行 3 个数字——这叫**向量（vector，一维数组）**。一个班 30 个学生的成绩单摞在一起，30 行 3 列——这叫**矩阵（matrix，二维数组）**。全校 10 个班的成绩单摞成一沓，10 × 30 × 3——三层盒子，这就叫**张量（tensor）**。

**直觉解释**：别被"线性代数"四个字吓到。对程序员来说，这些概念就是你已经会的东西：标量是单个数字，向量是列表，矩阵是"列表的列表"，张量是"列表的列表的列表"。区别只在盒子有几层，术语上叫有几个**维度（dimension，可以简单理解为"用几个下标才能定位一个数"）**。

为什么要把数据装盒子？因为计算机只认数字。你想让电脑理解"一个学生"、"一张照片"、"一句话"，第一步永远是把它们变成某种层数的数组。照片是三维张量（高 × 宽 × 红绿蓝三个颜色通道），一批照片就是四维的。

**最小例子**：

```python
import numpy as np

student = np.array([90, 85, 88])            # 向量：一个学生的三科成绩
classroom = np.array([[90, 85, 88],
                      [70, 92, 80]])        # 矩阵：两个学生的成绩单
print(student.shape)     # (3,)   一维，3 个数
print(classroom.shape)   # (2, 3) 两行三列
print(classroom[1, 2])   # 80  第 2 个学生的英语成绩
```

注意 `.shape`（形状）这个东西：它告诉你盒子每层多大。它是后面一切运算的"身份证"，出 bug 时第一件事就是打印它。

**一句话总结**：向量、矩阵、张量不是高深数学，就是一层、两层、N 层的数字盒子，机器学习的第一步就是把世界装进盒子里。

---

### 2. 向量化：让全校一起做广播体操

**生活比喻**：做广播体操。校长可以让 1000 个学生排队，挨个单独喊"第一节，第二节……"做一遍；也可以喇叭一响，全校同时做。前者叫 `for` 循环，后者叫**向量化（vectorization，对一整块数据一次性施加同一个操作）**。

**直觉解释**：Python 的列表很灵活，但灵活有代价——列表里每个元素都是"贴了标签的小包裹"，每算一次电脑都要拆开看标签（类型检查）。NumPy 数组则是"一整箱一模一样的苹果"，紧挨着码放，电脑可以一整排一整排地搬。所以同样算 100 万个数的平方，循环要几秒，NumPy 只要几毫秒。

这个方向里你只要记住一件事：**能写 `arr ** 2` 就别写 `for` 循环**。后面的 K-Means、时间序列，所有"快"都来自这一条。

**最小例子**：

```python
import numpy as np

arr = np.arange(10)          # [0 1 2 ... 9]
squares = arr ** 2           # 一整批同时平方，不用写循环
doubled = arr * 2            # 一整批同时乘 2
print(squares)   # [0 1 4 9 16 25 36 49 64 81]
print(arr + 100) # 每个数都加 100，也是一次完成的
```

**一句话总结**：向量化 = 把"一个个做"改成"一整批一起做"，这是所有科学计算快的根源。

---

### 3. 广播：人数不同时的自动对齐术

**生活比喻**：还是广播体操。一个班 5 排，另一个班 3 排，要比对两队学生的站位。老师不会真的把人复制一遍，而是"脑补"：把单人示范的动作，默认应用到每一排。**广播（broadcasting）**就是 NumPy 的这种"脑补"：形状不同的两个数组做运算时，自动把小的那个"复制扩展"到能对齐。

**直觉解释**：你已经见过最简单的广播了——上一节的 `arr + 100`，`100` 是一个数，`arr` 是 10 个数，NumPy 自动把 `100` 当成 10 个 `100` 来加。推广到多维只有一条口诀：**从右往左对比形状，每一层要么相等、要么其中一边是 1，就能对上**。

这个能力最经典的用途：一口气算出"每个数据点到每个中心点的距离"——这正是 K-Means 的心脏。

**最小例子**（3 个点 × 2 个中心，一次算完全部 6 个距离）：

```python
import numpy as np

points  = np.array([[0, 0], [3, 4], [6, 8]])  # 3 个点的坐标
centers = np.array([[0, 0], [10, 0]])          # 2 个中心的坐标
diff = points[:, np.newaxis, :] - centers      # 自动补齐成 (3, 2, 2)
dist = np.sqrt((diff ** 2).sum(axis=-1))       # 沿坐标维求和再开方
print(dist)  # 每行是一个点到两个中心的距离，如 [0. 10.]、[5. 5.]
```

`np.newaxis` 的意思是"在这里凭空加一层盒子"。加在哪一层决定了谁和谁配对，这是新手最容易翻车的地方，难点一节还会说。

**一句话总结**：广播就是形状不同时的自动对齐规则——"从右往左，相等或有 1 就能对上"，学会它能少写 90% 的循环。

---

### 4. K-Means 聚类：没人当裁判，也能自动分社团

**生活比喻**：开学第一天，老师说："按兴趣自己组成 2 个社团，我不告诉你们谁属于哪个社。"学生们只好先随便选 2 个"临时社长"站到场地上，每个人走到离自己最近的社长那边；然后每个社重新把"社团的中心位置"定在所有成员的平均位置；大家再看自己离哪个新中心近，重新站队……几轮之后，队伍就稳定了。这就是 **K-Means（K 均值聚类，把数据自动分成 K 组，每组以自己成员的平均位置为中心）**。

**直觉解释**：这属于**无监督学习（unsupervised learning，没有标准答案、没有老师，算法自己从数据里找结构）**。它只有四步循环：随机选 K 个中心 → 每个点归入最近的中心 → 把每个中心移到组员平均位置 → 重复直到中心不再动。

我们用 6 个一维数字手算一遍，你就能彻底看懂。数据：`1, 2, 3, 10, 11, 12`，K=2，随机选中心 `1` 和 `10`：

```text
第 1 轮：归组  →  离 1 近：{1,2,3}    离 10 近：{10,11,12}
         移中心 →  新中心 = 平均数： 2        和  11
第 2 轮：归组  →  还是 {1,2,3} 和 {10,11,12}，中心不再移动
         收敛！最终分组：小组围绕 2，大组围绕 11
```

**最小例子**（和手算完全一致的代码版）：

```python
import numpy as np

X = np.array([1, 2, 3, 10, 11, 12])      # 一维数据
centers = np.array([1.0, 10.0])          # 随机初始化两个中心
for _ in range(10):
    d = np.abs(X[:, np.newaxis] - centers)   # 每个点到各中心的距离
    label = d.argmin(axis=1)                 # 归入最近的那一组
    centers = np.array([X[label == k].mean() for k in range(2)])
print(centers)  # [ 2. 11.] 和手算一模一样
```

**一句话总结**：K-Means 就是"归最近的组、移到组平均、反复直到不动"，聚类不需要标准答案，相似的东西自然会凑到一起。

---

### 5. 时间序列整理：把不齐的钟表对齐

**生活比喻**：体测时老师每隔 10 秒记一次你的心率，但手表不靠谱，有时 3 秒报一次，有时半分钟没动静。你要画曲线，得先把数据"对齐到每 10 秒一格"：格子里有多个读数就取平均，格子空着怎么办？心率不会瞬间变成 0，最合理的填法是"沿用上一格的读数"。

**直觉解释**：这就是时间序列数据的第一步整理。**重采样（resampling，按固定时间间隔重新切分聚合数据）**负责对齐格子；**前向填充（forward fill，用前一个有效值填补空缺）**负责补空格。为什么不能用 0 填？因为温度、车速、心率这类物理量是连续的，填 0 等于说"那一秒世界暂停了"，会把后面的模型骗惨。

**最小例子**（纯 Python 演示前向填充的思想）：

```python
temps = [20, 21, None, None, 23, None]   # None 表示这一秒没采到数据
filled, last = [], None
for t in temps:
    if t is not None:        # 采到了新值
        last = t
    filled.append(last)      # 没采到就沿用上一次
print(filled)  # [20, 21, 21, 21, 23, 23] 空缺处都被"上一秒"填上了
```

实际工作里不用手写循环，`pandas`（Python 里最常用的表格数据库）一行就能搞定：`df.resample('10s').mean().ffill()`，意思和上面完全一样。

**一句话总结**：时间序列先对齐到固定格子，空缺处用"上一个值"而不是 0 来填——因为物理世界是连续的。

---

### 6. 给模型"历史记忆"，以及一条绝不能违反的铁律

**生活比喻**：问一个学生"你下次月考能考多少分？"只看这一次的成绩没法猜，但如果给你看"最近三次的平均分"和"上上次、上次的分数"，你就能看出他在进步还是退步。机器也一样：**想预测未来，必须先把"过去"变成模型能看到的列**。

**直觉解释**：两个常用招。**滑动窗口（rolling，用最近 N 个值的平均来平滑数据）**像"近三次月考平均分"，能抹掉偶然波动、看清趋势；**时滞特征（lag，把整列数据向下挪几行变成新列）**像把"上次成绩"抄到这次旁边，让模型在每一时刻都能看到自己的历史。

然后是这条**铁律**：普通机器学习切分训练集/测试集时会随机打乱（shuffle），时间序列**绝对禁止**。你只能按时间切一刀：前面的日子用来学，后面的日子用来考。否则相当于考试时偷看了答案——模型"见过未来"，测出来的高分全是假的。

**最小例子**：

```python
sales = [10, 12, 11, 13, 15, 14, 16]      # 一周的销量，顺序就是时间
rolling_avg = [round(sum(sales[i-2:i+1]) / 3, 1) for i in range(2, len(sales))]
print(rolling_avg)     # [11.0, 12.0, 13.0, 14.0, 15.0] 近 3 天平均

cut = int(len(sales) * 0.8)               # 按时间切一刀，绝不打乱
train, test = sales[:cut], sales[cut:]
print(train, test)     # [10, 12, 11, 13, 15] [14, 16]
```

**一句话总结**：预测未来 = 给模型看历史（滑窗 + 时滞），并且永远只用"过去"学习、用"未来"考试。

---

## 难点与易踩的坑

下面这几个点，是这个方向里新手公认最容易栽跟头的地方。

**1. `(3,)` 和 `(3, 1)` 不是一回事**
- 为什么难：看起来都像"3 个数"，但前者是一层盒子里装 3 个数（向量），后者是两层盒子（3 行 1 列的矩阵）。形状不同，广播的结果就完全不同。
- 怎么正确理解：少想当然，多 `print(x.shape)`。形状是数组的身份证，写每一行 NumPy 代码时心里都要默念"现在它是几层、每层多大"。

**2. `np.newaxis` 加错位置**
- 为什么难：广播时"凭空加一层"加在第几层，决定了谁和谁配对。算"每个点到每个中心的距离"时，点要加在中间层、中心加在最外层；加反了不会报错，只是结果静悄悄地全错——这是最可怕的一类 bug。
- 怎么正确理解：动手前先在纸上写出你想要的最终形状（比如 `(5, 3, 2)`：5 个点 × 3 个中心 × 2 个坐标），再倒推每个数组该在哪一层补 `1`。

**3. K-Means 的答案不唯一**
- 为什么难：初始中心是随机选的，选得不好，算法可能收敛到一个"局部还行但不是全局最好"的分组；而且 K（分几组）本身也要人拍脑袋定。很多同学以为"算法跑出来的就是真理"。
- 怎么正确理解：K-Means 给的是"一种合理的分法"，不是"唯一正确的分法"。工程上的对策是换几组随机初始中心多跑几次，取结果最好的那次。

**4. 用 0 填充缺失的时间数据**
- 为什么难：填 0 最顺手，表格里空格填 0 天经地义。但温度从 22 度"跳"到 0 度再跳回来，模型会真以为发生了两次剧变。
- 怎么正确理解：先问自己"这个量在物理上会不会瞬间归零"。车速、体温、股价都不会，所以用前向填充；真的表示"没发生"的量（比如这一小时的事故次数）才可以填 0。

**5. 时间序列随机打乱（数据泄露）**
- 为什么难：`train_test_split(shuffle=True)` 是普通机器学习的标准动作，肌肉记忆很容易带过来。打乱后模型在训练时"见过"测试时间段的邻居数据，准确率高得离谱，还特别有迷惑性。
- 怎么正确理解：把"用未来预测过去"当成作弊。时间序列的切分只有一句话——**按时间切一刀，前训练、后测试**。看到时序模型准确率高得反常时，第一反应应该是查有没有数据泄露，而不是庆祝。

---

## NumPy 最佳实践清单

在你继续深入之前，花 5 分钟记住下面这 10 条——它们是我（和无数前辈）用 bug 堆出来的经验。

### 数据创建

```python
import numpy as np

# ✅ 好：创建时直接指定 dtype，避免后续类型转换
scores = np.array([85, 90, 88], dtype=np.float32)

# ❌ 坏：不指定 dtype，全是 Python int 或 object
scores = np.array([85, 90, 88])

# ✅ 好：用 np.linspace 创建等间距数列
x = np.linspace(0, 1, 100)  # 0 到 1 之间均匀取 100 个点

# ❌ 坏：手写等差数列
x = np.array([i * 0.01 for i in range(100)])  # 慢、不精确、有浮点累积误差

# ✅ 好：np.zeros / np.ones 预分配数组
result = np.zeros((100, 3))  # 先挖好坑，后面往里填数

# ❌ 坏：用 list append 再转 array（每次 append 都重新分配内存）
result = []
for i in range(100):
    result.append([0, 0, 0])
result = np.array(result)  # 慢，且浪费内存
```

### 索引与切片

```python
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# ✅ 好：用列表一次取多行多列
print(arr[[0, 2]])          # 取第 0 行和第 2 行
print(arr[:, [1, 3]])       # 取第 1 列和第 3 列

# ✅ 好：布尔索引过滤
print(arr[arr > 5])         # 所有大于 5 的元素：[6 7 8 9 10 11 12]

# ⚠️ 注意：切片是"视图"，改了会影响原数组！
view = arr[:2, :2]
view[0, 0] = 999
print(arr[0, 0])  # 999！原数组被改了

# ✅ 如果想独立拷贝，用 .copy()
safe = arr[:2, :2].copy()
safe[0, 0] = 0
print(arr[0, 0])  # 还是 999，不受影响
```

### 形状操作

```python
arr = np.arange(12)  # [0 1 2 ... 11]

# reshape：改形状但总元素数不能变
print(arr.reshape(3, 4))   # 3 行 4 列
print(arr.reshape(2, 2, 3))  # 2 块 × 2 行 × 3 列

# 用 -1 让 NumPy 自动推算这一维的大小
print(arr.reshape(3, -1))  # 等价于 reshape(3, 4)，因为 12/3=4

# flatten vs ravel：都"拍平"成一维
# flatten() 始终返回副本；ravel() 尽量返回视图（更快）
flat = arr.reshape(3, 4).flatten()  # 安全，不牵动原数组
```

### 性能三连

```python
# 1. 永远避免 Python 级别的 for 循环处理数组元素
# ❌ 坏：
result = []
for x in np.arange(1_000_000):
    result.append(x ** 2)
# ✅ 好：
result = np.arange(1_000_000) ** 2

# 2. 用 @ 或 np.dot 做矩阵乘法，不要手写三重循环
A = np.random.rand(100, 100)
B = np.random.rand(100, 100)
C = A @ B  # 底层调 BLAS 库，比 Python 循环快 1000 倍

# 3. 能用 numpy 内置函数的别自己写
# ❌ 坏：
total = sum(arr)  # Python sum，慢
# ✅ 好：
total = np.sum(arr)  # NumPy sum，快
# 同样的：max→np.max, min→np.min, any→np.any, all→np.all
```

---

## 实战练习：从看懂到会做

下面三组练习按难度递进，每一组都配了参考答案。**强烈建议你亲自动手敲代码**——只看不写，这篇文章的收获打三折。

---

### 练习一：广播热身（10 分钟）

**任务**：给你一个 4×3 的矩阵（4 行数据，每行 3 个特征），现在要做**标准化**（Standardization）：对每一列，每个数减去该列的均值，再除以该列的标准差。

标准化公式：`新值 = (原值 - 该列均值) / 该列标准差`

要求只用向量化操作（不能用 for 循环），看看你能不能用广播一行搞定。

**提示**：矩阵是 `(4, 3)`，均值是 `(3,)`——广播会怎么对齐？从右往左推演。

<details>
<summary>点击查看答案</summary>

```python
import numpy as np

# 造数据：4 个样本，每个样本 3 个特征
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]], dtype=np.float64)

# 一行搞定标准化：列均值是 shape (3,)，列标准差也是 (3,)
# X 是 (4, 3)，广播规则：从右往左，(3,) 匹配 (3,)，OK
X_norm = (X - X.mean(axis=0)) / X.std(axis=0)

print("原始：")
print(X)
print("\n标准化后（每列均值约 0，标准差约 1）：")
print(X_norm)
print(f"\n每列均值: {X_norm.mean(axis=0)}")  # 应该都接近 0
print(f"每列标准差: {X_norm.std(axis=0)}")    # 应该都接近 1
```
</details>

---

### 练习二：从零实现 K-Means（20 分钟）

**任务**：写一个完整的 K-Means 函数，输入是二维数据点（比如 `(x, y)` 坐标），输出每个点属于哪个簇。

要求：
1. 随机选 K 个数据点作为初始中心（而不是全随机在空间里撒，这样更稳定）
2. 循环直到中心不再变化（或变化小于阈值 `tol`）
3. 返回最终的标签和中心坐标

**脚手架**：

```python
import numpy as np

def kmeans(X, k, max_iters=100, tol=1e-4):
    """
    X: 形状 (n_samples, n_features) 的数据
    k: 簇的数量
    max_iters: 最多迭代次数
    tol: 中心移动小于此值即认为收敛
    返回: (labels, centers)
    """
    n = X.shape[0]

    # TODO 1: 随机选 k 个不重复的索引，用它对应的 X 做初始中心
    # 提示: np.random.choice(n, k, replace=False)

    # TODO 2: 写循环
    for iteration in range(max_iters):
        # 2a: 算每个点到每个中心的距离（用广播！）
        # 提示: 形状要想好——点 (n, 2)，中心 (k, 2)，距离矩阵该是 (n, k)
        # 怎么做？给点加一层 → (n, 1, 2)，广播相减得 (n, k, 2)，再平方求和开方

        # 2b: 每个点归入最近的中心
        # 提示: .argmin(axis=1)

        # 2c: 更新中心
        # 提示: np.array([X[labels == i].mean(axis=0) for i in range(k)])

        # 2d: 检查中心移动是否小于 tol，是的话 break

    # 最后再跑一次分类（用最终中心），返回 labels 和 centers
    pass  # 替换为你的代码


# 测试数据：肉眼可辨的三堆点
np.random.seed(42)
c1 = np.random.randn(30, 2) * 0.5 + [2, 2]    # 围绕 (2,2) 的 30 个点
c2 = np.random.randn(30, 2) * 0.5 + [-2, -2]   # 围绕 (-2,-2) 的 30 个点
c3 = np.random.randn(30, 2) * 0.5 + [2, -2]    # 围绕 (2,-2) 的 30 个点
X = np.vstack([c1, c2, c3])
np.random.shuffle(X)  # 打乱顺序

labels, centers = kmeans(X, k=3)
print("最终中心：")
print(centers)
print(f"每簇点数：{[sum(labels == i) for i in range(3)]}")
```

<details>
<summary>点击查看完整答案</summary>

```python
import numpy as np

def kmeans(X, k, max_iters=100, tol=1e-4):
    n = X.shape[0]

    # 1. 随机选 k 个不重复的数据点作为初始中心
    idx = np.random.choice(n, k, replace=False)
    centers = X[idx].astype(np.float64)

    for iteration in range(max_iters):
        # 2a. 算距离矩阵 (n, k)：每个点到每个中心的欧氏距离
        # X: (n, 2) → 加轴 → (n, 1, 2)
        # centers: (k, 2)
        # diff: 广播 → (n, k, 2)
        diffs = X[:, np.newaxis, :] - centers[np.newaxis, :, :]
        distances = np.sqrt((diffs ** 2).sum(axis=2))

        # 2b. 每个点归入最近的中心
        labels = distances.argmin(axis=1)

        # 2c. 更新中心
        new_centers = np.array([X[labels == i].mean(axis=0) for i in range(k)])

        # 2d. 检查收敛
        shift = np.sqrt(((new_centers - centers) ** 2).sum())
        if shift < tol:
            print(f"第 {iteration + 1} 轮收敛，中心移动 = {shift:.6f}")
            break

        centers = new_centers

    # 最终分配
    diffs = X[:, np.newaxis, :] - centers[np.newaxis, :, :]
    distances = np.sqrt((diffs ** 2).sum(axis=2))
    labels = distances.argmin(axis=1)

    return labels, centers


# 测试
np.random.seed(42)
c1 = np.random.randn(30, 2) * 0.5 + [2, 2]
c2 = np.random.randn(30, 2) * 0.5 + [-2, -2]
c3 = np.random.randn(30, 2) * 0.5 + [2, -2]
X = np.vstack([c1, c2, c3])
np.random.shuffle(X)

labels, centers = kmeans(X, k=3)
print("最终中心：")
print(centers)
# 应该看到三个中心大约在 (2, 2)、(-2, -2)、(2, -2) 附近
print(f"每簇点数：{[sum(labels == i) for i in range(3)]}")

# 加分：如果装了 matplotlib，画出来看看
try:
    import matplotlib.pyplot as plt
    colors = ['red', 'blue', 'green']
    for i in range(3):
        plt.scatter(X[labels == i, 0], X[labels == i, 1],
                    c=colors[i], alpha=0.6, label=f'簇 {i}')
    plt.scatter(centers[:, 0], centers[:, 1],
                c='black', marker='x', s=200, linewidths=3, label='中心')
    plt.legend()
    plt.title(f'K-Means (K=3)')
    plt.axis('equal')
    plt.savefig('/tmp/kmeans_demo.png', dpi=150)
    print("图表已保存到 /tmp/kmeans_demo.png")
except ImportError:
    print("(安装 matplotlib 可看到聚类可视化图)")
```
</details>

---

### 练习三：迷你推荐系统（30 分钟）

**任务**：用本文学到的"向量 + 距离"思想，做一个极简的电影推荐系统。

**数据**：5 个用户各给 5 部电影打了分（1-5 分），你需要：

1. 把每个用户表示成一个 5 维向量（他对 5 部电影的评分）
2. 给定一个新用户（只评了 3 部），用"余弦相似度"找最相似的老用户
3. 用相似用户的评分来预测新用户对没评过的电影的评分

**脚手架**：

```python
import numpy as np

# 5 部电影：让子弹飞, 千与千寻, 星际穿越, 泰坦尼克号, 功夫
movies = ["让子弹飞", "千与千寻", "星际穿越", "泰坦尼克号", "功夫"]

# 5 个老用户的评分（1-5 分，0 表示没看过/没评）
ratings = np.array([
    [5, 3, 4, 2, 5],   # 用户 0：喜欢动作和科幻
    [1, 5, 2, 4, 1],   # 用户 1：喜欢动画和爱情
    [4, 1, 5, 1, 3],   # 用户 2：喜欢科幻
    [3, 4, 3, 5, 2],   # 用户 3：喜欢爱情
    [5, 2, 4, 3, 4],   # 用户 4：口味均衡偏动作
], dtype=np.float64)

# 新用户：只看过 3 部（让子弹飞=4, 千与千寻=1, 星际穿越=5）
# 其他两部还没看（用 np.nan 表示）
new_user = np.array([4, 1, 5, np.nan, np.nan], dtype=np.float64)


def cosine_similarity(a, b):
    """
    余弦相似度：两个向量夹角的余弦值
    cos(θ) = (a·b) / (|a| × |b|)
    返回值在 [-1, 1] 之间，1 表示完全相同，-1 表示完全相反
    注意：只比较两个用户都评过分的电影（标记为有效维）
    """
    # TODO: 找出 a 和 b 都有评分的维度
    # 提示: np.isfinite() 检查是否为有效数字（不是 nan 也不是 inf）

    # TODO: 只在这些有效维度上计算余弦相似度

    pass


# 第一步：找到和新用户最像的老用户
# TODO: 对每个老用户计算余弦相似度

# 第二步：用最相似用户的评分 + 相似度加权平均，预测新用户没看过的两部
# TODO: 加权平均预测

print("最相似用户索引：")
print(f"预测新用户对 {movies[3]} 的评价：")
print(f"预测新用户对 {movies[4]} 的评价：")
```

<details>
<summary>点击查看完整答案</summary>

```python
import numpy as np

movies = ["让子弹飞", "千与千寻", "星际穿越", "泰坦尼克号", "功夫"]

ratings = np.array([
    [5, 3, 4, 2, 5],
    [1, 5, 2, 4, 1],
    [4, 1, 5, 1, 3],
    [3, 4, 3, 5, 2],
    [5, 2, 4, 3, 4],
], dtype=np.float64)

new_user = np.array([4, 1, 5, np.nan, np.nan], dtype=np.float64)


def cosine_similarity(a, b):
    # 找出两个用户都评过分的维度（都不是 nan 且都 > 0）
    mask = np.isfinite(a) & np.isfinite(b)
    if mask.sum() == 0:
        return 0.0
    a_valid, b_valid = a[mask], b[mask]
    dot = np.dot(a_valid, b_valid)
    norm_a = np.sqrt(np.dot(a_valid, a_valid))
    norm_b = np.sqrt(np.dot(b_valid, b_valid))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# 第一步：找最相似的用户
similarities = np.array([cosine_similarity(new_user, ratings[i]) for i in range(5)])
most_similar = np.argmax(similarities)
print(f"各用户相似度: {similarities}")
print(f"最相似用户: {most_similar}, 相似度: {similarities[most_similar]:.3f}")

# 第二步：预测新用户没看过的电影
for movie_idx in [3, 4]:  # 泰坦尼克号, 功夫
    # 找出所有评过这部电影的用户（且相似度 > 0）
    valid_users = [i for i in range(5) if ratings[i, movie_idx] > 0]
    if not valid_users:
        print(f"{movies[movie_idx]}: 无可用预测")
        continue

    # 用相似度做加权平均
    weighted_sum = sum(similarities[i] * ratings[i, movie_idx] for i in valid_users)
    weight_sum = sum(abs(similarities[i]) for i in valid_users)
    prediction = weighted_sum / weight_sum if weight_sum > 0 else 0
    print(f"预测新用户对《{movies[movie_idx]}》的评分: {prediction:.2f}")

# 预期：最相似用户可能是用户 2（也喜欢科幻），
# 预测泰坦尼克号不会太高（1-2 分），功夫大概 3-4 分
```
</details>

---

## 调试技巧：出 bug 时按这个顺序排查

当 NumPy 代码跑不通或者结果不对时，按下面这个顺序排查，效率最高：

```
第 1 步：print(X.shape)   ← 形状是你的身份证，八成错误是形状不对
第 2 步：print(X.dtype)   ← 是 float64 还是 int64？int 做除法会截断！
第 3 步：print(np.isnan(X).sum())   ← 有没有 nan（Not a Number）？
第 4 步：print(X.min(), X.max())    ← 数值范围合理吗？
```

**经典 bug 速查表**：

| 症状 | 最可能的原因 | 怎么修 |
|------|-------------|--------|
| 结果全是整数，没有小数 | dtype 是 int，除法被截断 | `arr = arr.astype(np.float64)` |
| `ValueError: operands could not be broadcast together` | 两个数组的形状不兼容 | 打印各自 `.shape`，按"从右往左"规则对齐，缺的用 `np.newaxis` 补 |
| 程序很慢（几秒以上） | 用了 Python for 循环而非向量化 | 用广播或 `np.apply_along_axis` 替代 |
| 结果和预期差很大，但没报错 | 广播配对方向反了 | 在纸上画出最终想要的形状，确认每一维的来源 |
| `nan` 出现在不该出现的地方 | 除以 0 或 0/0 | `np.where(denom != 0, num / denom, 0)` |
| K-Means 结果每次跑都不一样 | 正常现象（初始中心随机），但差异很大说明 K 不合适 | 用"肘部法则"选 K（见下文补充知识） |

---

## 补充知识：怎么选 K？

K-Means 里 K 选几？有个通用的偷懒方法叫**肘部法则**（Elbow Method）：

对每个 K（比如 1 到 10），跑一次 K-Means，算所有点到各自中心的距离平方和（叫 Inertia 或 SSE），画出来——曲线会在某个 K 值突然"拐弯"变平缓，那就是合适的 K。

```python
def elbow_method(X, max_k=10):
    sse = []
    for k in range(1, max_k + 1):
        labels, centers = kmeans(X, k)
        # SSE = 每个点到其所属中心的距离平方总和
        sse.append(sum(np.sum((X[labels == i] - centers[i]) ** 2)
                       for i in range(k)))
    return sse

# sse = elbow_method(X, max_k=10)
# plt.plot(range(1, 11), sse, marker='o')
# "肘部"出现的地方就是合理的 K
```

---

## 学完能做什么 & 下一步

这套基础不是纸上谈兵，它直接撑着这些真实应用：

- **推荐系统**：把你和千万个用户都表示成向量，"和你向量距离近的人喜欢什么，就推荐给你什么"——就是向量 + 距离。
- **照片自动分类 / 客户分群**：相册按人脸聚类、运营商按消费习惯给用户分群，背后都是 K-Means 或其近亲。
- **设备预测性维护 / 气象与销量预测**：工厂传感器、天气、商品销量的预测，全部依赖时间序列的整理和历史特征构造。

继续深入的建议路径（按顺序）：

1. **先把工具用熟**：NumPy 之后学 `pandas`（表格数据）和 `matplotlib`（画图），把本文每个例子都亲手跑一遍、改一改。
2. **补一点数学**：不用啃教材，重点理解"距离""平均值""方差"的直觉即可，需要时再回头看公式。
3. **进入真正的机器学习**：学 `scikit-learn` 库，里面 `KMeans`、`LinearRegression` 都是几行代码的事——你会发现核心思想和本文手算的一模一样。
4. **最后碰深度学习**：当数据变成"一批句子""一批图片"这种三维、四维张量时，本文的形状和广播思维会直接迁移到 PyTorch。

记住这所学校：成绩单是向量，花名册是矩阵，广播体操是向量化，分社团是聚类，看历次月考预测下次是时间序列。把直觉带在身上，公式以后自然会来找你。
