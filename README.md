# Torrent Searcher Bot

Asynchronous telegram bot for tracking movie release.

## How to run

```bash
TELEGRAM_API_TOKEN="yout token"
pip install requirements.txt
python3 runner.py
```

## What's done

- [lesson 3](#lesson-3)
- [lesson 4](#lesson-4)

## Lesson 3

- Создан скелет приложения:
  - интерфесы для всех классов приложения
  - запуск телеграм бота
  - скелет классов для БД (создано при помощи фабрики)
- В интерфесах сделаны небольшие изменения
- Обновлена uml схема

## Lesson 4

- Создан бэкэнд для хранения пользователей и фильмов с помощью базы данных mongo и библиотеки motor
- Реализованы команды в телеграм и их обработка
  - активация\деактивация пользователя
  - список активных запросов
  - добавление\удаление запросов
- Поправлены интерфейсы