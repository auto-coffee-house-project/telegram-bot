# Инструкция по запуску

### Создание виртуального окружения

```shell
poetry env use python3.11
```

### Активация виртуального окружения

```shell
poetry shell
```

### Установка зависимостей

```shell
poetry install
```

### Создание конфигурационного файла

```shell
cp config.example.toml config.toml
```

### Конфигурация

Впишите данные перед запуском в файл [config.toml](./config.toml):

- `api_base_url` - URL API сервиса
- `web_app_url` - URL web-приложения которое будет запускаться в боте

### Запуск

```shell
python3.11 src/main.py
```