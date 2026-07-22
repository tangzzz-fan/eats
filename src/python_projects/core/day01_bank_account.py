class BankAccount:
    """
    Day 1: 核心语法与类设计练习 - 银行账户类
    
    目标：
    1. 使用初始化方法 `__init__` 初始化账户持有人名字和初始余额。
    2. 使用私有属性（通常以单下划线 `_` 开头）保存余额，防止被外部直接修改。
    3. 使用 `@property` 装饰器定义只读属性 `balance`。
    4. 实现 `deposit`（存款）和 `withdraw`（取款）方法，包含边界值校验（如金额不能为负数，余额不能透支）。
    5. 实现 `apply_interest`（计算利息）方法，根据给定的年利率（例如 0.05 代表 5%）增加余额。
    6. 实现特殊方法 `__repr__`，使得打印对象时能看到友好的格式，例如 `BankAccount(owner='Alice', balance=100.0)`。
    
    知识体系清单：
    - 类的初始化方法 `__init__` 与私有属性遮蔽（以单下划线 `_` 开头的变量作为约定私有成员）。
    - 属性装饰器 `@property` 机制（用于暴露只读接口，防止外部直接对其进行赋值覆盖，达到数据封装的目的）。
    - 特殊方法（魔术方法）的重写：`__repr__` 与 `__str__` 的区别。`__repr__` 偏向开发调试输出，`__str__` 偏向用户友好输出。
    
    工程实践避坑指南：
    - 属性篡改：Python 没有强制的 `private` 限制，单下划线仅作内部提示。必须遵守约定，不要直接通过 `obj._balance = value` 覆盖数值。
    - 边界条件校验：存取款如果不校验金额大于 0，一旦传入负数存入，会直接破坏业务一致性，导致账户数值错乱。
    """
    
    def __init__(self, owner: str, initial_balance: float = 0.0):
        """
        初始化账户。
        
        :param owner: 账户所有人姓名
        :param initial_balance: 初始余额（默认为 0.0）。注意：初始余额也需要校验不能为负数！
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        
        self.owner = owner
        # 我们默认初始化私有属性，以便后续实例化不报错，你可以更改这里的实现
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        """
        只读的余额属性。
        使用 @property 可以让外部像访问普通属性一样访问余额（如 account.balance），
        但因为没有定义 @balance.setter，外部直接赋值（如 account.balance = 100）会抛出 AttributeError。
        """
        # TODO: 请在此处返回私有余额变量的值
        return self._balance

    def deposit(self, amount: float) -> float:
        """
        存款方法。
        
        :param amount: 存款金额，必须大于 0。
        :return: 存款后的最新余额。
        """
        # TODO: 1. 检查 amount 是否大于 0，若不大于 0 则抛出 ValueError 异常。
        # TODO: 2. 将金额累加到私有余额中。
        # TODO: 3. 返回更新后的余额。
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        """
        取款方法。
        
        :param amount: 取款金额，必须大于 0。
        :return: 取款后的最新余额。
        """
        # TODO: 1. 检查 amount 是否大于 0，若不大于 0 则抛出 ValueError 异常。
        # TODO: 2. 检查余额是否足够取款（即 self.balance >= amount），若不足则抛出 ValueError 异常。
        # TODO: 3. 从私有余额中扣除相应金额。
        # TODO: 4. 返回更新后的余额。
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than 0.")
        if self.balance < amount:
            raise ValueError("Insufficient balance.")
        self._balance -= amount
        return self._balance

    def apply_interest(self, rate: float) -> float:
        """
        计算并结算利息。
        
        :param rate: 年利率（例如 0.05 代表 5%），必须大于等于 0。
        :return: 结算利息后的最新余额。
        """
        # TODO: 1. 检查利率 rate 是否为正数，若小于 0 则抛出 ValueError。
        # TODO: 2. 计算利息（利息 = 余额 * 利率）并将利息加到余额中。
        # TODO: 3. 返回更新后的余额。
        if rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self._balance += self._balance * rate
        return self._balance

    def __repr__(self) -> str:
        """
        返回对象的字符串表示，方便调试 and 打印。
        期望格式：BankAccount(owner='姓名', balance=当前余额)
        """
        # TODO: 请在此处返回格式化后的字符串
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
