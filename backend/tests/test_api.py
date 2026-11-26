from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Создаем изолированную тестовую БД в оперативной памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Подменяем зависимость БД в приложении на тестовую
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_filter_cards():
    # 1. Создаем дебетовую бесплатную карту
    card_1 = {
        "name": "Black",
        "bank_name": "Т-Банк",
        "card_type": "debit",
        "annual_fee": 0,
        "cashback_percent": 5.0,
        "apply_url": "https://example.com",
    }
    res1 = client.post("/api/cards", json=card_1)
    assert res1.status_code == 201
    assert res1.json()["name"] == "Black"

    # 2. Создаем кредитную платную карту
    card_2 = {
        "name": "Platinum",
        "bank_name": "Альфа-Банк",
        "card_type": "credit",
        "annual_fee": 990,
        "cashback_percent": 10.0,
        "apply_url": "https://example.com",
    }
    res2 = client.post("/api/cards", json=card_2)
    assert res2.status_code == 201

    # 3. Проверяем получение всех карт
    all_cards = client.get("/api/cards").json()
    assert len(all_cards) == 2

    # 4. Проверяем фильтр: только бесплатные
    free_cards = client.get("/api/cards?free_only=true").json()
    assert len(free_cards) == 1
    assert free_cards[0]["bank_name"] == "Т-Банк"

    # 5. Проверяем фильтр: кэшбэк от 8%
    high_cashback = client.get("/api/cards?min_cashback=8").json()
    assert len(high_cashback) == 1
    assert high_cashback[0]["card_type"] == "credit"
