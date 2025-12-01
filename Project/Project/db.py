from .settings import * 
import flask_migrate 
import flask_sqlalchemy

project.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
DATA_BASE = flask_sqlalchemy.SQLAlchemy(project)
migrations_path = os.path.abspath(os.path.join(__file__, '..', 'migrations'))
MIGRATE = flask_migrate.Migrate(app = project, db = DATA_BASE, directory = migrations_path)



project.app_context().push()


