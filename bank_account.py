from datetime import datetime


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0, account_type: str = "checking", interest_rate: float = 0.0):
        if not owner:
            raise ValueError("Владелец счёта должен быть указан")
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        if account_type not in ("checking", "savings"):
            raise ValueError("Неверный тип счёта")

        self.owner = owner
        self.balance = balance
        self.account_type = account_type
        self.interest_rate = interest_rate if account_type == "savings" else 0.0
        self.transactions = []

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount
        self._add_transaction("deposit", amount)
        return self.balance

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self.balance:
            raise ValueError("Недостаточно средств на счёте")
        self.balance -= amount
        self._add_transaction("withdraw", -amount)
        return self.balance

    def transfer(self, target_account, amount: float):
        if not isinstance(target_account, BankAccount):
            raise TypeError("Перевод возможен только на другой банковский счёт")
        self.withdraw(amount)
        target_account.deposit(amount)
        self._add_transaction("transfer", -amount, target_account.owner)
        return self.balance, target_account.balance

    def apply_interest(self):
        if self.account_type == "savings":
            interest = self.balance * self.interest_rate
            self.balance += interest
            self._add_transaction("interest", interest)
            return interest
        else:
            raise ValueError("Проценты применимы только к накопительным счетам")

    def get_balance(self) -> float:
        return self.balance

    def get_transactions(self):
        return self.transactions

    def _add_transaction(self, transaction_type: str, amount: float, target: str = None):
        self.transactions.append({
            "type": transaction_type,
            "amount": amount,
            "target": target,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance": self.balance
        })
