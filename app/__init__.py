from flask import Flask
from config import config_by_name
from app.routers.questions import questions_bp
from app.routers.responses import responses_bp
from app.routers.categories import categories_bp
from app.models import db
from flask_migrate import Migrate
import os

def create_app(config_name=None):

    if config_name is None:

        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db) 

    app.register_blueprint(questions_bp)
    app.register_blueprint(responses_bp)
    app.register_blueprint(categories_bp)

    return app



