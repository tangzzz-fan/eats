# 机器人仿真与PID控制：写给高中生的入门指南

你有没有想过，扫地机器人是怎么做到不撞墙、不漏扫的？外卖配送小车又是怎么稳稳停在酒店门口的？这背后有一个共同的领域：**机器人仿真与PID控制**。它要回答两个问题——"怎么在电脑里先造一个假的机器人来练手"（仿真），以及"怎么让机器人又快又稳地到达目标"（控制）。

这篇文章我们用一个贯穿始终的比喻：**学骑自行车**。你第一次骑车时，没人给你讲公式，你就是上去骑，眼睛看目标，身体不断调整方向，摔几次就会了。机器人仿真，就是给机器人一个"摔了也不疼"的练习场；PID控制，就是机器人骑车时那套"看差距、做调整"的本能。

---

## 先建立直觉

想象你蒙着眼睛，要把一辆玩具车从客厅这头推到沙发前面停下。你会怎么做？

你大概会这样：偷偷看一眼，发现离沙发还挺远，就用力推一把；再看一眼，近了，就轻轻推；快到的时候，你甚至会提前收手，因为你知道车会惯性前滑。

这个"看一眼 → 算差距 → 调整用力 → 再看一眼"的循环，就是**反馈控制**——整个机器人控制的灵魂。

但这里有两个现实问题：

1. **真实机器人很贵、很脆。** 一个底盘几万块，你调试的时候让它撞墙十次，老板会哭。所以工程师先在电脑里写一个"假机器人"——用代码算出它每一刻在哪里、朝哪个方向。这就是**仿真**：在数字世界里随便撞、随便试，一分钱不花。
2. **"调整用力"这件事要写成代码。** 你手上的感觉是本能，机器人没有本能，它需要一个明确的规则：差多少，就出多大力。这个规则最经典的一种，就是 **PID 控制器**（三个英文单词 Proportional、Integral、Derivative 的缩写，别急，后面逐个讲）。

所以这个领域一句话概括：**先在电脑里造一个遵守物理规律的虚拟机器人，再用反馈控制的规则教它准确到达目标。**

---

## 知识地图

整个方向的核心知识点就下面 6 个，先把全局装进脑子：

| 知识点 | 一句话概括 |
| --- | --- |
| 为什么要仿真 | 真机器人调试又贵又危险，电脑里的"假机器人"随便试错 |
| 状态与运动学 | 用三个数 `(x, y, θ)` 说清小车"在哪、朝哪"，用速度指令让它动 |
| 数值积分（欧拉法） | 把连续运动切成一小步一小步，每步按"速度 × 时间"挪一点 |
| 反馈控制与PID三项 | 看误差调力度：P管现在、I管历史、D管未来 |
| 角度环绕 | 179° 和 -179° 只差 2°，直接相减会算出 358°，小车当场发疯 |
| 积分饱和与调参 | 积分项会"记仇"记过头，必须限幅；三个系数靠直觉和套路调 |

---

## 重点逐个讲

### 一、为什么要仿真：给机器人一个"摔了不疼"的练习场

**生活比喻**：飞行员上天之前，要先在飞行模拟器里练几百个小时。模拟器里坠机一百次，真人一根汗毛都不会少。

**直觉解释**：机器人控制算法是人写的，人写的代码一定有错。如果直接在真车上试，一个符号写反，小车就全速撞墙。仿真器做的事很简单：用代码记住小车"现在在哪"，每次收到速度指令，就按物理规律算出"下一步在哪"。把这个过程循环几百次，小车的整个行驶轨迹就出来了——全程没有一个真实零件。

**最小例子**：下面这段代码就是一个世界上最简陋的"仿真器"——一个小车每秒往前挪 0.5 米，模拟 4 秒：

```python
x = 0.0      # 小车初始位置（米）
v = 0.5      # 小车速度（米/秒）
dt = 1.0     # 每一步代表 1 秒

for step in range(4):
    x = x + v * dt           # 新位置 = 旧位置 + 速度 × 时间
    print(f"第{step+1}秒末，小车在 x = {x:.1f} 米")
```

运行它，你会看到小车依次出现在 0.5、1.0、1.5、2.0 米——你刚刚"仿真"了一次行驶过程，没花一分钱，也没撞坏任何东西。真正的仿真器只是把这个思想做得更精细（每一步更短、还考虑转向）。

