import secrets

import flask_login

from .settings import project
from user.models import User

project.secret_key = project.secret_key or secrets.token_hex()

login_manager = flask_login.LoginManager(app=project)
login_manager.login_view = "user.render_login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)