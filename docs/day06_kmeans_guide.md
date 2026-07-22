# Day 06：科学计算与 NumPy 深度复习 - K-Means 聚类快速上手指南

本指南旨在帮助你快速掌握 `Day 06` 练习（[day06_kmeans.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day06_kmeans.py)）所需的所有核心 NumPy 知识点与算法逻辑。

---

## 0. 零基础概念拆解：向量化、线性代数与广播

如果你之前没有接触过 NumPy 的向量化和广播，不用担心！下面用最直观的方式一步步为你拆解。

### 0.1 什么是向量化 (Vectorization)？

* **Python 传统思维（循环扫描）**：
  就像在超市收银台，一件一件把商品从购物车拿出来扫码（`for` 循环）。如果购物车里有 1,000,000 件商品，就会非常慢。
* **NumPy 向量化思维（整块打包）**：
  就像把一整箱商品放到传送带上，由自动化机械臂瞬间完成批量扫码。NumPy 在底层的 C 语言级别实现了对整块内存数据的并行计算，速度比 Python 原生循环快几十倍到上百倍。

---

### 0.2 线性代数基础：欧式距离与 L2 范数 (L2 Norm)

#### (1) 什么是欧式距离？
在平面几何（2D）中，点 $A(x_1, y_1)$ 与点 $B(x_2, y_2)$ 的距离公式大家都很熟悉：
$$d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$

如果扩展到 $D$ 维空间（如包含 $D$ 个特征的数据点）：
$$d(A, B) = \sqrt{(A_1 - B_1)^2 + (A_2 - B_2)^2 + \dots + (A_D - B_D)^2}$$

#### (2) 什么是 L2 范数 (L2 Norm)？
在线性代数中，**一个向量的 L2 范数**指的就是这个向量的“几何长度”（即各元素平方和开根号）。
* 两个向量相减 $\boldsymbol{v} = A - B$ 得到的差值向量。
* $\boldsymbol{v}$ 的 L2 范数 $\|\boldsymbol{v}\|_2$ **正好就是点 $A$ 到点 $B$ 的欧式距离**！

在 NumPy 中计算 L2 范数非常简单：
```python
# 假设 A = np.array([0, 0]), B = np.array([3, 4])
diff = A - B                             # 得到 [-3, -4]
distance = np.linalg.norm(diff)          # 结果为 sqrt((-3)^2 + (-4)^2) = 5.0
```

---

### 0.3 什么是广播机制 (Broadcasting)？

当两个数组（Array）的形状 (Shape) 不完全相同时，NumPy 会在符合规则的情况下，**自动将较小的数组沿着缺少或长度为 1 的维度进行“复制/扩展”**，使其形状与较大数组一致，从而能进行逐元素（element-wise）运算。

#### 广播的对齐规则（从右向左对齐）：
判断两个维度 `Shape A` 和 `Shape B` 能否广播：
从**最右边的维度**开始逐个对比：
* 两个维度相等 $\Rightarrow$ 可以广播；
* 其中一个维度是 `1` $\Rightarrow$ 可以广播（数值 `1` 会自动拉伸复制到与另一个维度一致）；
* 某一数组缺失该维度 $\Rightarrow$ 相当于该维度为 `1`，可以广播。

#### 极简例子：标量与向量相加
```python
a = np.array([1, 2, 3])  # Shape: (3,)
b = 10                   # 标量

# 广播过程：10 被自动拉伸为 [10, 10, 10]
res = a + b              # 结果: [11, 12, 13]
```

---

### 0.4 K-Means 中的 3D 广播原理图解 (核心难点)

在 K-Means 中，我们有：
* `points`: $N$ 个数据点，Shape 为 `(N, D)`
* `centers`: $K$ 个中心点，Shape 为 `(K, D)`

我们要计算**每个点到每个中心点**的距离，结果应该是一个 `(N, K)` 的距离矩阵。

#### 为什么需要升维到 3D (`np.newaxis`)？

* `points[:, np.newaxis, :]` $\Rightarrow$ 形状变为 **`(N, 1, D)`**
* `centers[np.newaxis, :, :]` $\Rightarrow$ 形状变为 **`(1, K, D)`**

现在我们来看广播对齐规则（从右向左）：

| 维度索引 | points 形状 | centers 形状 | 广播对齐结果 | 实际含义 |
| :--- | :--- | :--- | :--- | :--- |
| **第 2 维 (D)** | $D$ | $D$ | $D$ | 特征维度（如 x, y 坐标） |
| **第 1 维 (K)** | **1** | $K$ | **$K$** | 沿聚类中心维度扩展 $K$ 次 |
| **第 0 维 (N)** | $N$ | **1** | **$N$** | 沿数据点维度扩展 $N$ 次 |
| **最终 Shape** | `(N, 1, D)` | `(1, K, D)` | **`(N, K, D)`** | **$N \times K$ 个差值向量** |

#### 具象化数值演练：
假设有 2 个点 ($N=2$)，2 个中心点 ($K=2$)，特征维度为 2 ($D=2$)：
* `points` = `[[0, 0], [3, 4]]`
* `centers` = `[[0, 0], [3, 0]]`

1. **`points[:, np.newaxis, :]` (Shape: 2, 1, 2)**:
   ```text
   [
     [ [0, 0] ],   # 第 0 个点
     [ [3, 4] ]    # 第 1 个点
   ]
   ```
