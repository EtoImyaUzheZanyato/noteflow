\# NoteFlow



Веб-сервис для заметок с поддержкой тегов, поиска и экспорта в Markdown.



\## Возможности



\- Регистрация и вход (JWT)

\- Создание, редактирование, удаление заметок

\- Полнотекстовый поиск по заголовку и телу

\- Теги и папки (в разработке)

\- Экспорт заметок в Markdown



\## Стек



\- Python 3.10

\- SQLAlchemy + SQLite

\- PyJWT

\- Sphinx (документация)



\## Установка



```bash

git clone https://github.com/EtoImyaUzheZanyato/noteflow.git

cd noteflow/backend

python -m venv .venv

source .venv/Scripts/activate   # Windows: .venv\\Scripts\\activate.bat

pip install -r requirements.txt

## Запуск

```bash
cd backend
python -c "from src.noteflow.db import init_db; init_db()"
python test_run.py
```

## Примеры использования

```python
from src.noteflow.db import init_db
from src.noteflow.auth import register, login
from src.noteflow.notes import create_note, get_notes
from src.noteflow.search import search

init_db()

# 1. Регистрация
user = register("student@example.com", "secret123")

# 2. Вход
token = login("student@example.com", "secret123")

# 3. Создание заметки
note = create_note(user["id"], "Список покупок", "- хлеб\n- молоко")

# 4. Поиск
results = search(user["id"], "покуп")
print(results)
```

## Документация

Сгенерированная HTML-документация: [`docs/_build/html/index.html`](docs/_build/html/index.html)

Сгенерировать заново:

```bash
cd docs
make.bat html      # Windows
make html          # Linux/macOS
```

## Структура проекта

```
noteflow/
├── backend/
│   ├── src/noteflow/       # исходный код
│   ├── tests/              # тесты (в разработке)
│   ├── test_run.py         # демонстрационный скрипт
│   └── requirements.txt
├── docs/                   # Sphinx-документация
│   └── _build/html/        # сгенерированная HTML-документация
├── .gitignore
└── README.md
```

## Лицензия

Учебный проект. Свободное использование в образовательных целях.