import time
import functools
from typing import Callable, Any

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Day 3: 数据处理与高级特性 - 重试装饰器
    
    目标：
    实现一个带参数的装饰器 `@retry`，用于装饰可能会失败的函数（例如网络请求或数据库查询）。
    如果被装饰的函数运行抛出异常，装饰器会自动捕获该异常，等待 `delay` 秒后重试。
    如果尝试次数达到 `max_attempts` 仍失败，则抛出最后一次的异常。
    
    提示与关键点：
    1. 带参数的装饰器有三层结构：
       - 第一层：接收装饰器参数（`max_attempts`, `delay`），返回真正的装饰器。
       - 第二层：接收目标函数（`func`），返回包裹函数。
       - 第三层：接收目标函数的任意参数（`*args`, `**kwargs`），执行重试逻辑。
    2. 使用 `@functools.wraps(func)` 保持目标函数的元数据（例如 `__name__` 和 `__doc__`）。
    3. 在循环中执行 `func(*args, **kwargs)`，如果成功则直接 `return` 结果。
    4. 如果抛出异常且未达到最大尝试次数，使用 `time.sleep(delay)` 暂停，然后继续循环。
    5. 达到最大次数时，直接让异常冒泡抛出。
    
    知识体系清单：
    - 闭包与带参装饰器的多层函数嵌套构造。
    - `functools.wraps` 保留原函数签名、文档说明、`__name__` 属性的作用。
    - `yield` 关键字与生成器机制的执行暂停特性。
    
    工程实践避坑指南：
    - 丢失包装原信息：不用 `@functools.wraps` 会使得被装饰的函数重命名为内层 `wrapper`，导致测试框架识别失败及反射诊断信息丢失。
    - 延迟阻滞线程：重试逻辑中使用同步 `time.sleep(delay)` 会阻塞当前运行线程。在异步网络框架中（如 FastAPI 异步端点），若非必须，应改用 `await asyncio.sleep(delay)`。
    
    :param max_attempts: 最大尝试次数，默认为 3。
    :param delay: 每次重试之间的等待秒数，默认为 1.0 秒。
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # TODO: 请在此处实现重试逻辑
            # 1. 循环最多 max_attempts 次
            # 2. 用 try...except 包裹函数执行：func(*args, **kwargs)
            # 3. 执行成功则直接返回结果
            # 4. 执行失败则捕获异常，打印重试提示，并 time.sleep(delay)
            # 5. 如果是最后一次尝试依然失败，则 raise 该异常
            raise NotImplementedError("Please implement the retry decorator logic")
        return wrapper
    return decorator


def fibonacci_generator():
    """
    Day 3: 数据处理与高级特性 - 无限斐波那契数列生成器
    
    目标：
    用生成器（Generator）实现一个无限产生斐波那契数（0, 1, 1, 2, 3, 5, 8, 13, ...）的迭代器。
    
    提示与关键点：
    1. 生成器使用 `yield` 关键字来返回值，并在每次 yield 后暂停状态，下次迭代时继续从该位置执行。
    2. 使用 `while True` 实现无限循环，但由于有 `yield` 挂起，不会导致 CPU 跑满或内存溢出。
    3. 数列前两项为 0 和 1，后续每一项为前两项之和。
    
    用法示例：
    fib = fibonacci_generator()
    print(next(fib))  # 0
    print(next(fib))  # 1
    print(next(fib))  # 1
    print(next(fib))  # 2
    """
    # TODO: 请实现无限斐波那契数列的生成逻辑
    # 1. 初始化前两项，例如 a, b = 0, 1
    # 2. 使用 while True 循环
    # 3. 每次 yield 当前的 a
    # 4. 更新 a, b 的值为下一个数（a, b = b, a + b）
    raise NotImplementedError("Please implement fibonacci_generator")


if __name__ == "__main__":
    # 测试生成器
    print("Testing Fibonacci Generator (first 8 numbers):")
    try:
        fib = fibonacci_generator()
        for _ in range(8):
            print(next(fib), end=" ")
        print()
    except (TypeError, NotImplementedError):
        print("\n[Please implement fibonacci_generator first!]")
        
    # 测试重试装饰器
    print("\nTesting Retry Decorator:")
    attempts = 0
    
    @retry(max_attempts=3, delay=0.5)
    def unstable_function():
        global attempts
        attempts += 1
        print(f"Executing unstable_function (Attempt {attempts})...")
        if attempts < 3:
            raise ConnectionError("Temporary network issue")
        return "Success!"
        
    try:
        res = unstable_function()
        print("Function output:", res)
    except Exception as e:
        print("Failed with exception:", e)
