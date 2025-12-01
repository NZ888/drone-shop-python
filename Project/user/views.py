import flask
from Project.db import DATA_BASE
from .models import User
from Project.configure import config_page
def render_login():
    return flask.render_template(
        template_name_or_list= "login.html"
    )

@config_page("register.html")
def render_register():
    message = ""
    if flask.request.method == 'POST':
        name = flask.request.form["username"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        confirm_password = flask.request.form["confirm_password"]

        user_email = User.query.filter_by(email=email).first()
        if user_email is None:
            if password == confirm_password:
                user = User(
                    name=name,
                    email=email,
                    password=password
                )
                DATA_BASE.session.add(user)
                DATA_BASE.session.commit()
                message = "Успішно"
            else:
                message = "Паролі не співпадають"
        else:
            message = "Такий користувач вже існує"

    return {"message": message}