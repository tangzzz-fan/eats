import pytest
import numpy as np  # type: ignore
import math
from python_projects.simulation.day12_kinematics import Robot2D
from python_projects.simulation.day12_controller import PIDController
from python_projects.simulation.day12_sim_loop import run_simulation_loop, generate_circular_path

def test_robot2d_kinematics():
    robot = Robot2D(x=0.0, y=0.0, theta=0.0)
    try:
        x, y, theta = robot.update(v=1.0, omega=0.0, dt=1.0)
        assert math.isclose(x, 1.0, abs_tol=1e-6)
        assert math.isclose(y, 0.0, abs_tol=1e-6)
        assert math.isclose(theta, 0.0, abs_tol=1e-6)
        
        # 旋转 90 度然后前进
        robot2 = Robot2D(x=0.0, y=0.0, theta=math.pi / 2)
        x2, y2, theta2 = robot2.update(v=2.0, omega=0.1, dt=1.0)
        assert math.isclose(x2, 0.0, abs_tol=1e-6)
        assert math.isclose(y2, 2.0, abs_tol=1e-6)
        assert math.isclose(theta2, math.pi / 2 + 0.1, abs_tol=1e-6)
    except NotImplementedError:
        pytest.skip("Robot2D kinematics update is not implemented yet.")

def test_pid_controller():
    pid = PIDController(kp=1.0, ki=0.2, kd=0.05)
    try:
        out = pid.update(setpoint=5.0, feedback=4.0, dt=0.5)
        # error = 1.0
        # P = 1.0 * 1.0 = 1.0
        # I = 0.2 * (0 + 1.0 * 0.5) = 0.1
        # D = 0.05 * (1.0 - 0.0) / 0.5 = 0.1
        # output = 1.0 + 0.1 + 0.1 = 1.2
        assert math.isclose(out, 1.2, abs_tol=1e-6)
    except NotImplementedError:
        pytest.skip("PIDController update is not implemented yet.")

def test_simulation_loop():
    path = generate_circular_path(radius=5.0, num_points=20)
    try:
        history = run_simulation_loop(path, kp=1.0, ki=0.1, kd=0.01, total_time=1.0, dt=0.2)
        assert "time" in history
        assert "x" in history
        assert "tracking_error" in history
        assert len(history["time"]) == 5
    except NotImplementedError:
        pytest.skip("run_simulation_loop is not implemented yet.")
