"""Модуль экспорта заметок.

Поддерживает экспорт в Markdown.
"""

from .db import get_session
from .models import Note


def export_to_markdown(note_id: int, user_id: int) -> str:
    """Экспортирует заметку в формат Markdown.

    Args:
        note_id (int): ID заметки.
        user_id (int): ID владельца (проверка прав).

    Returns:
        str: Содержимое заметки в формате Markdown.

    Raises:
        ValueError: Если заметка не найдена.

    Examples:
        >>> md = export_to_markdown(1, 1)
        >>> md.startswith("#")
        True
    """
    with get_session() as session:
        note = session.query(Note).filter_by(id=note_id, user_id=user_id).first()
        if not note:
            raise ValueError("Заметка не найдена")
        return f"# {note.title}\n\n{note.body}\n"