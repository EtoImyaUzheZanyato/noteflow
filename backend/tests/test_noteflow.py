"""Автотесты для NoteFlow (pytest)."""
import os
import pytest

# Удаляем БД перед тестами
if os.path.exists("noteflow.db"):
    os.remove("noteflow.db")

from src.noteflow.db import init_db, get_session, engine
from src.noteflow.models import User
from src.noteflow.auth import register, login, verify_token
from src.noteflow.notes import create_note, get_notes, update_note, delete_note
from src.noteflow.search import search
from src.noteflow.export import export_to_markdown


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """Инициализирует БД перед тестами и удаляет после."""
    init_db()
    yield
    engine.dispose()  # закрываем соединения
    if os.path.exists("noteflow.db"):
        os.remove("noteflow.db")


@pytest.fixture
def user():
    """Создаёт или возвращает тестового пользователя."""
    try:
        return register("test@example.com", "secret123")
    except ValueError:
        with get_session() as session:
            u = session.query(User).filter_by(email="test@example.com").first()
            return {"id": u.id, "email": u.email}


def test_register_success():
    """TC-01: успешная регистрация."""
    user = register("new@example.com", "secret123")
    assert user["email"] == "new@example.com"
    assert "id" in user


def test_register_duplicate(user):
    """TC-02: повторная регистрация с тем же email."""
    with pytest.raises(ValueError, match="Email уже занят"):
        register("test@example.com", "secret123")


def test_register_short_password():
    """TC-03: пароль короче 6 символов."""
    with pytest.raises(ValueError, match="минимум 6 символов"):
        register("short@example.com", "123")


def test_login_success(user):
    """TC-04: успешный вход."""
    token = login("test@example.com", "secret123")
    assert token.count(".") == 2
    payload = verify_token(token)
    assert payload["email"] == "test@example.com"


def test_login_wrong_password(user):
    """TC-05: неверный пароль."""
    with pytest.raises(ValueError, match="Неверный email или пароль"):
        login("test@example.com", "wrong")


def test_create_note(user):
    """TC-06: создание заметки."""
    note = create_note(user["id"], "Тест", "Тело")
    assert note["title"] == "Тест"
    assert note["body"] == "Тело"


def test_create_note_empty_title(user):
    """TC-07: пустой заголовок."""
    with pytest.raises(ValueError, match="Заголовок не может быть пустым"):
        create_note(user["id"], "", "Тело")


def test_search(user):
    """TC-08: поиск по кириллице."""
    create_note(user["id"], "Список покупок", "- хлеб")
    results = search(user["id"], "покуп")
    assert len(results) >= 1
    assert "покуп" in results[0]["title"].lower()


def test_update_note(user):
    """TC-09: обновление заметки."""
    note = create_note(user["id"], "Старое", "Старое тело")
    updated = update_note(note["id"], user["id"], "Новое", "Новое тело")
    assert updated["title"] == "Новое"


def test_delete_note(user):
    """TC-10: удаление заметки."""
    note = create_note(user["id"], "Удалить", "")
    delete_note(note["id"], user["id"])
    assert all(n["id"] != note["id"] for n in get_notes(user["id"]))


def test_export_markdown(user):
    """Экспорт в Markdown."""
    note = create_note(user["id"], "Экспорт", "Тело")
    md = export_to_markdown(note["id"], user["id"])
    assert md.startswith("# Экспорт")