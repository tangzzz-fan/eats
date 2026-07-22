# Day 03：高级语法特性 (重试装饰器与生成器) - 快速上手指南

本指南旨在帮助你快速掌握 `Day 03` 练习（[day03_tools.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/common/day03_tools.py)）中的 Python 闭包、带参装饰器与生成器（Generator）机制。

---

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
| --- | --- | --- |
| 带参装饰器的三层嵌套 | 比无参装饰器多一层：参数层 → 函数层 → 执行层 | `@retry(max_attempts=3)` 必须带括号调用；写成 `@retry`（无括号）会把函数当参数传入，直接报错 |
| 最后一次重试的边界判断 | `attempt == max_attempts - 1` 时才抛出异常 | `range(max_attempts)` 从 0 开始，最后一次循环的下标是 `max_attempts - 1`，不是 `max_attempts` |
| `@functools.wraps(func)` | 把原函数的 `__name__`、`__doc__` 复制到 `wrapper` 上 | 不加它会导致反射诊断失效、测试框架识别不到原函数名 |
| `yield` 的暂停与恢复 | 遇到 `yield` 挂起函数，下次 `next()` 从挂起处继续 | 正因"按需推进一步"，`while True` 的无限生成器才只占 O(1) 内存 |
| 异常冒泡 (raise) | 重试次数用尽后，异常必须重新抛给调用方 | 若只是 `print` 或 `pass` 吞掉异常，调用方无法感知失败，重试机制形同虚设 |

---

## 1. 核心任务目标

1. **带参数的自动重试装饰器 (`@retry`)**：
   - 语法：`@retry(max_attempts=3, delay=1.0)`
   - 作用：装饰可能抛出异常的函数。捕获异常后，等待 `delay` 秒并自动重试，直至达到 `max_attempts`；若最后一次仍然失败，则将该异常冒泡抛出。
2. **无限斐波那契生成器 (`fibonacci_generator`)**：
   - 作用：利用 `yield` 实现一个无限产生斐波那契数列（0, 1, 1, 2, 3, 5, 8...）的迭代器。

---

## 2. 核心知识点详解

### 2.1 带参数装饰器的三层结构

常规装饰器不需要参数，只有两层函数；而**带参数的装饰器有三层嵌套**：

```python
import functools
import time
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    # 第一层：接收装饰器自身的参数 (max_attempts, delay)
    def decorator(func: Callable) -> Callable:
        # 第二层：接收被装饰的目标函数 (func)
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 第三层：接收目标函数的任意参数 (*args, **kwargs)
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)  # 成功则直接返回
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e  # 最后一次失败，冒泡抛出异常
                    time.sleep(delay)
                    
        return wrapper
    return decorator
```

调用时三层一一对应：`retry(max_attempts=3, delay=1.0)` 先返回 `decorator`，`decorator(func)` 再返回 `wrapper`，此后调用原函数实际执行的是 `wrapper`。因此带参装饰器必须写成 `@retry(...)`（带括号）；若写成 `@retry`，目标函数会被直接传给第一层当参数，导致参数错位报错。

另外注意边界判断：`range(max_attempts)` 的下标从 `0` 到 `max_attempts - 1`，所以 `attempt == max_attempts - 1` 才是"最后一次"。若误写成 `attempt == max_attempts`，条件永不成立，循环结束后 `wrapper` 隐式返回 `None`，异常会被静默吞掉。

#### `@functools.wraps(func)` 的重要作用：
若不用 `@functools.wraps`，被装饰函数的 `__name__` 和 `__doc__` 属性会被替换为内层函数名 `wrapper`，导致反射诊断失效或单元测试识别错误。

---

### 2.2 生成器 (Generator) 与 `yield` 关键字

生成器是一种特殊的迭代器，通过 `yield` 关键字实现**函数的暂停与状态保留**。

```python
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a          # 暂停并返回当前 a 的值
        a, b = b, a + b  # 下一次调用 next() 时从此处恢复执行
```

消费这个生成器时，用 `next()` 逐个取值（切勿直接 `list(gen)`，无限序列会永远跑不完）：

```python
gen = fibonacci_generator()
print([next(gen) for _ in range(7)])  # [0, 1, 1, 2, 3, 5, 8]
```

#### 为什么无限循环 `while True` 不会导致内存爆满？
因为 `yield` 会挂起程序执行逻辑，只有当外部主动调用 `next(gen)` 时，代码才会向前推进一步，内存中仅保存当前的状态变量 `a` 和 `b`。

---

## 3. 单元测试验证

完成代码后，运行测试验证：

提示：若测试用例里包含"必定失败"的函数，真实执行 `time.sleep(delay)` 会让每个用例白等 `delay * (max_attempts - 1)` 秒；练习或写测试时可把 `delay` 传小值（如 `0.01`）避免拖慢测试。

```bash
.venv/bin/pytest tests/test_day03_tools.py
```
