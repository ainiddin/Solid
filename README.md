# inVision U — AI Candidate Screening System

Система автоматизированного скрининга кандидатов для программы inVision U (inDrive) с использованием искусственного интеллекта. Система оценивает кандидатов по 4 измерениям, объясняет каждый балл и определяет использование ИИ в эссе.

## 🌐 Демо

- **Frontend:** https://ainiddin.github.io/Solid/frontend/#apply
- **Backend API:** https://ainiddin.pythonanywhere.com/candidates
- **API Документация:** https://ainiddin.pythonanywhere.com/docs

---

## 🧠 Как работает система
Кандидат заполняет форму (Frontend)
↓ POST /candidates
Backend (FastAPI) сохраняет в SQLite
↓ POST /score/{id}
Groq API (LLaMA 3.3 70b) анализирует данные
↓ Возвращает JSON с баллами + объяснениями
Dashboard — комиссия видит результаты и принимает решение

### Что оценивает система:

| Измерение | Вес | Что анализируется |
|---|---|---|
| Skills & Experience | 25% | Академический и технический бэкграунд |
| Motivation & Values | 25% | Ясность цели и ценности |
| Leadership Potential | 30% | Реальные лидерские сигналы |
| Growth Trajectory | 20% | Траектория развития и mindset |

### Explainable AI:
Каждый балл сопровождается:
- 📌 **Evidence** — прямая цитата из анкеты
- 💬 **What would improve** — что подняло бы оценку
- 🧠 **Overall reasoning** — общая логика решения
- 🎤 **Interview questions** — вопросы для комиссии

---

## 🛠 Технологический стек

- **Backend:** Python 3.11, FastAPI, Uvicorn
- **AI:** Groq API (LLaMA 3.3 70b)
- **AI Detector:** Определяет написано ли эссе человеком или ИИ
- **Database:** SQLite через aiosqlite
- **Frontend:** HTML / CSS / JavaScript (без фреймворков)
- **Деплой:** PythonAnywhere (backend) + GitHub Pages (frontend)
- **Контейнеризация:** Docker, Docker Compose

---

## 📁 Структура проекта
invision-ai/
├── backend/
│ ├── main.py # FastAPI приложение + CORS
│ ├── models.py # Pydantic схемы
│ ├── scorer.py # Логика скоринга через Groq API
│ ├── ai_detector.py # Детектор AI-текста в эссе
│ ├── database.py # SQLite через aiosqlite
│ └── routes/
│ ├── candidates.py # POST/GET /candidates
│ └── score.py # POST /score/{id}
├── frontend/
│ └── index.html # SPA: Apply / Dashboard / Candidate Card
├── .env # API ключи (не публикуется)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

---

## 🚀 Запуск локально через Docker

Самый простой способ — нужен только [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Шаг 1 — Клонировать репозиторий
```bash
git clone https://github.com/ainiddin/Solid.git
cd Solid
```

### Шаг 2 — Создать .env файл
Создай файл `.env` в корне проекта:
OPENAI_API_KEY=gsk_твойgroqключ
> Groq ключ получи бесплатно на **console.groq.com**

### Шаг 3 — Запустить
```bash
docker-compose up -d --build
```

### Шаг 4 — Открыть
- 🖥️ **Сайт:** открой файл `frontend/index.html` в браузере
- ⚙️ **API:** `http://localhost:8000`
- 📖 **Swagger docs:** `http://localhost:8000/docs`

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
# Остановить
docker-compose stop

# Выключить и удалить контейнеры
docker-compose down

# Посмотреть логи
docker-compose logs -f
```

---

## ⚠️ Этические принципы

- AI-оценка **advisory only** — финальное решение принимает комиссия (human-in-the-loop)
- Демографические данные **не используются** как сигнал оценки
- PII данные хранятся локально и не передаются третьим сторонам кроме Groq API
