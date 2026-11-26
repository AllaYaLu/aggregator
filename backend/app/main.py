
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin  # <-- НОВОЕ
from sqlalchemy.orm import Session

from . import models, schemas
from .admin import BankCardAdmin  # <-- НОВОЕ
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Cards Aggregator API", version="1.0.0")

# Подключаем админ-панель по адресу /admin  <-- НОВОЕ
admin = Admin(app, engine)
admin.add_view(BankCardAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check():
    """Эндпоинт для проверки работоспособности сервиса (нужен для Docker и CI/CD)"""
    return {"status": "ok"}


@app.get("/api/cards", response_model=list[schemas.CardResponse], tags=["Cards"])
def get_cards(
    card_type: str | None = Query(None, description="Фильтр по типу: debit или credit"),
    free_only: bool = Query(False, description="Только с бесплатным обслуживанием"),
    min_cashback: float | None = Query(None, ge=0, description="Минимальный процент кэшбэка"),
    db: Session = Depends(get_db),
):
    """Получить список карт с поддержкой фильтрации"""
    query = db.query(models.BankCard)

    if card_type:
        query = query.filter(models.BankCard.card_type == card_type)
    if free_only:
        query = query.filter(models.BankCard.annual_fee == 0)
    if min_cashback is not None:
        query = query.filter(models.BankCard.cashback_percent >= min_cashback)

    return query.all()


@app.post("/api/cards", response_model=schemas.CardResponse, status_code=201, tags=["Cards"])
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    """Добавить новую банковскую карту"""
    db_card = models.BankCard(**card.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
