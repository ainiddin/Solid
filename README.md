# inVision U — AI-система скрининга кандидатов

AI-система автоматического отбора кандидатов для программы inVision U (inDrive).
Оценивает кандидатов по 4 измерениям, объясняет каждый балл и определяет, написано ли эссе человеком или ИИ.

## 🌐 Демо

- **Сайт:** [https://ainiddin.pythonanywhere.com](https://ainiddin.pythonanywhere.com)
- **API:** [https://ainiddin.pythonanywhere.com/candidates](https://ainiddin.pythonanywhere.com/candidates)
- **Документация:** [https://ainiddin.pythonanywhere.com/docs](https://ainiddin.pythonanywhere.com/docs)

---

## 🧠 Как работает система

1. Кандидат заполняет форму заявки на сайте
2. Backend сохраняет данные в SQLite через `POST /candidates`
3. `POST /score/{id}` отправляет данные в Groq API (LLaMA 3.3 70b)
4. ИИ возвращает баллы + объяснения + вопросы для интервью
5. Комиссия видит результаты на Dashboard и принимает решение

### Критерии оценки

| Измерение | Вес | Что анализируется |
|---|---|---|
| Skills & Experience | 25% | Академический и технический бэкграунд |
| Motivation & Values | 25% | Ясность цели и ценности кандидата |
| Leadership Potential | 30% | Реальные лидерские сигналы |
| Growth Trajectory | 20% | Траектория роста и mindset |

### Explainable AI — прозрачность оценки

Каждый балл сопровождается:
- 📌 **Evidence** — прямая цитата из анкеты кандидата
- 💬 **What would improve** — что подняло бы оценку
- 🧠 **Overall reasoning** — общая логика решения
- 🎤 **Interview questions** — вопросы для комиссии

---

## 🛠 Технологический стек

- **Backend:** Python 3.11, FastAPI, Uvicorn
- **AI:** Groq API (LLaMA 3.3 70b)
- **AI Детектор:** определяет, написано ли эссе человеком или ИИ
- **База данных:** SQLite через aiosqlite
- **Frontend:** Vanilla HTML / CSS / JavaScript (без фреймворков)
- **Деплой:** PythonAnywhere
- **Контейнеризация:** Docker, Docker Compose

---

## 📁 Структура проекта
invision-ai/
├── backend/
│ ├── main.py # FastAPI приложение + CORS
│ ├── models.py # Pydantic схемы
│ ├── scorer.py # Логика скоринга через Groq API
│ ├── ai_detector.py # Детектор AI-текста
│ ├── database.py # SQLite через aiosqlite
│ └── routes/
│ ├── candidates.py # POST/GET /candidates
│ └── score.py # POST /score/{id}
├── frontend/
│ └── index.html # SPA: Apply / Dashboard / Карточка кандидата
├── .env # API ключи (не публикуется)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

---

## 🚀 Запуск локально через Docker

### Шаг 1 — Клонировать репозиторий
```bash
git clone https://github.com/ainiddin/Solid.git
cd Solid
```
OPENAI_API_KEY=gsk_твойgroqключ

> Groq ключ — бесплатно на **console.groq.com**

### Шаг 3 — Запустить
```bash
docker-compose up -d --build
```

### Шаг 4 — Открыть
- 🖥️ **Сайт:** открой `frontend/index.html` в браузере
- ⚙️ **API:** `http://localhost:8000`
- 📖 **Docs:** `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Метод | Путь | Описание |
|---|---|---|
| POST | `/candidates` | Добавить кандидата |
| GET | `/candidates` | Список всех кандидатов |
| GET | `/candidate/{id}` | Карточка кандидата |
| POST | `/score/{id}` | Запустить AI-скоринг |
| PATCH | `/candidate/{id}/status` | Shortlist / Reject |

---

## 🛑 Полезные команды

```bash
docker-compose stop       # Остановить
docker-compose down       # Остановить и удалить контейнеры
docker-compose logs -f    # Посмотреть логи
```

---

## ⚠️ Этические принципы

- AI-оценка **носит рекомендательный характер** — финальное решение принимает комиссия
- Демографические данные **не используются** как сигнал оценки
- Личные данные хранятся локально и не передаются третьим сторонам, кроме Groq API

### Шаг 2 — Создать .env файл
OPENAI_API_KEY=gsk_твойgroqключOPENAI_API_KEY=gsk_твойgroqключOPENAI_API_KEY=gsk_твойgroqключ
