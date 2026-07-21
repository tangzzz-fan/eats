import pytest
from python_projects.core.day01_bank_account import BankAccount

def test_bank_account_initialization():
    account = BankAccount(owner="Alice", initial_balance=100.0)
    assert account.owner == "Alice"
    try:
        assert account.balance == 100.0
    except NotImplementedError:
        pytest.skip("BankAccount.balance is not implemented yet.")

def test_bank_account_read_only_balance():
    account = BankAccount(owner="Alice", initial_balance=100.0)
    with pytest.raises(AttributeError):
        account.balance = 200.0  # type: ignore

def test_bank_account_deposit():
    account = BankAccount(owner="Alice", initial_balance=100.0)
    try:
        new_balance = account.deposit(50.0)
        assert new_balance == 150.0
        assert account.balance == 150.0
    except NotImplementedError:
        pytest.skip("BankAccount.deposit is not implemented yet.")

def test_bank_account_withdraw():
    account = BankAccount(owner="Alice", initial_balance=100.0)
    try:
        new_balance = account.withdraw(30.0)
        assert new_balance == 70.0
        assert account.balance == 70.0
    except NotImplementedError:
        pytest.skip("BankAccount.withdraw is not implemented yet.")
