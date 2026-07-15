## Project Start command
uvicorn app.main:app --reload

## Way to migrate db
alembic upgrade head
alembic revision --autogenerate -m "syncing"
alembic upgrade head

## way to run docker
#up
docker compose -f docker-compose-dev.yml up -d

#down
docker compose -f docker-compose-dev.yml down