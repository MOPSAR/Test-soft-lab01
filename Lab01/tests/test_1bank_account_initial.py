from Lab01.bank_account import BankAccount
import pytest


# Тест №1А: Верные данные при инициализации счёта
def test_initial__valid_inputs():
    owner = "Alice"
    balance = 100.0
    account_type = "savings"
    interest_rate = 0.05

    acc = BankAccount(owner, balance, account_type, interest_rate)

    assert acc.owner == owner, "Владелец должен сохраниться как передан"
    assert acc.balance == balance, "Начальный баланс должен совпадать"
    assert acc.account_type == account_type, "Тип счёта должен сохраниться"
    assert acc.interest_rate == interest_rate, "Для savings ставка принимается"
    assert acc.get_transactions() == [], "История при старте пустая"


# Тест №1Б: Неверные данные при инициализации счёта
@pytest.mark.parametrize(
    "kwargs, expected_error",
    [
        # Пустой владелец
        (dict(owner="", balance=0.0, account_type="checking", interest_rate=0.0),
         ValueError),

        # Отрицательный баланс
        (dict(owner="Bob", balance=-1.0, account_type="checking", interest_rate=0.0),
         ValueError),

        # Неверный тип счёта
        (dict(owner="Bob", balance=0.0, account_type="investment", interest_rate=0.1),
         ValueError),
    ],
)
def test_initial_invalid_inputs(kwargs, expected_error):
    with pytest.raises(expected_error):
        BankAccount(**kwargs)
