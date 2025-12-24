# **Presentation Validator - Документация проекта**

## Описание проекта

HTTP API на Python для валидации структуры и формата PowerPoint презентаций.
Система обнаруживает типичные ошибки: списки из одного пункта, разнобой в шрифтах, слишком много текста на слайде.
В будущем планируется расширение на ML-проверки для более сложных ошибок.

**Команда**: 2 человека
**Технологии**: Python, FastAPI, SQLAlchemy (async), Docker, pytest, python-pptx

---

### Что будет видеть пользователь

* Web-страница с формой загрузки `.pptx` файла

* Кнопка «Проверить презентацию»

* JSON-ответ с детализированным отчетом об ошибках

* Список найденных ошибок на странице

* Таблица с историей предыдущих проверок

* REST API endpoints:

  * **POST /validate** — загрузка презентации и запуск проверки
  * **GET /validations** — список всех проверок
  * **GET /validations/{id}** — детали конкретной проверки

---

### Распределение задач

#### Участник 1

* FastAPI приложение и endpoints
* Docker контейнеризация
* Database модели и миграции
* Интеграционное тестирование

#### Участник 2

* Парсинг PPTX файлов
* Реализация правил валидации
* ML компоненты для сложных проверок (будет позже)
* Модульное тестирование валидаторов

---

### План разработки

#### Неделя 1: Базовая инфраструктура

* Настройка проекта и окружения
* Базовый парсер PPTX (`parse_presentation`)
* Схема БД и дизайн API

#### Неделя 2: Ядро валидации

* Реализация основных правил проверки (single bullet, font inconsistency, text overflow)
* FastAPI endpoints и веб-страница

#### Неделя 3: ML компонент и тестирование

* ML модели для сложных проверок (планируется)
* Тестирование и bug fixing
* Документация и деплой

---

## Архитектура системы

### Компоненты системы

```mermaid
graph TB
    A[Клиент / Веб] --> B[HTTP API]
    B --> C[Validation Service]
    C --> D[PPTX Parser]
    C --> E[Rule Engine]
    E --> F[Style & Text Validator]
    E --> G[Structure Validator]
    C --> H["Database (Validation / Issue)"]
```

---

### Диаграмма последовательности

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant V as Validator
    participant P as PPTX Parser
    participant R as Rule Engine
    
    C->>A: POST /validate
    A->>V: validate_presentation(file)
    V->>P: parse_presentation(file)
    P-->>V: slides_data
    V->>R: apply_rules(slides_data)
    R-->>V: validation_results
    V-->>A: validation_report
    A-->>C: JSON response
```

---

### Схема базы данных

```mermaid
erDiagram
    VALIDATION ||--o{ ISSUE : contains
    VALIDATION {
        int id PK
        string filename
        timestamp created_at
    }
    ISSUE {
        int id PK
        int validation_id FK
        string rule
        string message
        int slide_number
    }
```

---

### Принципы архитектуры

* **SOLID**: разделение ответственности между сервисами (API, валидаторы, парсер, БД)
* **DRY**: переиспользование кода через базовые классы и функции
* **Strategy Pattern**: разные правила валидации подключаются динамически
* **Repository Pattern**: работа с базой через SQLAlchemy async
* **Минимум глобального состояния**, все сервисы асинхронные

