import flask_login
from .settings import project
import secrets
from user.models import User


project.secret_key = secrets.token_hex()

login_manager = flask_login.LoginManager(app= project)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

