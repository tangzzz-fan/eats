# Day 01：核心语法与类设计 (BankAccount) - 快速上手指南

本指南旨在帮助你快速掌握 `Day 01` 练习（[day01_bank_account.py](file:///Users/apple/Developments/Python%20Projects/src/python_projects/core/day01_bank_account.py)）所需的核心面向对象编程 (OOP) 知识点。

## 重难点速览

| 重难点 | 一句话要点 | 易错/关键提示 |
| --- | --- | --- |
| `_balance` 私有命名约定 | 单下划线开头只是“请勿直接访问”的约定，Python 并不强制私有 | 不要写 `account._balance = -100`，一切余额变动必须走 `deposit`/`withdraw` 等带校验的方法 |
| `@property` 只读属性 | 把方法伪装成属性，读取用 `account.balance`（不加括号） | 没有定义 `@balance.setter`，赋值 `account.balance = 100` 会抛 `AttributeError` |
| 存取款边界校验 | 金额必须**大于** 0，即 `amount <= 0`（含 0）一律抛 `ValueError` | 判断条件别写成 `amount < 0`，否则 `deposit(0)` 会漏过校验 |
| 透支校验 | 取款金额超过当前余额时抛 `ValueError` | 先校验后扣款，顺序反了可能出现负余额 |
| `__repr__` vs `__str__` | `__str__` 面向用户（`print` 触发），`__repr__` 面向开发者调试 | 用 `{self.owner!r}` 让字符串自动带引号，输出 `owner='Alice'` 而非 `owner=Alice` |

---

## 1. 核心任务目标

设计并实现一个安全、封装良好的银行账户类 `BankAccount`，满足以下功能要求：
1. **构造初始化 (`__init__`)**：初始化持有人姓名 `owner` 和初始余额 `initial_balance`（初始余额不能为负数）。
2. **私有属性与只读包装 (`_balance` & `@property`)**：使用 `_balance` 存储余额，防止被外部非法篡改，并通过 `@property` 暴露只读属性 `balance`。
3. **存款 (`deposit`)**：存入金额必须大于 0。
4. **取款 (`withdraw`)**：取款金额必须大于 0，且余额必须充足。
5. **计算利息 (`apply_interest`)**：年利率必须大于等于 0，按 `balance += balance * rate` 更新余额。
6. **开发者输出 (`__repr__`)**：重写 `__repr__` 方法，输出格式如 `BankAccount(owner='Alice', balance=100.0)`。

---

## 2. 核心知识点详解

### 2.1 封装与私有属性命名约定
在 Python 中没有像 C++/Java 一样强制的 `private` 关键字。
* 约定使用**单下划线开头**的成员变量（如 `self._balance`）表示私有变量，提示外部不要直接访问。
* 注意这只是命名约定：解释器并不会阻止你访问 `account._balance`，真正的保护来自“只暴露 `@property`、不提供 setter”这一设计。
* 外部不应该直接执行 `account._balance = -100`，所有余额变动必须通过类提供的方法进行安全校验。

### 2.2 `@property` 装饰器实现只读属性
装饰器 `@property` 可以将一个方法伪装成属性来调用：
```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.owner = owner
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        # 外部可以通过 account.balance 读取，但因为没有定义 @balance.setter，
        # 执行 account.balance = 100 会抛出 AttributeError
        return self._balance
```
读取时写成 `account.balance` 即可，不要加括号：`account.balance()` 会把返回的 `float` 当作函数调用，抛出 `TypeError: 'float' object is not callable`。

### 2.3 边界条件校验与异常抛出
业务代码中必须进行强鲁棒性的边界校验：
```python
if amount <= 0:
    raise ValueError("Deposit amount must be greater than 0.")
```
* **存取款校验**：金额 $\le 0$ 时抛出 `ValueError`。
* **透支校验**：取款金额 > 当前余额时抛出 `ValueError`。

### 2.4 魔术方法 `__repr__` vs `__str__`
* `__str__`：面向最终用户的字符串展示，由 `str(obj)` 或 `print(obj)` 触发。
* `__repr__`：面向开发者的调试展示，由 `repr(obj)` 或在交互式命令行中直接敲对象名触发。
* 如果只定义了 `__repr__` 而没有 `__str__`，`print(obj)` 会自动回退到 `__repr__` 的输出——所以练习中只需实现 `__repr__` 也能打印出可读结果。
* 使用 `!r` 自动为字符串加上引号：
```python
def __repr__(self) -> str:
    return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
```

---

## 3. 单元测试验证

完成代码后，运行测试验证：
```bash
.venv/bin/pytest tests/test_day01_bank_account.py
```
