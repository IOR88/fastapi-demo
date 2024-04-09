import os
from celery import Celery
from app import settings
from app.followers.crud import stats
from app.followers import schema
from app.users.crud import get_all_users
from app.database import sessionmanager

app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", settings.CELERY_BROKER_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60*5, stats)


@app.task()
async def stats(task_type):
    with sessionmanager.session() as session:
        users = await get_all_users(session)
        for user in users:
            results = await stats(session, schema.User(id=user.id))
            print(results)
