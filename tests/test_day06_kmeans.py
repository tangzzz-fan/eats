import pytest
import numpy as np  # type: ignore
from python_projects.data_engineering.day06_kmeans import (
    compute_distances,
    assign_clusters,
    update_centers,
    kmeans_fit
)

def test_compute_distances():
    points = np.array([[0.0, 0.0], [3.0, 4.0]])
    centers = np.array([[0.0, 0.0], [3.0, 0.0]])
    try:
        dist = compute_distances(points, centers)
        # 点0(0,0)到中心0(0,0)距离是0，到中心1(3,0)距离是3
        # 点1(3,4)到中心0(0,0)距离是5，到中心1(3,0)距离是4
        expected = np.array([[0.0, 3.0], [5.0, 4.0]])
        assert np.allclose(dist, expected)
    except NotImplementedError:
        pytest.skip("compute_distances is not implemented yet.")

def test_assign_clusters():
    distances = np.array([[1.0, 5.0], [10.0, 2.0]])
    try:
        labels = assign_clusters(distances)
        assert np.array_equal(labels, [0, 1])
    except NotImplementedError:
        pytest.skip("assign_clusters is not implemented yet.")

def test_update_centers():
    points = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    labels = np.array([0, 0, 1])
    try:
        new_centers = update_centers(points, labels, k=2)
        # 聚类0的中心点是 (1+3)/2=2, (2+4)/2=3 -> [2.0, 3.0]
        # 聚类1的中心点是 [5.0, 6.0]
        expected = np.array([[2.0, 3.0], [5.0, 6.0]])
        assert np.allclose(new_centers, expected)
    except NotImplementedError:
        pytest.skip("update_centers is not implemented yet.")

def test_kmeans_fit():
    # 测试数据点
    points = np.array([
        [1.0, 1.0], [1.5, 1.0],
        [10.0, 10.0], [10.5, 10.0]
    ])
    try:
        centers, labels = kmeans_fit(points, k=2, max_iters=10)
        assert centers.shape == (2, 2)
        assert labels.shape == (4,)
        # 同一簇的点应该被归入同一类
        assert labels[0] == labels[1]
        assert labels[2] == labels[3]
        assert labels[0] != labels[2]
        
        # 验证聚类中心数值收敛，排序以应对随机初始化顺序
        sorted_centers = centers[np.argsort(centers[:, 0])]
        expected_centers = np.array([[1.25, 1.0], [10.25, 10.0]])
        assert np.allclose(sorted_centers, expected_centers, atol=1e-3)
    except NotImplementedError:
        pytest.skip("kmeans_fit loop is not implemented yet.")
