"""Модели данных NoteFlow.

Содержит SQLAlchemy-модели для пользователей, заметок и тегов.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


note_tag = Table(
    "note_tag",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    """Пользователь сервиса.

    Attributes:
        id (int): Уникальный идентификатор.
        email (str): Email пользователя (уникальный).
        password_hash (str): Хеш пароля.
        created_at (datetime): Дата регистрации.
        notes (list[Note]): Список заметок пользователя.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")


class Note(Base):
    """Заметка пользователя.

    Attributes:
        id (int): Уникальный идентификатор.
        title (str): Заголовок заметки.
        body (str): Тело заметки (Markdown).
        created_at (datetime): Дата создания.
        updated_at (datetime): Дата последнего редактирования.
        user_id (int): ID владельца.
        tags (list[Tag]): Теги заметки.
    """

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="notes")
    tags = relationship("Tag", secondary=note_tag, back_populates="notes")


class Tag(Base):
    """Тег для категоризации заметок.

    Attributes:
        id (int): Уникальный идентификатор.
        name (str): Название тега (уникальное).
        notes (list[Note]): Заметки с этим тегом.
    """

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    notes = relationship("Note", secondary=note_tag, back_populates="tags")