一个像样的机器人仿真器通常包含三块东西：

- **世界模型**：地面、墙壁、障碍物在哪里。
- **机器人模型**：就是我们上面写的"状态 + 运动规则"，有的还会模拟轮子打滑、电机延迟。
- **传感器模型**：假装机器人有摄像头、雷达，按照世界模型算出它"应该看到什么"。

有了这三块，你的控制代码根本分不清自己在开真车还是假车——这正是仿真最大的价值：**同一套代码，仿真里调好，直接搬上真车。**

**一句话总结**：仿真就是用代码按物理规律推算机器人轨迹，让算法在零成本、零风险的环境里反复试错。

---

### 二、状态与运动学：用三个数说清"小车在哪、朝哪"

**生活比喻**：跟朋友约饭，你说"我在商场东门，面朝北"。两个信息缺一不可——只说位置，朋友不知道你朝向；只说朝向，朋友不知道你在哪。

**直觉解释**：在平面地面上跑的小车，它的**状态**（State，指描述物体当前处境的一组数字）只需要三个数：

- `x`、`y`：小车在平面上的位置坐标（单位：米）。
- `θ`（读作 theta）：车头朝向的角度（单位：弧度。弧度是另一种量角度的单位，π 弧度 = 180°）。

而控制小车动起来，也只需要两个指令：**线速度 `v`**（前进多快）和**角速度 `ω`**（读作 omega，转向多快），就像电动车的油门和车把。给定当前状态和运动指令，推算下一刻状态的规则，就叫**运动学**（Kinematics）。

**最小例子**：用 Python 字典表示小车状态，一目了然：

```python
import math

car = {"x": 0.0, "y": 0.0, "theta": math.pi / 2}  # 在原点，车头朝正北
v, omega = 1.0, 0.0   # 直行 1 米/秒，不转向

print(f"位置: ({car['x']}, {car['y']}), 朝向: {math.degrees(car['theta'])} 度")
```

**一句话总结**：平面小车的全部状态就是 `(x, y, θ)` 三个数；运动学就是"给速度指令，算新状态"的规则。

---

### 三、数值积分（欧拉法）：把运动切成无数小碎步

**生活比喻**：你没法"瞬移"到学校，但你可以走一步、再走一步。每一步都朝着当前方向迈固定距离，几千步之后你自然就到了。步子越小，走得越贴近你想走的曲线。

**直觉解释**：真实世界里运动是连续的，但计算机只会一步一算。于是我们做个近似：假设在每一小步 `dt`（比如 0.05 秒）内，小车方向和速度都不变，沿直线挪一小段：

- 新朝向 = 旧朝向 + 角速度 × `dt`
- 新位置 = 旧位置 + 速度沿车头方向的分量 × `dt`

这个方法叫**欧拉法**（Euler Integration，积分在这里就是"一小段一小段累加出总位移"的意思）。它的代价是：转弯时真实轨迹是弧线，欧拉法每步走的是直线，所以 `dt` 取得越大，轨迹偏差越明显；取小一点（比如 0.05 秒）就足够逼真。

**最小例子**：小车边前进边左转，用欧拉法模拟 3 步：

```python
import math

x, y, theta = 0.0, 0.0, 0.0   # 原点出发，车头朝东
v, omega, dt = 1.0, 0.5, 0.1  # 前进 1 m/s，转向 0.5 rad/s，步长 0.1 秒

for i in range(3):
    x += v * math.cos(theta) * dt   # 沿车头方向分解出 x 方向的位移
    y += v * math.sin(theta) * dt   # 沿车头方向分解出 y 方向的位移
    theta += omega * dt             # 车头转一点
    print(f"位置 ({x:.3f}, {y:.3f}), 朝向 {math.degrees(theta):.1f} 度")
```

你会看到 `y` 越来越大——小车正在画出一条向左弯的弧线（尽管每一步走的是直线）。

**一句话总结**：欧拉法就是"每小步假设匀速直走，逐步累加"，步长越小越接近真实运动。

---

### 四、反馈控制与PID三项：看差距、算总账、提前刹车

