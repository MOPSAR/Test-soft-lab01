from Lab01.bank_account import BankAccount
import pytest

# Тест 2А: Пополнение увеличивает баланс и возвращает новое значение
def test_deposit_increases_balance_and_returns_new_balance():
    acc = BankAccount(owner="Alice", balance=100.0, account_type="checking")
    amount = 25.0
    start = acc.get_balance()

    returned = acc.deposit(amount)

    assert acc.get_balance() == start + amount, "Баланс должен увеличиться на сумму пополнения"
    assert returned == acc.get_balance(), "Метод должен возвращать текущее значение баланса"


# Тест 2Б: Неверные суммы пополнения
@pytest.mark.parametrize("bad_amount", [0.0, -0.01, -10])
def test_deposit_invalid_amount_raises(bad_amount):
    acc = BankAccount(owner="Bob", balance=50.0, account_type="checking")

    with pytest.raises(ValueError):
        acc.deposit(bad_amount)

    assert acc.get_balance() == 50.0, "При ошибке баланс должен остаться без изменений"


# Тест 2В: Запись в историю транзакций
def test_deposit_records_transaction():
    acc = BankAccount(owner="Alex", balance=10.0, account_type="checking")
    amount = 7.5

    new_balance = acc.deposit(amount)
    txs = acc.get_transactions()

    assert len(txs) == 1, "Должна быть одна запись о пополнении"
    tx = txs[0]
    assert tx["type"] == "deposit", "Тип операции должен быть deposit"
    assert tx["amount"] == amount, "Сумма операции в истории должна совпадать с пополнением"
    assert tx["balance"] == new_balance, "Поле balance в транзакции должно отражать новый баланс"
    assert isinstance(tx["date"], str) and len(tx["date"]) >= 16, "Должна быть дата/время транзакции"
    assert tx["target"] is None, "Поле target для пополнения должно быть None"

