import random

import flask
import flask_login
from flask_mail import Message

from Project.db import DATA_BASE
from Project.settings import mail
from .models import User


def _collect_code(payload):
    digits = [value for key, value in sorted(payload.items()) if key.startswith("code")]
    return "".join(digits)


def render_login():
    message = ""
    message_type = ""

    if flask.request.method == "POST":
        username = flask.request.form.get("username", "").strip()
        password = flask.request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flask_login.login_user(user)
            return flask.redirect("/")

        message = "Невірний логін або пароль"
        message_type = "error"

    return flask.render_template(
        "register.html",
        default_tab="login",
        current_user=flask_login.current_user,
        message=message,
        message_type=message_type,
    )


def render_register():
    message = ""
    message_type = ""

    if flask.request.method == "POST":
        name = flask.request.form.get("username", "").strip()
        email = flask.request.form.get("email", "").strip()
        password = flask.request.form.get("password", "").strip()
        confirm_password = flask.request.form.get("confirm_password", "").strip()

        if not all([name, email, password, confirm_password]):
            message = "Заповніть усі поля"
            message_type = "error"
        else:
            user_email = User.query.filter_by(email=email).first()
            if user_email is None:
                if password == confirm_password:
                    code = "".join(str(random.randint(0, 9)) for _ in range(6))

                    msg = Message(
                        "Email confirm",
                        recipients=[email],
                        body=code,
                    )
                    mail.send(msg)
                    flask.session["verify_code"] = code
                    flask.session["name"] = name
                    flask.session["email"] = email
                    flask.session["password"] = password
                    flask.flash("Код підтвердження надіслано на вашу пошту")
                    return flask.redirect(flask.url_for("user.render_verify"))
                message = "Паролі не співпадають"
                message_type = "error"
            else:
                message = "Такий користувач вже існує"
                message_type = "error"

    return flask.render_template(
        "register.html",
        default_tab="register",
        current_user=flask_login.current_user,
        message=message,
        message_type=message_type,
    )


def render_verify():
    if not flask.session.get("verify_code"):
        return flask.redirect(flask.url_for("user.render_register"))

    message = ""
    message_type = ""

    if flask.request.method == "POST":
        verify_code = _collect_code(flask.request.form)
        if flask.session.get("verify_code") == verify_code:
            user = User(
                username=flask.session.get("name"),
                email=flask.session.get("email"),
                password=flask.session.get("password"),
            )
            DATA_BASE.session.add(user)
            DATA_BASE.session.commit()
            flask_login.login_user(user)
            flask.session.pop("verify_code", None)
            flask.session.pop("name", None)
            flask.session.pop("email", None)
            flask.session.pop("password", None)
            return flask.redirect("/")

        message = "Код не співпадає"
        message_type = "error"

    return flask.render_template(
        "verify_code.html",
        current_user=flask_login.current_user,
        message=message,
        message_type=message_type,
    )


def logout():
    flask_login.logout_user()
    flask.session.clear()
    return flask.redirect("/")