**生活比喻**：你骑共享单车去一个路口。离路口远，你使劲蹬（**P：差距大，力气大**）；路口有段上坡，你感觉"光靠现在的劲儿过不去"，于是持续额外多蹬几脚（**I：积累过去的不足，补上欠账**）；快到路口你提前捏闸，免得冲过停止线（**D：看到逼近速度太快，提前减速**）。

**直觉解释**：PID 控制器每一拍都做同一件事：算出**误差**（目标 − 当前值），然后把三种"反应"加起来作为输出力度：

- **P（比例项，Proportional）**：误差越大，输出越大。最本能的反应，但它有个毛病——离目标很近时误差很小，输出小到推不动小车（比如地面有摩擦），小车会永远停在目标前一点点，这个剩下的差距叫**静差**。
- **I（积分项，Integral）**：把历史上的误差累加起来。静差一直存在，累加值就越来越大，直到足够把小车"推过终点线"，专治静差。
- **D（微分项，Derivative）**：看误差变化得多快。误差在飞速缩小，说明小车正在猛冲，D 就施加反向力提前刹车，防止冲过头来回震荡。

**最小例子**：只用 P 项控制小车靠近 10 米处的目标，每步打印位置：

```python
target, x = 10.0, 0.0
Kp, dt = 0.5, 0.5   # P 系数 0.5，每步 0.5 秒

for i in range(8):
    error = target - x      # 算误差
    v = Kp * error          # P 控制：误差大就跑得快
    x += v * dt
    print(f"位置 {x:.2f} 米, 误差 {error:.2f} 米")
```

你会看到误差一路缩小：10 → 5 → 2.5 → ……这就是 P 控制的典型样子——快，但越到后面越"温柔"，如果有摩擦拦着，最后那点距离就永远走不完（这时就该 I 出场了）。

**一句话总结**：P 响应当前差距、I 补偿历史欠账、D 根据逼近速度提前刹车，三者相加就是 PID。

---

### 五、角度环绕：179° 和 -179° 之间只隔一层窗户纸

**生活比喻**：钟表上 11 点 59 分和 12 点 01 分只差 2 分钟，但如果你用"12:01 − 11:59"硬算，会得出"差 11 小时 58 分钟"——角度也是圆的，也会踩同一个坑。

**直觉解释**：机器人里角度范围通常是 -180° 到 +180°。假设车头朝 -179°，目标朝 +179°，物理上只要顺时针转 2° 就到。但直接相减：`179 - (-179) = 358°`。PID 一看误差 358°，以为差了大半圈，指挥小车疯狂转一整圈——实际表现就是原地抽搐甩头。

解决办法是把角度差**归一化**（统一折算到 -180° ~ +180° 这个区间），把多算的整圈数扔掉。工程上惯用的写法是 `atan2(sin(差), cos(差))`，你暂时不用懂原理，记住效果：`358°` 进去，`-2°` 出来。

**最小例子**：

```python
import math

def angle_error(target, current):
    diff = target - current
    # 归一化到 [-180°, 180°]，自动选择最短的转向方向
    return math.degrees(math.atan2(math.sin(diff), math.cos(diff)))

t = math.radians(179)    # 目标朝向 +179°
c = math.radians(-179)   # 当前朝向 -179°
print(f"错误算法: {179 - (-179)} 度")          # 358 度，小车会猛转一圈
print(f"正确算法: {angle_error(t, c):.1f} 度")  # -2.0 度，轻轻一转就到
```

**一句话总结**：角度是圆的，误差必须先归一化再相减，否则 2° 的转身会被算成 358° 的暴走。

---

### 六、积分饱和与调参直觉：别让"记仇"的积分毁了到达

**生活比喻**：你攒了一肚子火跑步去找人理论，跑到对方面前时火气太大收不住，直接撞进了人家怀里。积分项就是这样：跑向目标的漫漫长路上它一直在"攒火"，到达时火还没消，小车就冲过头了。

**直觉解释**：这就是**积分饱和**（Integral Windup）：目标很远时，误差长时间很大，`integral += error * dt` 每一拍都在猛加，攒成一个天文数字。等小车到了目标点，当前误差已经是 0，可巨大的积分存量还在输出推力，小车根本停不下来。解决办法很朴素——给积分**限幅**（Clamp），攒到上限就不许再攒：

