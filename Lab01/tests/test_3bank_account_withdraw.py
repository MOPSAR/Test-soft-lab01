from Lab01.bank_account import BankAccount
import pytest


# Тест 3А: Снятие уменьшает баланс и возвращает новое значение
def test_withdraw_decreases_balance_and_returns_new_balance():
    acc = BankAccount(owner="Alice", balance=120.0, account_type="checking")
    amount = 35.0
    start = acc.get_balance()

    returned = acc.withdraw(amount)

    assert acc.get_balance() == start - amount, "Баланс должен уменьшиться на сумму снятия"
    assert returned == acc.get_balance(), "Метод должен возвращать текущее значение баланса"


# Тест 3Б: Неверные суммы
@pytest.mark.parametrize("bad_amount", [0.0, -0.01, -10])
def test_withdraw_invalid_amount_raises_and_balance_unchanged(bad_amount):
    acc = BankAccount(owner="Bob", balance=50.0, account_type="checking")
    start = acc.get_balance()

    with pytest.raises(ValueError):
        acc.withdraw(bad_amount)

    assert acc.get_balance() == start, "При ошибке баланс должен остаться без изменений"


# Тест 3В: Превышение баланса
def test_withdraw_over_balance_raises_and_doesnt_change_balance():
    acc = BankAccount(owner="Alex", balance=40.0, account_type="checking")
    start = acc.get_balance()

    with pytest.raises(ValueError):
        acc.withdraw(41.0)

    assert acc.get_balance() == start, "Баланс не должен измениться при ошибке превышения"


# Тест 3Г: Запись в историю транзакций
def test_withdraw_records_transaction():
    acc = BankAccount(owner="Dave", balance=75.0, account_type="checking")
    amount = 25.0

    new_balance = acc.withdraw(amount)
    txs = acc.get_transactions()

    assert len(txs) == 1, "Должна быть одна запись о снятии"
    tx = txs[0]
    assert tx["type"] == "withdraw", "Тип операции должен быть withdraw"
    assert tx["amount"] == -amount, "Сумма в истории для снятия должна быть со знаком минус"
    assert tx["balance"] == new_balance, "Поле balance в транзакции должно отражать новый баланс"
    assert isinstance(tx["date"], str) and len(tx["date"]) >= 16, "Должна быть дата/время транзакции"
    assert tx["target"] is None, "Поле target для снятия должно быть None"
