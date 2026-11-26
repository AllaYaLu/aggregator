from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Пока используем локальный файл SQLite, позже заменим на PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./cards.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Зависимость (Dependency) для получения сессии БД в каждом запросе
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
