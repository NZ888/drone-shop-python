from Project.db import DATA_BASE
from flask_login import UserMixin


class User(UserMixin, DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key= True)
    username = DATA_BASE.Column(DATA_BASE.String(50), nullable= False)
    email = DATA_BASE.Column(DATA_BASE.String(50), nullable=False)
    password = DATA_BASE.Column(DATA_BASE.String(35), nullable=False)
    isAdmin = DATA_BASE.Column(DATA_BASE.Boolean, default=False)