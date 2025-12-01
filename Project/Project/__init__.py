from .urls import *
from .settings import project
from .loadenv import init_db
# add registration blueprint
project.register_blueprint(blueprint= user.user)
project.register_blueprint(blueprint= home.home)