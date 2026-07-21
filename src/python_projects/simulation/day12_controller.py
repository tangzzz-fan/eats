class PIDController:
    """
    Day 12: 具身智能仿真 - 反馈 PID 控制器
    
    目标：
    实现机器人轨迹控制中的 PID 反馈环，根据目标（setpoint）与实际反馈（feedback）计算速度或转向角控制指令。
    
    公式：
    Error = Setpoint - Feedback
    P = Kp * Error
    I = Ki * (Integral + Error * dt)
    D = Kd * (Error - Prev_Error) / dt
    Output = P + I + D
    """
    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, setpoint: float, feedback: float, dt: float) -> float:
        """
        更新并计算 PID 输出值。
        
        :param setpoint: 目标追踪位置值
        :param feedback: 当前状态反馈值
        :param dt: 运行时间周期（必须大于 0）
        :return: 控制输出控制量
        """
        if dt <= 0.0:
            raise ValueError("dt must be positive.")
            
        # TODO: 编写 PID 控制器计算式
        # 提示：计算当前误差 error，更新 self.integral，计算微分项，保存 self.prev_error 并输出 P+I+D。
        # 进阶优化：可以在积分更新累加时，对 self.integral 加上限制截断（例如限制在某个最大值范围如 [-10.0, 10.0] 内），以防止积分饱和（Anti-windup）。
        raise NotImplementedError("Please implement PIDController.update")

    def reset(self) -> None:
        """
        重置 PID 的积分和历史误差。
        """
        self.prev_error = 0.0
        self.integral = 0.0
