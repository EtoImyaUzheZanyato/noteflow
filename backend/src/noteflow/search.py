"""Модуль поиска заметок.

Реализует полнотекстовый поиск по заголовку и телу заметки.
"""

from .db import get_session
from .models import Note


def search(user_id: int, query: str) -> list[dict]:
    """Ищет заметки пользователя по ключевому слову.

    Поиск выполняется по заголовку и телу, регистронезависимо.
    Фильтрация выполняется на стороне Python, так как SQLite
    не поддерживает регистронезависимый поиск для кириллицы.

    Args:
        user_id (int): ID пользователя.
        query (str): Поисковый запрос.

    Returns:
        list[dict]: Список найденных заметок.

    Examples:
        >>> results = search(1, "покупк")
        >>> isinstance(results, list)
        True
    """
    q = query.lower()
    with get_session() as session:
        notes = session.query(Note).filter(Note.user_id == user_id).all()
        found = [
            n for n in notes
            if q in n.title.lower() or q in (n.body or "").lower()
        ]
        return [{"id": n.id, "title": n.title, "body": n.body} for n in found]