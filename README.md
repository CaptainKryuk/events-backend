# events-backend

# Требования
- Наличие docker
- python 3.10+
- Получить .env файл. Запросить у тг @akryuk

# Запуск
В Makefile содержится набор команд по управлению проектом (обновляется)
Порядок запуска:
- make build - создаст image билда, который будет использоваться в docker-compose
- make up - запуск всех контейнеров
- poetry shell
- pre-commit install - установка линтера ruff перед запуском git commit ...
- make down - удаляет все контейнеры (данные остаются)
