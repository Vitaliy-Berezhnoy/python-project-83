#!/usr/bin/env bash
# скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Автоматическое определение параметров
if [ -z "$DATABASE_URL" ]; then
  export DATABASE_URL="postgresql://postgres:postgres@db:5432/postgres"
fi

# Ожидание готовности PostgreSQL
for _ in {1..5}; do
  if pg_isready -d "$DATABASE_URL"; then
    break
  fi
  sleep 2
done

make install && psql -a -d $DATABASE_URL -f database.sql