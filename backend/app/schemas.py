
from pydantic import BaseModel, Field


class CardBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    bank_name: str = Field(..., min_length=2, max_length=100)
    card_type: str = Field(..., pattern="^(debit|credit)$")  # Только debit или credit
    annual_fee: int = Field(default=0, ge=0)                 # Не может быть меньше 0
    cashback_percent: float = Field(default=0.0, ge=0.0, le=100.0)
    apply_url: str
    image_url: str | None = None


class CardCreate(CardBase):
    pass


class CardResponse(CardBase):
    id: int

    class Config:
        from_attributes = True  # Позволяет Pydantic читать данные из моделей SQLAlchemy
