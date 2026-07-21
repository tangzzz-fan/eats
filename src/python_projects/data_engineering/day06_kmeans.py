import numpy as np  # type: ignore

def compute_distances(points: np.ndarray, centers: np.ndarray) -> np.ndarray:
    """
    Day 6: 科学计算与 NumPy 深度复习 - 计算点集到中心点的距离矩阵
    
    目标：
    使用 NumPy 向量化（Broadcasting）机制，计算 N 个 D 维数据点到 K 个 D 维中心点的欧氏距离。
    不允许使用任何 Python 原生循环（如 for, while）。
    
    提示与关键点：
    1. 输入形状：points 为 (N, D)，centers 为 (K, D)。
    2. 输出形状：(N, K)，第 (i, j) 个元素代表第 i 个点到第 j 个中心点的距离。
    3. 利用广播机制增加轴：
       - points[:, np.newaxis, :] 的形状为 (N, 1, D)
       - centers[np.newaxis, :, :] 的形状为 (1, K, D)
       - 两者相减会广播为 (N, K, D) 的差值张量。
    4. 对差值张量求 L2 范数（`np.linalg.norm(..., axis=2)`）或者计算平方和再开方。
    
    知识体系清单：
    - NumPy 广播机制（Broadcasting）：不同维度数组自动对齐以执行逐元素操作的机制。
    - 向量化数学距离计算：使用 `np.linalg.norm(..., axis=2)` 进行高效的欧氏距离范数求解。
    - K-means 聚类收敛迭代优化：利用坐标中心点均值漂移逼近聚类极限。
    
    工程实践避坑指南：
    - 广播计算引发内存溢出 (OOM)：如果样本数 N 和聚类中心 K 极大，广播扩展产生的中间矩阵 (N, K, D) 占用空间巨大。应当注意限制 Batch 或利用快速计算库（如 Scipy KDTree 或 PyTorch 的分布式计算）。
    - 均值除以零产生空聚类 NaN：如果某次迭代中，第 j 个中心点没有分配到任何数据样本点，那么在更新该类别的中心位置时会因分子除以分母 0 导致数值转化为 NaN，造成迭代崩溃。更新时务必对空聚类加上前置判断限制。
    
    :param points: 输入点集，形状为 (N, D)
    :param centers: 中心点集，形状为 (K, D)
    :return: 距离矩阵，形状为 (N, K)
    """
    # TODO: 使用广播机制一步完成距离矩阵计算，不要使用 for 循环
    raise NotImplementedError("Please implement compute_distances using numpy broadcasting")


def assign_clusters(distances: np.ndarray) -> np.ndarray:
    """
    基于距离矩阵，将点分配给最近的中心点。
    
    提示与关键点：
    1. 输入为 (N, K) 的距离矩阵。
    2. 对每一行（对应每个点），找出距离最小值的索引（0 到 K-1）。
    3. 使用 `np.argmin(..., axis=1)` 操作。
    
    :param distances: 距离矩阵，形状为 (N, K)
    :return: 聚类标签，形状为 (N,)，类型为整数
    """
    # TODO: 找出每一行最小值的索引并返回
    raise NotImplementedError("Please implement assign_clusters")


def update_centers(points: np.ndarray, labels: np.ndarray, k: int) -> np.ndarray:
    """
    更新中心点位置为各自聚类内所有点的均值。
    
    提示与关键点：
    1. 遍历中心点索引 0 到 k-1。对于每一个类，筛选出对应标签的所有点。
    2. 计算这些点的均值（axis=0）。
    3. 如果某个聚类下没有任何点，为防止 NaN，可保持原先值或设为随机点（此处如果为空类，可直接设为全 0）。
    
    :param points: 数据点集，形状为 (N, D)
    :param labels: 聚类标签，形状为 (N,)
    :param k: 聚类数量
    :return: 更新后的中心点集，形状为 (K, D)
    """
    # TODO: 计算每个聚类中所有点的均值作为新的中心点
    raise NotImplementedError("Please implement update_centers")


def kmeans_fit(points: np.ndarray, k: int, max_iters: int = 100, tol: float = 1e-4) -> tuple[np.ndarray, np.ndarray]:
    """
    手写 K-means 聚类算法主体流程。
    
    算法步骤：
    1. 随机初始化中心点：从 points 中随机无重复选取 k 个点作为初始中心。
    2. 迭代直至收敛或达到最大迭代次数：
       a. 计算距离矩阵 compute_distances。
       b. 划分聚类标签 assign_clusters。
       c. 保存旧的中心点，计算新中心点 update_centers。
       d. 判断中心点漂移距离是否小于阈值 tol（如果旧中心和新中心的绝对误差均值小于 tol，则提前终止迭代）。
    
    :param points: 数据点集，形状为 (N, D)
    :param k: 聚类簇数
    :param max_iters: 最大迭代次数
    :param tol: 收敛终止阈值
    :return: 元组 (最终中心点集 (K, D), 聚类标签 (N,))
    """
    # 随机种子设定以确保测试可复现
    rng = np.random.default_rng(42)
    n_samples = points.shape[0]
    if n_samples < k:
        raise ValueError("Number of samples must be greater than or equal to k.")
        
    # 1. 随机选取 k 个中心点
    indices = rng.choice(n_samples, size=k, replace=False)
    centers = points[indices].copy()
    
    labels = np.zeros(n_samples, dtype=int)
    
    # TODO: 实现 K-means 迭代收敛循环
    # 提示：在循环中调用 compute_distances, assign_clusters, update_centers，并检查是否收敛。
    raise NotImplementedError("Please implement kmeans_fit loop")
