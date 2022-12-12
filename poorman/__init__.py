from flask import Flask
from poorman.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate(app, db, compare_type=True)

    from poorman.main.routes import main
    from poorman.candidates.routes import candidates
    app.register_blueprint(main)
    app.register_blueprint(candidates)

    return app