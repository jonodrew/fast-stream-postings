from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from redis import StrictRedis
from flask_redis import FlaskRedis

db = SQLAlchemy()
migrate = Migrate()
redis = StrictRedis(host='redis', port=6379, charset="utf-8", decode_responses=True)


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    app.config['ASSETS_DEBUG'] = True

    """these are blueprints - a way of making a Flask application more modular and re-usable"""
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.submit import bp as submit_bp
    app.register_blueprint(submit_bp, url_prefix='/submit')


    return app


from app import models
