import flask_sqlalchemy, flask_migrate
from .settings import project
import os


project.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
project.app_context().push()

DATA_BASE = flask_sqlalchemy.SQLAlchemy(project)
MIGARTE = flask_migrate.Migrate(
    app= project,
    db= DATA_BASE,
    directory= os.path.abspath(os.path.join(__file__, "..", "migrations"))
)
