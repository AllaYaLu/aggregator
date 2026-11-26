from sqlalchemy import Column, Float, Integer, String

from .database import Base


class BankCard(Base):
    __tablename__ = "bank_cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)        # Название (напр. "Tinkoff Black")
    bank_name = Column(String, index=True, nullable=False)   # Банк (напр. "Т-Банк")
    card_type = Column(String, index=True, nullable=False)   # "debit" или "credit"
    annual_fee = Column(Integer, default=0)                  # Обслуживание в год (0 = бесплатно)
    cashback_percent = Column(Float, default=0.0)            # Максимальный кэшбэк (%)
    apply_url = Column(String, nullable=False)               # Ссылка на оформление
    image_url = Column(String, nullable=True)                # Ссылка на картинку карты
