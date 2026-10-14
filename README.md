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

