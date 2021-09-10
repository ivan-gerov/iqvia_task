
import datetime
from random import choice, randint

from celery import Celery

from main import app
from models import Contact, ContactSchema


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(
    broker_url="redis://localhost:6379", result_backend="redis://localhost:6379"
)
celery = make_celery(app)


@celery.task(name="task.create_random_contact")
def create_random_contact():
    names = [
        ("Ivan", "Gerov"),
        ("Baki", "Hamna"),
        ("Homer", "Simpson"),
        ("Billy", "Bob"),
    ]
    contact_choice = choice(names)
    new_contact = {
        "username": f"{contact_choice[0]}_{contact_choice[1]}{randint(0, 1000)}",
        "first_name": contact_choice[0],
        "last_name": contact_choice[1],
    }
    contact_schema = ContactSchema()
    contact = contact_schema.load(new_contact).create()
    print(contact_schema.dump(contact))
    since = datetime.datetime.now() - datetime.timedelta(minutes=1)
    contacts = Contact.query.filter(Contact.created_at > since).all()
    if contacts:
        print(contacts)


@celery.task(name="task.remove_older_than_1_min")
def remove_old_contact():
    since = datetime.datetime.now() - datetime.timedelta(minutes=1)
    Contact.query.filter(Contact.created_at > since)
    import pdb; pdb.set_trace()


celery.conf.beat_schedule = {
    "create-contact-15-seconds": {
        "task": "task.create_random_contact",
        "schedule": 15.0,
    },
}
