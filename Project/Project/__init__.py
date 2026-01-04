from .settings import project
from .urls import *
from .loadenv import init_db
from .loginmanager import login_manager

project.register_blueprint(blueprint=user.user)
project.register_blueprint(blueprint=home.home)