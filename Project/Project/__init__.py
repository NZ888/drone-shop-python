from .urls import *
from .settings import project
from .db import*
from .loadenv import execute
from user.models import User
# add registration blueprint
from .config_page import config_page
from .loginmanager import *

project.register_blueprint(blueprint= user.user)
project.register_blueprint(blueprint= home.home)
