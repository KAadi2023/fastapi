import pytest
from app.calculations import InsufficientFundsError, add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_balance_bank_account():
    return BankAccount("123456", 0)

@pytest.fixture
def bank_account():
    return BankAccount("123456", 10000)

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (-5, -5, -10),
])
def test_add(num1, num2, expected):
    print("Testing the add function...")
    assert add(num1, num2) == expected

def test_subtract():
    print("Testing the subtract function...")
    assert subtract(5, 3) == 2

def test_multiply():
    print("Testing the multiply function...")
    assert multiply(2, 3) == 6

def test_divide():
    print("Testing the divide function...")
    assert divide(6, 3) == 2


def test_bank_set_initial_balance(bank_account):
    assert bank_account.balance == 10000

def test_bank_default_balance(zero_balance_bank_account):
    assert zero_balance_bank_account.balance == 0.0


def test_bank_deposit(bank_account):
    print("Testing BankAccount deposit...")
    bank_account.deposit(5000)
    assert bank_account.balance == 15000

def test_bank_withdraw(bank_account):
    print("Testing BankAccount withdraw...")
    bank_account.withdraw(3000)
    assert bank_account.balance == 7000

def test_collect_interest(bank_account):
    print("Testing BankAccount collect_interest...")
    bank_account.collect_interest(0.1)  # 10% interest
    assert bank_account.balance == 11000

@pytest.mark.parametrize("deposit_amount, withdraw_amount, interest_rate, expected_balance", [
    (1000, 500, 0.05, 525.0),
    (2000, 1000, 0.1, 1100.0),
    (500, 200, 0.2, 360.0),
])

def test_bank_account_transactions(zero_balance_bank_account, deposit_amount, withdraw_amount, interest_rate, expected_balance):
    print("Testing BankAccount transactions...")
    zero_balance_bank_account.deposit(deposit_amount)
    zero_balance_bank_account.withdraw(withdraw_amount)
    zero_balance_bank_account.collect_interest(interest_rate)
    assert zero_balance_bank_account.balance == expected_balance

def test_insufficient_funds(bank_account):
    print("Testing BankAccount insufficient funds...")
    with pytest.raises(InsufficientFundsError):
        bank_account.withdraw(20000)