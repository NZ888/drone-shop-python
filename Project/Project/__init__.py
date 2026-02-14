from .urls import *
from .settings import *
from .db import*
from .loadenv import execute
from user.models import User
from catalog.models import Product
# add registration blueprint
from .config_page import config_page
from .loginmanager import *
import cart

project.register_blueprint(blueprint= user.user)
project.register_blueprint(blueprint= home.home)
project.register_blueprint(blueprint= catalog.catalog)
project.register_blueprint(blueprint= cart.cart)