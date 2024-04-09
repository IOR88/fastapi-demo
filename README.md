## Docker-Compose

In order to run locally the whole stack, we will use docker-compose
```bash
docker-compose -f docker-compose.yaml --env-file .env.docker up
```

## Local Development
For local development, comment fastapi and celery services and leave only postgresql.
After run only fastapi with uvicorn
```bash
pipenv run uvicorn app.main:app --reload
```

and celery
```bash
pipenv run celery -A app.tasks worker -l INFO
```
-A app.tasks worker -l info

In order to apply migrations run alembic
```bash
alembic upgrade head
```

In production mode when using for example Kubernetes remember to define
1. Resources requests and limits which specify how much cpu and memory is 
allocated to container.
2. Use security context to allow read access only to system files, as well
specify group id and user id to avoid granting root access for container user
which is root by default if not defined.