```python
error, dt = 5.0, 0.05   # 举例：误差停在 5，每拍 0.05 秒
integral = 0.0          # 积分器从零开始攒

for i in range(100):
    integral += error * dt
    integral = max(-1.0, min(integral, 1.0))   # 限幅：最多攒到 ±1

print(f"攒了 100 拍，积分被钳在: {integral}")   # 若不限幅，此时已攒到 25.0
```

运行结果：不管误差持续多久，积分都被钳在 1.0，小车到达后最多被这个"小尾巴"推一下，而不会带着 25.0 的巨额推力飞出去。

至于**调参**（给 Kp、Ki、Kd 三个系数找合适的数值），公认的上手套路是：

1. 先把 Ki、Kd 设为 0，只调 Kp：从小往大加，加到小车能比较快接近目标、但开始有点来回晃。
2. 加一点 Kd 把晃动压下去（就像给弹簧床加阻尼）。
3. 如果发现总停在目标前一点点（静差），再加一点点 Ki——Ki 通常是三者里最小的。

**一句话总结**：积分要限幅防冲过头；调参顺序是"先 P 后 D 最后补一点 I"。

---

## 难点与易踩的坑

**1. 觉得 `dt` 无所谓，随手设成 1 秒。** 欧拉法每一步都假设"这步内方向不变"，步长越大，转弯时走的直线和弦与真实弧线差得越远，仿真轨迹会明显失真，你在仿真里调好的参数到真车上全错。正确理解：仿真步长要远小于运动变化的快慢，工程上常用 0.01 ~ 0.05 秒。

**2. 以为 P 越大越好。** Kp 太小，小车慢吞吞；Kp 太大，小车在目标两边来回猛冲（震荡），甚至越晃越厉害彻底失控。正确理解：P 给的是"冲劲"，冲劲必须和 D 的"刹车"配合，单独猛加 P 必翻车。

**3. 角度直接相减。** 这是机器人新手几乎必踩一次的坑：代码在大部分角度下都正常，偏偏小车转到 ±180° 分界线附近时突然疯狂甩头，查半天查不出。正确理解：只要涉及角度差，永远先归一化到 [-π, π]，形成肌肉记忆。

**4. 忘记积分有记忆，换目标了还带着旧账。** 积分项累加的是"历史"，如果你中途给小车换了一个新目标，旧的积分存量会干扰新任务，甚至带着巨大的旧值直接冲出去。正确理解：切换任务或误差符号翻转时，往往要清零或限幅积分。

**5. 在噪声大的传感器上猛加 D。** D 项看的是误差的"变化率"，而传感器噪声（读数的随机抖动）会让变化率剧烈跳动，D 会把这些抖动放大成乱抖的输出。正确理解：D 能平抑震荡，但它怕脏数据，实际工程里常要对误差信号先做平滑。

---

## 实战练习：从仿真到控制的一条龙

### 练习一：完整的 2D 小车仿真器（30 分钟）

**任务**：写一个 `Robot2D` 类和一个 `Simulator` 类，让小车能按照速度指令在平面上运动。

**要求**：
- `Robot2D` 存状态 `(x, y, theta)`，提供 `step(v, omega, dt)` 方法
- `Simulator` 存小车对象和时间参数，提供 `run(controller, duration)` 方法——每一拍调一次 controller，拿到速度指令，驱动小车
- Controller 是一个函数，输入当前状态和目标，返回 `(v, omega)`

```python
import math

class Robot2D:
    """2D 差速驱动机器人"""
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta

    @property
    def state(self):
        return (self.x, self.y, self.theta)

    def step(self, v, omega, dt):
        """用欧拉法更新一步"""
        # TODO: 实现运动学更新
        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt
        self.theta += omega * dt


class Simulator:
    def __init__(self, robot, dt=0.05):
        self.robot = robot
        self.dt = dt
        self.history = []  # 记录轨迹 [(t, x, y, theta), ...]

    def run(self, controller, target, duration):
        """运行仿真 duration 秒，每 dt 秒调一次 controller"""
        steps = int(duration / self.dt)
        for i in range(steps):
            t = i * self.dt

            # TODO: 调用 controller，传入当前状态和 target，得到 (v, omega)
            v, omega = controller(self.robot, target, self.dt)

            # TODO: 记录当前状态
            self.history.append((t, self.robot.x, self.robot.y, self.robot.theta))

            # TODO: 驱动小车走一步
            self.robot.step(v, omega, self.dt)

        return self.history
```

