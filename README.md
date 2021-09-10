# IQVIA Task
**What you need to run the main app:**
* Activate virtual env and export the env variable for the Flask app - `export FLASK_APP=app/main:app`

**What you need to run the Celery tasks:**
* A running redis server on `localhost:6379`
* Open another terminal, activate the virtual env and enter the app folder.
* Run `celery -A tasks.celery worker -B`

**Endpoints**
```
Endpoint                     Methods  Rule
---------------------------  -------  ---------------------------------
api.create_contact           POST     /api/v1/contact
api.get_contact_by_id        GET      /api/v1/contact/<int:id>
api.get_contact_by_username  GET      /api/v1/contact/<string:username>
api.list_contacts            GET      /api/v1/contact
api.remove_contact_by_id     DELETE   /api/v1/contact/<id>
api.update_contact_by_id     PUT      /api/v1/contact/<id>
```