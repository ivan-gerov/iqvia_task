
from flask import Flask
from flask_migrate import Migrate # For migrations, which I didn't have enough time 
                                  # to figure out how to implement with this setup

import config
from models import db
from api import api

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(api)

with app.app_context():
    db.init_app(app)
    db.create_all(app=app)