**测试**：写一个"原地转圈"的 controller，让小车以固定角速度转一圈，画出来应该是一个点或者一个小圆。

<details>
<summary>点击查看 Robot2D + Simulator 实现</summary>

```python
import math

class Robot2D:
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta

    @property
    def state(self):
        return (self.x, self.y, self.theta)

    def step(self, v, omega, dt):
        self.x += v * math.cos(self.theta) * dt
        self.y += v * math.sin(self.theta) * dt
        self.theta += omega * dt


class Simulator:
    def __init__(self, robot, dt=0.05):
        self.robot = robot
        self.dt = dt
        self.history = []

    def run(self, controller, target, duration):
        steps = int(duration / self.dt)
        for i in range(steps):
            t = i * self.dt
            v, omega = controller(self.robot, target, self.dt)
            self.history.append((t, self.robot.x, self.robot.y, self.robot.theta))
            self.robot.step(v, omega, self.dt)
        return self.history


# 测试：原地转圈
def spin_controller(robot, target, dt):
    return (0.0, 1.0)  # 不前进，纯转向

robot = Robot2D()
sim = Simulator(robot, dt=0.05)
history = sim.run(spin_controller, target=None, duration=6.28)  # 约转一圈

# 可视化轨迹
try:
    import matplotlib.pyplot as plt
    xs, ys = [h[1] for h in history], [h[2] for h in history]
    plt.plot(xs, ys, 'b.-', markersize=2)
    plt.axis('equal')
    plt.title("纯转向：小车原地转圈（应该几乎是一个点）")
    plt.show()
except ImportError:
    print("(安装 matplotlib 可看到轨迹图)")
```
</details>

---

### 练习二：PID 控制器（20 分钟）

**任务**：实现完整的 PID 控制器，包含三项 + 积分限幅 + 角度归一化。

```python
import math

class PIDController:
    def __init__(self, Kp, Ki, Kd, integral_max=1.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral_max = integral_max
        self.prev_error = 0.0
        self.integral = 0.0

    def reset(self):
        """切换目标时调用，清空积分"""
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, error, dt):
        """给定当前误差和 dt，返回控制量"""
        # TODO 1: P 项 = Kp × error

        # TODO 2: I 项 = 累加 error × dt，然后限幅

        # TODO 3: D 项 = Kd × (error - prev_error) / dt

        # TODO 4: 保存 prev_error 供下一拍使用

        pass  # 返回 p + i + d


class RobotPIDController:
    """完整的 2D 小车 PID 控制器——分别控制速度和转向"""
    def __init__(self, Kp_dist, Ki_dist, Kd_dist,
                 Kp_angle, Ki_angle, Kd_angle):
        self.dist_pid = PIDController(Kp_dist, Ki_dist, Kd_dist)
        self.angle_pid = PIDController(Kp_angle, Ki_angle, Kd_angle)

    def __call__(self, robot, target, dt):
        """target = (target_x, target_y)"""
        tx, ty = target

        # TODO: 算距离误差（到目标的直线距离）
        # dist_error = ...

        # TODO: 算角度误差（车头朝向 vs 目标方向）
        # 目标方向 = atan2(ty - robot.y, tx - robot.x)
        # 角度误差 = 目标方向 - robot.theta，然后归一化到 [-pi, pi]
        # des_theta = ...
        # angle_error = ...

        # TODO: 用 dist_pid 算线速度 v
        # v = ...

        # TODO: 用 angle_pid 算角速度 omega
        # omega = ...

        # return v, omega
        pass
```

<details>
<summary>点击查看完整 PID 实现</summary>

