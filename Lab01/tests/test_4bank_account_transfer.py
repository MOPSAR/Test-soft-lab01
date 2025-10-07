from Lab01.bank_account import BankAccount
import pytest


# Тест 4А: Перевод обновляет оба баланса
def test_transfer_updates_both_balances():
    sender = BankAccount(owner="Alice", balance=100.0, account_type="checking")
    receiver = BankAccount(owner="Bob", balance=10.0, account_type="checking")
    amount = 35.0

    s_bal, r_bal = sender.transfer(receiver, amount)

    assert s_bal == sender.get_balance() == 65.0, "У отправителя должно списаться ровно amount"
    assert r_bal == receiver.get_balance() == 45.0, "У получателя должно зачислиться ровно amount"


# Тест 4Б: Сумма средств сохраняется
def test_transfer_preserves_total_funds():
    sender = BankAccount("Alex", 70.0, "checking")
    receiver = BankAccount("Maria", 5.0, "checking")
    total_before = sender.get_balance() + receiver.get_balance()

    sender.transfer(receiver, 20.0)

    total_after = sender.get_balance() + receiver.get_balance()
    assert total_after == total_before, "Перевод не должен менять суммарные средства системы"


# Тест 4В: История у отправителя и получателя
def test_transfer_records_transactions_sender_and_receiver():
    sender = BankAccount("Alice", 60.0, "checking")
    receiver = BankAccount("Bob", 3.0, "checking")

    amount = 25.0
    sender.transfer(receiver, amount)

    s_txs = sender.get_transactions()
    r_txs = receiver.get_transactions()

    # Отправитель: 2 записи
    assert len(s_txs) == 2, "У отправителя должны быть withdraw и transfer"
    # 1) withdraw
    w = s_txs[0]
    assert w["type"] == "withdraw", "Первая запись - списание"
    assert w["amount"] == -amount, "Для withdraw сумма со знаком минус"
    # 2) transfer
    t = s_txs[1]
    assert t["type"] == "transfer", "Вторая запись - факт перевода"
    assert t["amount"] == -amount, "В записи transfer фиксируется списанная сумма"
    assert t["target"] == receiver.owner, "В записи transfer должен быть получатель"
    assert t["balance"] == sender.get_balance(), "balance в записи соответствует текущему балансу отправителя"

    # Получатель: 1 запись - deposit
    assert len(r_txs) == 1, "У получателя должна быть одна запись - зачисление"
    d = r_txs[0]
    assert d["type"] == "deposit", "Тип у получателя - deposit"
    assert d["amount"] == amount, "Сумма зачисления положительная"
    assert d["balance"] == receiver.get_balance(), "balance должен соответствовать новому балансу получателя"


# Тест 4Г: Тип получателя только BankAccount
def test_transfer_type_check_target_account():
    sender = BankAccount("Alice", 50.0, "checking")
    not_account = object()

    with pytest.raises(TypeError):
        sender.transfer(not_account, 10.0)


# Тест 4Д: Перевод, если недостаточно средств
def test_transfer_if_not_enough_balance():
    sender = BankAccount("Pug", 10.0, "checking")
    receiver = BankAccount("Bul-dog", 100.0, "checking")
    s_before, r_before = sender.get_balance(), receiver.get_balance()

    with pytest.raises(ValueError):
        sender.transfer(receiver, 999.0)

    assert sender.get_balance() == s_before, "Баланс отправителя не должен измениться"
    assert receiver.get_balance() == r_before, "Баланс получателя не должен измениться"
    assert len(sender.get_transactions()) == 0, "История отправителя не должна пополняться при ошибке"
    assert len(receiver.get_transactions()) == 0, "История получателя не должна пополняться при ошибке"
