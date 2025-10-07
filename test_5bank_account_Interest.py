from Lab01.bank_account import BankAccount
import pytest


# Тест 5: Начисление процентов
def test_apply_interest_on_savings_adds_balance_and_records_transaction():
    start_balance = 200.0
    rate = 0.05
    acc = BankAccount(owner="Alice", balance=start_balance, account_type="savings", interest_rate=rate)

    interest_returned = acc.apply_interest()

    expected_interest = start_balance * rate
    expected_balance = start_balance + expected_interest

    assert interest_returned == pytest.approx(expected_interest), "Метод должен вернуть начисленные проценты"
    assert acc.get_balance() == pytest.approx(expected_balance), "Баланс должен увеличиться на сумму процентов"

    # Проверяем запись в истории
    txs = acc.get_transactions()
    assert len(txs) == 1, "Должна появиться запись с типом interest"
    tx = txs[0]
    assert tx["type"] == "interest", "Тип операции должен быть interest"
    assert tx["amount"] == pytest.approx(expected_interest), "В записи должна быть сумма начисленных процентов"
    assert tx["balance"] == pytest.approx(expected_balance), "Поле balance в записи - новый баланс после начисления"
    assert tx["target"] is None, "Для начисления процентов целевой аккаунт не используется"
    assert isinstance(tx["date"], str) and len(tx["date"]) >= 16, "Должна быть строка с датой/временем транзакции"
