"""Тестовый запуск NoteFlow."""
import os

# Удаляем старую БД, если есть
if os.path.exists("noteflow.db"):
    os.remove("noteflow.db")
    print("[OK] Старая БД удалена")

from src.noteflow.db import init_db
from src.noteflow.auth import register, login, verify_token
from src.noteflow.notes import create_note, get_notes, update_note, delete_note
from src.noteflow.search import search
from src.noteflow.export import export_to_markdown

# 1. Инициализация БД
init_db()
print("[OK] БД инициализирована")

# 2. Регистрация
user = register("student@example.com", "secret123")
print(f"[OK] Пользователь: {user}")

# 3. Вход
token = login("student@example.com", "secret123")
print(f"[OK] Токен: {token[:30]}...")

# 4. Проверка токена
payload = verify_token(token)
print(f"[OK] Payload: {payload}")

# 5. Создание заметки
note = create_note(user["id"], "Список покупок", "- хлеб\n- молоко")
print(f"[OK] Заметка: {note}")

# 6. Поиск
results = search(user["id"], "покуп")
print(f"[OK] Поиск: {results}")

# 7. Экспорт
md = export_to_markdown(note["id"], user["id"])
print(f"[OK] Markdown:\n{md}")

# 8. Обновление
updated = update_note(note["id"], user["id"], "Список покупок v2", "- хлеб\n- молоко\n- сыр")
print(f"[OK] Обновлено: {updated}")

# 9. Список заметок
all_notes = get_notes(user["id"])
print(f"[OK] Всего заметок: {len(all_notes)}")

# 10. Удаление
delete_note(note["id"], user["id"])
print("[OK] Заметка удалена")