from .urls import *
from .settings import project

# add registration blueprint
project.register_blueprint(blueprint= user.user)
project.register_blueprint(blueprint= home.home)