```python
import math

class PIDController:
    def __init__(self, Kp, Ki, Kd, integral_max=1.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral_max = integral_max
        self.prev_error = 0.0
        self.integral = 0.0

    def reset(self):
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, error, dt):
        # P
        p = self.Kp * error

        # I（限幅）
        self.integral += error * dt
        self.integral = max(-self.integral_max,
                           min(self.integral, self.integral_max))
        i = self.Ki * self.integral

        # D
        derivative = (error - self.prev_error) / dt
        d = self.Kd * derivative

        self.prev_error = error
        return p + i + d


class RobotPIDController:
    def __init__(self, Kp_dist, Ki_dist, Kd_dist,
                 Kp_angle, Ki_angle, Kd_angle):
        self.dist_pid = PIDController(Kp_dist, Ki_dist, Kd_dist, integral_max=2.0)
        self.angle_pid = PIDController(Kp_angle, Ki_angle, Kd_angle, integral_max=1.0)

    def __call__(self, robot, target, dt):
        tx, ty = target

        # 距离误差（欧几里得距离）
        dx, dy = tx - robot.x, ty - robot.y
        dist_error = math.sqrt(dx**2 + dy**2)

        # 角度误差（归一化）
        des_theta = math.atan2(dy, dx)
        angle_error = des_theta - robot.theta
        # 归一化到 [-pi, pi]
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        # 线速度：由距离决定（但不要太快，限幅 2.0 m/s）
        v = self.dist_pid.compute(dist_error, dt)
        v = max(-2.0, min(v, 2.0))

        # 角速度：由角度误差决定
        omega = self.angle_pid.compute(angle_error, dt)
        omega = max(-math.pi, min(omega, math.pi))

        return v, omega
```
</details>

---

### 练习三：轨迹跟踪 + 可视化（20 分钟）

**任务**：把前面两个练习组装起来——让小车先开到 A 点，再开到 B 点，再开回原点。画出完整轨迹。

```python
import math

# TODO: 用之前写的 Robot2D、Simulator、RobotPIDController

# 参数
robot = Robot2D(x=0.0, y=0.0, theta=0.0)
sim = Simulator(robot, dt=0.05)

# 调好的 PID 参数（你可以自己调！）
controller = RobotPIDController(
    Kp_dist=0.8,  Ki_dist=0.05, Kd_dist=0.3,
    Kp_angle=2.0, Ki_angle=0.0,  Kd_angle=0.5,
)

# 路径点
waypoints = [(5, 3), (8, -1), (0, 0)]

all_history = []
for wp in waypoints:
    print(f"前往目标 {wp}...")
    controller.dist_pid.reset()
    controller.angle_pid.reset()
    history = sim.run(controller, target=wp, duration=10.0)

    # 检查是否到达（距离 < 0.1 米算到达）
    final_dist = math.sqrt((robot.x - wp[0])**2 + (robot.y - wp[1])**2)
    if final_dist < 0.15:
        print(f"  ✓ 到达！（最终距离 {final_dist:.3f} 米）")
    else:
        print(f"  ✗ 未到达（最终距离 {final_dist:.3f} 米）")
    all_history.extend(history)

# 可视化
try:
    import matplotlib.pyplot as plt

    xs = [h[1] for h in all_history]
    ys = [h[2] for h in all_history]

    plt.figure(figsize=(8, 8))
    plt.plot(xs, ys, 'b-', linewidth=1.5, alpha=0.8, label='小车轨迹')

    # 标出路径点和箭头
    wpx = [0] + [w[0] for w in waypoints]
    wpy = [0] + [w[1] for w in waypoints]
    plt.plot(wpx, wpy, 'ro-', markersize=8, label='路径点')

    # 每隔 50 步画一个方向箭头
    step = max(1, len(all_history) // 20)
    for i in range(0, len(all_history), step):
        h = all_history[i]
        dx = 0.3 * math.cos(h[3])
        dy = 0.3 * math.sin(h[3])
        plt.arrow(h[1], h[2], dx, dy, head_width=0.15, head_length=0.2,
                 fc='green', ec='green', alpha=0.5)

    plt.xlabel('X (米)')
    plt.ylabel('Y (米)')
    plt.title('PID 控制的 2D 小车轨迹跟踪')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('/tmp/robot_trajectory.png', dpi=150)
    print("\n轨迹图已保存到 /tmp/robot_trajectory.png")
except ImportError:
    print("(安装 matplotlib 可看到轨迹图)")
```

---

### 练习四：PID 调参实验（15 分钟）

**任务**：系统地体验 Kp、Ki、Kd 对控制效果的影响。把下面的参数组合都跑一遍，记录现象。

