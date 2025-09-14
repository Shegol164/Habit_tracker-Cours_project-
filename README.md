# Трекер полезных привычек

[![CI/CD Pipeline](https://github.com/Shegol164/Habit_tracker-Cours_project-/actions/workflows/ci-cd.yml/badge.svg?branch=develop)](https://github.com/Shegol164/Habit_tracker-Cours_project-/actions/workflows/ci-cd.yml)

## Описание

Бэкенд-часть SPA веб-приложения для трекинга полезных привычек по методике Джеймса Клира ("Атомные привычки"). Позволяет пользователям создавать, управлять и получать напоминания о своих привычках через Telegram-бота.

## Адрес сервера

Приложение развернуто и доступно по адресу: **http://158.160.1.102**

*(Примечание: если Nginx настроен корректно и порт 80 открыт на сервере, приложение будет доступно по этому адресу. Если нет, API будет доступен напрямую через `http://158.160.1.102:8000`)*

## Локальный запуск

### Предварительные требования

- Установленный [Docker](https://docs.docker.com/get-docker/)
- Установленный [Docker Compose](https://docs.docker.com/compose/install/)

### Шаги запуска

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Shegol164/Habit_tracker-Cours_project-.git
    cd Habit_tracker-Cours_project-
    ```

2.  **Создайте файл `.env`:**
    Создайте файл `.env` в корне проекта и заполните его необходимыми переменными окружения. Пример содержимого:
    ```env
    SECRET_KEY=your-super-secret-key-change-this-in-production
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Database (PostgreSQL)
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=habit_tracker_db
    DB_USER=postgres
    DB_PASSWORD=your_strong_db_password
    DB_HOST=db
    DB_PORT=5432

    # Telegram Bot
    TELEGRAM_BOT_TOKEN=your_actual_telegram_bot_token
    TELEGRAM_BOT_USERNAME=your_bot_username

    # Celery (Redis)
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0

    # Frontend URL (для CORS)
    FRONTEND_URL=http://localhost:3000
    ```
    *Замените `your_...` на реальные значения.*

3.  **Запустите приложение с помощью Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    Эта команда соберет Docker-образы и запустит все сервисы, определенные в `docker-compose.yml` (Django, PostgreSQL, Redis, Celery Worker, Celery Beat, Nginx).

4.  **Выполните миграции и создайте суперпользователя (первый запуск):**
    В новом терминале, когда контейнеры запущены, выполните:
    ```bash
    # Выполнить миграции
    docker-compose exec web python manage.py migrate

    # Создать суперпользователя
    docker-compose exec web python manage.py createsuperuser
    ```
    Следуйте инструкциям в терминале для создания учетной записи администратора.

5.  **Доступ к приложению:**
    -   **API:** `http://localhost` (через Nginx) или `http://localhost:8000` (напрямую из контейнера `web`).
    -   **Django Admin:** `http://localhost/admin` или `http://localhost:8000/admin`.
    -   **Swagger UI (документация API):** `http://localhost/api/docs/` или `http://localhost:8000/api/docs/`.

## Настройка и запуск на удаленном сервере

### Предварительные требования

1.  **Сервер:**
    *   Сервер под управлением Ubuntu 20.04/22.04 или аналогичной Linux ОС.
    *   Открытые порты 22 (SSH), 80 (HTTP) и, при необходимости, 443 (HTTPS) в брандмауэре.
2.  **Пользователь на сервере:**
    *   Создайте пользователя (например, `deployer`) с правами `sudo`.
    *   Добавьте этого пользователя в группу `docker`: `sudo usermod -aG docker deployer`.
3.  **Docker и Docker Compose:**
    *   Установите Docker Engine и Docker Compose (или Docker Compose plugin) на сервер.
    *   Убедитесь, что Docker запущен и включен для автозапуска: `sudo systemctl status docker`, `sudo systemctl enable docker`.
4.  **SSH-ключи:**
    *   Сгенерируйте SSH-ключ для GitHub Actions (на вашей локальной машине или сервере).
    *   Добавьте **публичный** ключ в `~/.ssh/authorized_keys` пользователя `deployer` на сервере.
    *   Сохраните **приватный** ключ в надежном месте.

### Настройка CI/CD (GitHub Actions)

1.  **Подготовьте сервер:**
    *   Залогиньтесь на сервер под пользователем `deployer`.
    *   Клонируйте репозиторий в домашнюю директорию:
        ```bash
        cd ~
        git clone https://github.com/Shegol164/Habit_tracker-Cours_project-.git
        ```
        *Убедитесь, что имя папки после клонирования соответствует пути, указанному в скрипте GitHub Actions (`cd /home/deployer/Habit_tracker-Cours_project-`).*

2.  **Создайте `.env` на сервере:**
    *   Перейдите в директорию проекта:
        ```bash
        cd ~/Habit_tracker-Cours_project-
        ```
    *   Создайте файл `.env` и заполните его **реальными значениями переменных окружения** (как в локальном запуске, но с учетом production-настроек, например, `DEBUG=False`, `ALLOWED_HOSTS=ваш_ip_сервера`).
        ```bash
        nano .env
        # Вставьте содержимое, сохраните и закройте
        ```

3.  **Настройте Secrets в GitHub:**
    *   Перейдите в ваш репозиторий на GitHub: `Settings` -> `Secrets and variables` -> `Actions`.
    *   Добавьте следующие **Repository Secrets**:
        *   `SERVER_IP`: IP-адрес вашего сервера (например, `158.160.1.102`).
        *   `SERVER_USER`: Имя пользователя на сервере (например, `deployer`).
        *   `SSH_PRIVATE_KEY`: Содержимое **приватного** SSH-ключа, созданного ранее.

4.  **Проверьте файл workflow:**
    *   Убедитесь, что файл `.github/workflows/ci-cd.yml` существует и настроен правильно, особенно секция `on:` (например, `branches: [ "develop" ]`) и скрипт деплоя.

### Как работает автоматический деплой

Когда вы пушите изменения в ветку, на которую настроен CI/CD (например, `develop`), GitHub Actions автоматически:

1.  Запускает тесты и линтинг (если не отключены).
2.  Проверяет возможность сборки Docker-образов.
3.  Если предыдущие шаги успешны, подключается к вашему серверу по SSH.
4.  На сервере выполняет следующие команды:
    *   `cd /home/deployer/Habit_tracker-Cours_project-` (переход в директорию проекта).
    *   `git pull origin develop` (обновление кода из репозитория).
    *   `docker-compose -p habit_tracker down` (остановка старых контейнеров).
    *   `docker-compose -p habit_tracker up -d --build` (пересборка и запуск новых контейнеров с именем проекта `habit_tracker`).

## Структура проекта

- `config/`: Основной Django-проект.
- `users/`: Приложение для управления пользователями.
- `habits/`: Приложение для управления привычками.
- `notifications/`: Приложение для интеграции с Telegram и Celery-задачами.
- `nginx/`: Конфигурация Nginx.
- `Dockerfile`: Инструкции для сборки Docker-образа Django-приложения.
- `docker-compose.yml`: Файл для оркестрации всех сервисов.
- `requirements.txt`: Зависимости Python.
- `.env`: (Не коммитится) Файл с переменными окружения.
- `.github/workflows/ci-cd.yml`: Конфигурация CI/CD пайплайна.

## Используемые технологии

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Message Broker/Cache:** Redis
- **Task Queue:** Celery
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Docker Compose on Ubuntu Server
- **Messaging:** Telegram Bot API