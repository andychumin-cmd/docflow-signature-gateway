# DocFlow Signature Gateway

Система проверки ЭЦП на потоке документов (входящая/исходящая корреспонденция).
- Хранение открытых ключей сотрудников в БД (SQLite/PostgreSQL)
- Проверка отсоединённых подписей GPG (отклонение неверных/отсутствующих)
- Журнал проверок (status: valid / invalid / missing_sig / unknown_key)
- API: POST /check — проверка пары документ+подпись, GET /report — отчёт

Запуск: pip install -r requirements.txt && uvicorn app:app --port 8000