```python
# 调参实验矩阵
experiments = [
    # (名字, Kp, Ki, Kd, 预期现象)
    ("纯P-弱",   0.3, 0.0, 0.0, "缓慢靠近，停不下来（有静差）"),
    ("纯P-中",   0.8, 0.0, 0.0, "较快靠近，仍有明显静差"),
    ("纯P-猛",   2.0, 0.0, 0.0, "快速靠近但震荡严重，来回晃"),
    ("P+D",      0.8, 0.0, 0.3, "快但震荡被 D 压住了，更平滑"),
    ("P+I",      0.8, 0.1, 0.0, "能到达了（无静差），但可能超调"),
    ("PID-温和", 0.8, 0.05, 0.3, "又快又准又稳——三者的配合"),
    ("你的组合", 1.0, 0.02, 0.5, "自己试着调一组更好的！"),
]

for name, kp, ki, kd, expected in experiments:
    robot = Robot2D()
    sim = Simulator(robot, dt=0.05)
    ctrl = RobotPIDController(
        Kp_dist=kp, Ki_dist=ki, Kd_dist=kd,
        Kp_angle=2.0, Ki_angle=0.0, Kd_angle=0.5,
    )
    sim.run(ctrl, target=(5, 0), duration=8.0)
    final_dist = math.sqrt((robot.x - 5)**2 + (robot.y - 0)**2)

    # 统计超调量和收敛时间
    xs = [h[1] for h in sim.history]
    overshoot = max(0, max(xs) - 5) if xs else 0  # 超过目标的最大距离

    print(f"{name:<12} | 最终距离={final_dist:.3f} | 超调={overshoot:.3f} | 预期: {expected}")
```

---

## 调参直觉完整指南

### PID 三兄弟的性格

```
现象                          →  调整方案
──────────────────────────────────────────────────────
响应太慢，半天到不了             →  增大 Kp
震荡厉害，在目标两侧来回晃        →  减小 Kp 或增大 Kd
停在目标前一点点，永远到不了      →  增大 Ki（消除静差）
冲过头，然后回来，再冲过头（超调） →  增大 Kd（加阻尼）或减小 Ki
越晃越厉害，发散                  →  立即减小 Kp 和 Ki，增大 Kd
到达后还在慢慢漂                  →  Ki 太大或积分未限幅
刚启动时突然猛冲一下              →  D 太大（初始误差变化率大），加低通滤波
```

### 参数数量级参考

针对本文的 2D 小车场景（距离单位米，时间步长 0.05 秒）：

```
参数   典型范围       作用
─────────────────────────────────────
Kp     0.3 ~ 2.0    距离误差转线速度的"油门敏感度"
Ki     0.01 ~ 0.2   很小！消除静差即可，大了必震荡
Kd     0.1 ~ 1.0    阻尼"刹车"，抵消 P 的震荡
```

---

## 学完能做什么 & 下一步

掌握这些内容后，你已经能做出一些真东西了：

- **写一个 2D 小车仿真器**：在终端或画图库里模拟小车从任意位置、任意朝向，用 PID 控制平滑地开到目标点并摆正车头——这是很多机器人课程的第一次大作业。
- **理解并调试真实的入门硬件**：比如给循迹小车、平衡车的控制代码调 PID 参数，你会知道每个旋钮背后的含义，而不是瞎拧。
- **看懂更大的系统**：无人机悬停、机械臂到位、恒温箱控温，内核都是这套"状态估计 + 反馈控制"，PID 是它们的共同祖先。

继续深入的建议路径：

1. **先把本文的代码自己敲一遍并改参数玩**：把 Kp 调大 10 倍看看震荡，把 `dt` 调大看看轨迹失真——亲手玩坏一次胜过读十篇文章。
2. **学一点画图**（如 Python 的 `matplotlib` 库），把仿真轨迹画出来，视觉反馈会让你的调参直觉突飞猛进。
3. **进阶方向**：更准的积分方法（如 Runge-Kutta）、更聪明的控制（如 LQR、MPC），以及带激光雷达和地图的真实机器人定位与导航（ROS 生态）。

最后记住：这个领域的核心不是背公式，而是那套"**量化现状 → 计算差距 → 谨慎调整 → 观察反馈**"的循环——它不只能控制机器人，其实也是做好很多事情的通用方法论。
