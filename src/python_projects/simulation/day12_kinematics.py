import math
from typing import Tuple

class Robot2D:
    """
    Day 12: 具身智能仿真 - 2D 差速移动机器人运动学模型
    
    目标：
    实现机器人运动学模拟器的状态更新（数值积分）。
    
    机器人位姿表示为 (x, y, theta)：
    - x, y: 机器人在二维世界坐标系中的平面位置（米）
    - theta: 机器人的朝向偏航角（Yaw，弧度值）
    
    更新公式（欧拉一阶积分）：
    x_new = x + v * cos(theta) * dt
    y_new = y + v * sin(theta) * dt
    theta_new = theta + omega * dt
    
    其中：
    - v: 线速度 (Linear velocity, m/s)
    - omega: 角速度 (Angular velocity, rad/s)
    - dt: 时间步长（秒）
    
    知识体系清单：
    - 移动机器人非线性运动学：差速驱动小车的运动学非线性状态空间模型。
    - 欧拉数值积分：微分方程离散化与状态递推估计（Euler integration）。
    - 经典反馈控制理论：PID 控制器三项（P项响应当前，I项消除静差，D项平抑震荡）在角度/速度跟踪中的应用。
    - 周期角度归一化：航向误差使用 atan2 映射到主值区间 [-pi, pi] 的数学方法。
    
    工程实践避坑指南：
    - 航向角相减导致的调头震荡：在计算方向控制时，若直接使用减法获取角度偏差，在边界突变（例如机器人朝向 -179 度，目标方向 179 度）时会计算出接近 360 度的巨幅角度误差，导致小车原地猛转圈。必须通过 `math.atan2(math.sin(diff), math.cos(diff))` 归一化角差。
    - 积分饱和与积分防跑飞 (Windup)：在闭环追踪中，如果小车距离目标很远或者长期无法消除残余静差，PID 控制器的积分项 `self.integral` 会无限增大，导致接近目标点时产生巨大的超调与严重抖动。必须在积分更新步骤增加 Anti-windup 积分幅值裁剪限制。
    """
    def __init__(self, x: float = 0.0, y: float = 0.0, theta: float = 0.0):
        self.x = x
        self.y = y
        self.theta = theta

    def update(self, v: float, omega: float, dt: float) -> Tuple[float, float, float]:
        """
        基于速度控制量更新机器人位姿状态。
        
        :param v: 线速度 (m/s)
        :param omega: 角速度 (rad/s)
        :param dt: 运行时间间隔，必须大于 0
        :return: 更新后的位姿元组 (x, y, theta)
        """
        if dt <= 0:
            raise ValueError("dt must be positive.")
            
        # TODO: 编写机器人的欧拉积分状态更新并返回新位姿
        # 提示：使用 math.cos(self.theta) 和 math.sin(self.theta)
        raise NotImplementedError("Please implement Robot2D.update")

    @property
    def pose(self) -> Tuple[float, float, float]:
        """
        返回机器人当前的位姿。
        """
        return self.x, self.y, self.theta
