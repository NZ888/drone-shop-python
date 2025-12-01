import flask
from Project.db import DATA_BASE
from .models import User
from Project.config_page import config_page
import flask_login


def render_login():
    if flask.request.method == "POST":
        name = flask.request.form["username"]
        password = flask.request.form["password"]
        users = User.query.all()
        for user in users:
            if user.username == name and user.password == password:
                flask_login.login_user(user)
    if not flask_login.current_user.is_authenticated:
        return flask.render_template("login.html")
    else:
        return flask.redirect("/")    


@config_page("register.html")
def render_register():
    message = ""
    if flask.request.method == 'POST':
        name = flask.request.form["username"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        confirm_password = flask.request.form["confirm_password"]

        user_email = User.query.filter_by(email= email).first()
        if user_email is None :
            if password == confirm_password:
                user = User(
                    username = name,
                    email = email,
                    password = password
                )
                DATA_BASE.session.add(user)
                DATA_BASE.session.commit()
                message = "Успішно"
            else:
                message = "Паролі не співпадають"
        else:
            message = "Такий користувач вже існує"


    return {"message": message}

def logout():
    flask.session.clear()
    return flask.redirect("/")