def add(num1: int, num2: 2):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds in the bank account."""
    pass

class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds.")
        self.balance -= amount

    def collect_interest(self, interest_rate: float):
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self.balance += self.balance * interest_rate