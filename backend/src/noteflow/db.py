"""Модуль работы с базой данных.

Отвечает за инициализацию соединения, создание схемы и предоставление сессий.
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///noteflow.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Создаёт все таблицы в базе данных.

    Вызывается при первом запуске приложения. Если таблицы уже существуют —
    ничего не делает.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    """Контекстный менеджер для работы с сессией БД.

    Гарантирует закрытие сессии даже при возникновении исключения.

    Yields:
        Session: Сессия SQLAlchemy.

    Examples:
        >>> with get_session() as session:
        ...     user = session.query(User).first()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()