2. **`centers[np.newaxis, :, :]` (Shape: 1, 2, 2)**:
   ```text
   [
     [ [0, 0], [3, 0] ]   # 中心点 0 和 中心点 1
   ]
   ```
3. **两张量相减 `diff = points[:, np.newaxis, :] - centers[np.newaxis, :, :]` (Shape: 2, 2, 2)**:
   ```text
   [
     # 点 0 分别减去 [中心0, 中心1]
     [ [0-0, 0-0],   [0-3, 0-0] ],  -> [ [0, 0], [-3, 0] ]
     
     # 点 1 分别减去 [中心0, 中心1]
     [ [3-0, 4-0],   [3-3, 4-0] ]   -> [ [3, 4], [ 0, 4] ]
   ]
   ```
4. **计算 L2 范数 `np.linalg.norm(diff, axis=2)` (Shape: 2, 2)**:
   沿着 `axis=2`（最内层的坐标差 `[dx, dy]`）计算长度 $\sqrt{dx^2 + dy^2}$：
   * 点 0 到 中心 0 距离：$\sqrt{0^2 + 0^2} = 0$
   * 点 0 到 中心 1 距离：$\sqrt{(-3)^2 + 0^2} = 3$
   * 点 1 到 中心 0 距离：$\sqrt{3^2 + 4^2} = 5$
   * 点 1 到 中心 1 距离：$\sqrt{0^2 + 4^2} = 4$

   输出矩阵 `distances`:
   ```python
   [[0.0, 3.0],
    [5.0, 4.0]]
   ```

---

### 0.5 理解 NumPy 中的 `axis` 参数

很多初学者容易搞混 `axis=0`, `axis=1`, `axis=2`：
* **`axis=0`**：跨行（沿着第 0 维向下）压缩计算。
* **`axis=1`**：跨列（沿着第 1 维向右）压缩计算。
* **`axis=2`**：跨深度/特征维（沿着最内层维度）压缩计算。

例如：
- 在 `distances` 矩阵 `(N, K)` 中，`np.argmin(distances, axis=1)`：沿 `axis=1`（第1维，共 $K$ 个中心）找到最小距离所在的列号，结果 Shape 为 `(N,)`。
- 在 `cluster_points` 矩阵 `(M, D)` 中，`cluster_points.mean(axis=0)`：沿 `axis=0`（第0维，共 $M$ 个点）求均值，求出这 $M$ 个点的中心坐标，结果 Shape 为 `(D,)`。

---

## 1. 核心任务目标

K-Means 是一种最基础且高效的无监督聚类算法。在 Day 06 中，你的核心目标是**使用 NumPy 向量化（Broadcasting）计算**实现一个高效的 K-Means 算法，**不使用 Python 原生循环（如 for/while）来计算点与点之间的距离**。

整个实现包含 4 个核心函数：
1. `compute_distances(points, centers)`: 计算点集到中心点的距离矩阵
2. `assign_clusters(distances)`: 根据距离矩阵分配每个点的类别标签
3. `update_centers(points, labels, k)`: 计算各类别的新中心点
4. `kmeans_fit(points, k, max_iters, tol)`: 串联整体迭代流程直到收敛

---

## 2. 核心代码实现卡片 (Quick Reference)

### 2.1 `compute_distances(points, centers)`
```python
def compute_distances(points: np.ndarray, centers: np.ndarray) -> np.ndarray:
    # 1. 扩维：points (N, 1, D), centers (1, K, D)
    diff = points[:, np.newaxis, :] - centers[np.newaxis, :, :]
    # 2. 沿特征维度 axis=2 计算范数 (欧式距离)
    return np.linalg.norm(diff, axis=2)
```

### 2.2 `assign_clusters(distances)`
```python
def assign_clusters(distances: np.ndarray) -> np.ndarray:
    # 沿 axis=1 (列维度) 找距离最小的中心点索引
    return np.argmin(distances, axis=1)
```

### 2.3 `update_centers(points, labels, k)`
```python
def update_centers(points: np.ndarray, labels: np.ndarray, k: int) -> np.ndarray:
    D = points.shape[1]
    new_centers = np.zeros((k, D))
    for i in range(k):
        pts_in_cluster = points[labels == i]
        if len(pts_in_cluster) > 0:
            new_centers[i] = pts_in_cluster.mean(axis=0)
        else:
            # 防空类边界：若没有点归入该类，维持全 0 或不变更
            new_centers[i] = 0.0
    return new_centers
```

---

## 3. 函数 API 总结对比表

| 函数名 | 输入 Shape | 输出 Shape | 关键 NumPy 方法 |
| :--- | :--- | :--- | :--- |
| `compute_distances` | `points(N, D)`, `centers(K, D)` | `distances(N, K)` | `np.newaxis`, `np.linalg.norm(..., axis=2)` |
| `assign_clusters` | `distances(N, K)` | `labels(N,)` | `np.argmin(distances, axis=1)` |
| `update_centers` | `points(N, D)`, `labels(N,)`, `k` | `new_centers(K, D)` | 布尔掩码 `points[labels == i]`, `mean(axis=0)` |
| `kmeans_fit` | `points(N, D)`, `k` | `(centers, labels)` | `rng.choice`, 循环调用上述三个函数 |

---

## 4. 快速检验你的实现

在完成 [day06_kmeans.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/data_engineering/day06_kmeans.py) 的代码后，你可以运行配套的单元测试来验证正确性：

```bash
.venv/bin/pytest tests/test_day06_kmeans.py
```

祝你练习顺利！如有任何疑问，随时向我提问。
