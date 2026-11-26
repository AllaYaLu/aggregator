from sqladmin import ModelView

from .models import BankCard


class BankCardAdmin(ModelView, model=BankCard):
    name = "Банковская карта"
    name_plural = "Банковские карты"
    icon = "fa-solid fa-credit-card"

    # Какие колонки показывать в общем списке
    column_list = [
        BankCard.id,
        BankCard.bank_name,
        BankCard.name,
        BankCard.card_type,
        BankCard.annual_fee,
        BankCard.cashback_percent,
    ]
    # По каким полям можно искать
    column_searchable_list = [BankCard.name, BankCard.bank_name]
    # По каким полям можно сортировать
    column_sortable_list = [BankCard.annual_fee, BankCard.cashback_percent]
