import flask
from Project.db import DATA_BASE
from .models import User
from Project.config_page import config_page
import flask_login
from flask_mail import Message
from Project.settings import mail
import random
import werkzeug.security as security


def render_login():
    if flask.request.method == "POST":
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        user = User.query.filter_by(email=email).first() 
        is_password_compare = security.check_password_hash(user.password, password=password)
        if user.email == email and is_password_compare:
            flask_login.login_user(user)
    if not flask_login.current_user.is_authenticated:
        return flask.make_response(flask.jsonify({
            "success": False
        }))
    else:
        return flask.redirect("/")    


def render_register():
    message = ""
    if flask.request.method == 'POST':
        name = flask.request.form["first_name"]
        email = flask.request.form["email"]
        password = flask.request.form["password"]
        confirm_password = flask.request.form["confirm_password"]

        user_email = User.query.filter_by(email= email).first()
        if user_email is None :
            if password == confirm_password:
                code = ""
                for _ in range(6):
                    code += str(random.randint(0, 9))

                msg = Message(
                    "Email confirm",
                    recipients= [email],
                    sender= "lenafedchenko07@gmail.com",
                    body=code
                )
                msg.html = f"""
                    <html lang="en">
                    <body style="margin: 0; padding: 0; background-color: #f4f4f4">
                        <div style="max-width: 500px; margin:40px; background-color: #ffffff ;
                        padding: 24px; border-radius: 6px; text-align: center">
                            <h2 style="color: black">Підтвердження почти</h2>
                            <p style="font-size: 16px; color:grey">Ваш код підтвердження:</p>
                            <div style="font-size: 28px; font-weight: bolt; color: black; 
                            margin: 20px; letter-spacing: 4px">
                                {code}
                            </div>
                            <p style="font-size: 13px; color: #888">Якщо ви не реєструвалися проігноруйте цей лист</p>
                        </div>
                    </body>
                    </html>
                """
                
                mail.send(msg)
                flask.session["verify_code"] = code
                flask.session["name"] = name
                flask.session["email"] = email
                flask.session["password"] = password
                message = "Successfully"
            else:
                message = "Password didnt match"
        else:
            message = "User alredy exist"
    return flask.make_response(flask.jsonify({
        "message": message
    }))





def render_verify():
    if flask.request.method == "POST":
        verify_code = ""
        for i in flask.request.form.values():
            verify_code += i
        if flask.session.get("verify_code") == verify_code:
            password = flask.session.get("password")
            hashed_password = security.generate_password_hash(password, salt_length=10)
            user = User(
                first_name = flask.session.get("name"),
                email = flask.session.get("email"),
                password = hashed_password
            )
            DATA_BASE.session.add(user)
            DATA_BASE.session.commit()
            return flask.redirect("/")
    return flask.make_response(flask.jsonify({
        "success": False
    }))


def logout():
    # flask.redirect()
    flask.session.clear()
    return flask.redirect("/")


