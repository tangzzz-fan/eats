import math
import numpy as np  # type: ignore
from typing import List, Tuple, Dict
from python_projects.simulation.day12_kinematics import Robot2D
from python_projects.simulation.day12_controller import PIDController

def generate_circular_path(radius: float = 5.0, num_points: int = 100) -> np.ndarray:
    """
    生成一个圆形轨迹用于机器人追踪。
    返回形状为 (num_points, 2) 的 NumPy 数组，保存 [x, y] 坐标点集。
    """
    angles = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return np.stack([x, y], axis=1)


def run_simulation_loop(path: np.ndarray, 
                        kp: float, 
                        ki: float, 
                        kd: float, 
                        target_speed: float = 1.0, 
                        dt: float = 0.1, 
                        total_time: float = 10.0) -> Dict[str, List[float]]:
    """
    Day 12: 具身智能仿真 - 闭环轨迹追踪主仿真循环
    
    目标：
    在给定的目标路径点集（path）上，运行闭环仿真，使机器人依靠 PID 控制器追踪该路径。
    
    追踪算法说明：
    1. 寻找路径上距离机器人当前位置最近的点作为当前追踪目标点。
    2. 计算目标朝向角：`target_theta = atan2(target_y - robot.y, target_x - robot.x)`。
    3. 计算航向误差（Heading Error）：`heading_error = target_theta - robot.theta`。
       注意航向误差需要归一化到 [-pi, pi] 之间，防止多旋转 360 度。
       归一化公式：`heading_error = atan2(sin(heading_error), cos(heading_error))`。
    4. 将航向误差送入 PID 控制器中，计算输出的转向角速度 omega。
    5. 设置机器人的线速度 v 为恒定的 target_speed（若接近终点则设为 0）。
    6. 使用 `robot.update(v, omega, dt)` 更新小车状态。
    7. 记录每个时间步长的 [time, x, y, theta, error_val]。
    
    :param path: 二维目标路径点矩阵，形状为 (M, 2)
    :param kp: PID 比例系数
    :param ki: PID 积分系数
    :param kd: PID 微分系数
    :param target_speed: 设定的小车线速度
    :param dt: 仿真步长
    :param total_time: 仿真运行总时间
    :return: 包含各类仿真记录数据的字典
    """
    steps = int(total_time / dt)
    robot = Robot2D(x=path[0, 0], y=path[0, 1] + 1.0, theta=0.0) # 故意添加 1m 的初始偏差以观察收敛情况
    steering_pid = PIDController(kp, ki, kd)
    
    history: Dict[str, List[float]] = {
        "time": [],
        "x": [],
        "y": [],
        "theta": [],
        "tracking_error": []
    }
    
    # TODO: 补全闭环仿真计算主循环，按时间步长向前推进
    # 1. 遍历 steps 步数
    # 2. 计算当前位置与路径上所有点之间的距离，选取距离最近的点的索引
    # 3. 计算航向角误差 heading_error 并做 [-pi, pi] 范围规整
    # 4. 调用 steering_pid.update 计算得到角速度 omega
    # 5. 调用 robot.update 更新小车状态，并写入历史字典
    raise NotImplementedError("Please implement run_simulation_loop")
