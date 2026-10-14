"""Модуль управления заметками (CRUD).

Реализует создание, чтение, редактирование и удаление заметок.
"""

from .db import get_session
from .models import Note


def create_note(user_id: int, title: str, body: str = "") -> dict:
    """Создаёт новую заметку.

    Args:
        user_id (int): ID владельца заметки.
        title (str): Заголовок заметки.
        body (str, optional): Тело заметки в Markdown. По умолчанию пусто.

    Returns:
        dict: Данные созданной заметки.

    Raises:
        ValueError: Если заголовок пустой.

    Examples:
        >>> note = create_note(1, "Список покупок", "- хлеб\\n- молоко")
        >>> note["title"]
        'Список покупок'
    """
    if not title.strip():
        raise ValueError("Заголовок не может быть пустым")

    with get_session() as session:
        note = Note(user_id=user_id, title=title, body=body)
        session.add(note)
        session.flush()
        return {"id": note.id, "title": note.title, "body": note.body}


def get_notes(user_id: int) -> list[dict]:
    """Возвращает список заметок пользователя, отсортированный по дате.

    Args:
        user_id (int): ID пользователя.

    Returns:
        list[dict]: Список заметок.
    """
    with get_session() as session:
        notes = (
            session.query(Note)
            .filter_by(user_id=user_id)
            .order_by(Note.created_at.desc())
            .all()
        )
        return [{"id": n.id, "title": n.title, "body": n.body} for n in notes]


def update_note(note_id: int, user_id: int, title: str, body: str) -> dict:
    """Обновляет существующую заметку.

    Args:
        note_id (int): ID заметки.
        user_id (int): ID владельца (проверка прав).
        title (str): Новый заголовок.
        body (str): Новое тело.

    Returns:
        dict: Обновлённые данные заметки.

    Raises:
        ValueError: Если заметка не найдена или не принадлежит пользователю.
    """
    with get_session() as session:
        note = session.query(Note).filter_by(id=note_id, user_id=user_id).first()
        if not note:
            raise ValueError("Заметка не найдена")
        note.title = title
        note.body = body
        session.flush()
        return {"id": note.id, "title": note.title, "body": note.body}


def delete_note(note_id: int, user_id: int) -> None:
    """Удаляет заметку.

    Args:
        note_id (int): ID заметки.
        user_id (int): ID владельца (проверка прав).

    Raises:
        ValueError: Если заметка не найдена или не принадлежит пользователю.
    """
    with get_session() as session:
        note = session.query(Note).filter_by(id=note_id, user_id=user_id).first()
        if not note:
            raise ValueError("Заметка не найдена")
        session.delete(note)