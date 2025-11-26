# Развертывание на Northflank

Это руководство поможет вам развернуть LLM Council на платформе Northflank.

## Предварительные требования

1. Аккаунт на [Northflank](https://northflank.com)
2. API ключ OpenRouter (получите на [openrouter.ai](https://openrouter.ai/))
3. Git репозиторий с вашим кодом (GitHub, GitLab, или Bitbucket)

## Шаг 1: Подготовка репозитория

Убедитесь, что ваш код находится в Git репозитории и доступен для Northflank.

## Шаг 2: Создание проекта на Northflank

1. Войдите в ваш аккаунт Northflank
2. Создайте новый проект
3. Подключите ваш Git репозиторий

## Шаг 3: Настройка переменных окружения

В настройках проекта добавьте следующие переменные окружения:

- `OPENROUTER_API_KEY` - ваш API ключ OpenRouter (обязательно)
- `BACKEND_URL` - URL бэкенда (будет автоматически установлен после развертывания бэкенда)

## Шаг 4: Развертывание сервисов

### Вариант 1: Использование northflank.yaml (Рекомендуется)

1. Northflank автоматически обнаружит файл `northflank.yaml` в корне репозитория
2. Нажмите "Deploy" для развертывания обоих сервисов

### Вариант 2: Ручная настройка через веб-интерфейс

#### Backend сервис:

1. Создайте новый сервис типа "Service"
2. Настройки сборки:
   - **Build Type**: Dockerfile
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Context**: `.` (корень проекта)
3. Порт: `8001`
4. Переменные окружения:
   - `OPENROUTER_API_KEY` = ваш API ключ
5. Volumes:
   - Создайте volume `data` размером 10GB
   - Mount path: `/app/data`
6. Ресурсы:
   - CPU: 1000m (1 core)
   - Memory: 2Gi
7. Healthcheck:
   - Path: `/`
   - Port: `8001`
   - Interval: 30s
   - Timeout: 10s

#### Frontend сервис:

1. Создайте новый сервис типа "Service"
2. Настройки сборки:
   - **Build Type**: Dockerfile
   - **Dockerfile Path**: `frontend/Dockerfile.prod`
   - **Context**: `./frontend`
3. Build Arguments:
   - `VITE_API_URL` = URL вашего бэкенда (например, `https://llm-council-backend.your-project.northflank.app`)
4. Порт: `80`
5. Переменные окружения:
   - `VITE_API_URL` = URL вашего бэкенда
6. Ресурсы:
   - CPU: 500m (0.5 core)
   - Memory: 512Mi
7. Зависимости: выберите backend сервис

## Шаг 5: Получение URL бэкенда

После развертывания бэкенда:

1. Перейдите в настройки backend сервиса
2. Скопируйте публичный URL (например, `https://llm-council-backend.your-project.northflank.app`)
3. Обновите переменную окружения `BACKEND_URL` в frontend сервисе
4. Пересоберите frontend сервис с новым значением `VITE_API_URL`

## Шаг 6: Настройка CORS (если необходимо)

Если вы используете кастомный домен, обновите `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-frontend-domain.com",  # Добавьте ваш домен
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Шаг 7: Проверка развертывания

1. Откройте URL вашего frontend сервиса
2. Создайте новую беседу
3. Отправьте тестовое сообщение
4. Убедитесь, что все этапы (Stage 1, 2, 3) работают корректно

## Обновление приложения

При каждом push в основную ветку репозитория, Northflank автоматически пересоберет и переразвернет сервисы (если включен auto-deploy).

Для ручного обновления:
1. Перейдите в настройки сервиса
2. Нажмите "Redeploy"

## Мониторинг и логи

- **Логи**: Доступны в разделе "Logs" каждого сервиса
- **Метрики**: CPU и память отображаются на дашборде сервиса
- **Healthcheck**: Статус здоровья сервиса отображается на главной странице

## Устранение неполадок

### Backend не запускается

- Проверьте, что переменная `OPENROUTER_API_KEY` установлена
- Проверьте логи сервиса
- Убедитесь, что volume `data` создан и подключен

### Frontend не может подключиться к Backend

- Проверьте, что `VITE_API_URL` установлен правильно
- Убедитесь, что backend сервис запущен и доступен
- Проверьте настройки CORS в backend

### Ошибки сборки

- Проверьте логи сборки в разделе "Build Logs"
- Убедитесь, что все файлы присутствуют в репозитории
- Проверьте, что пути к Dockerfile указаны правильно

## Дополнительные ресурсы

- [Документация Northflank](https://docs.northflank.com)
- [OpenRouter API](https://openrouter.ai/docs)

