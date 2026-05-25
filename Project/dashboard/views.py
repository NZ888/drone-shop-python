import flask, flask_login
from user.models import User
from order.models import Order
from Project.db import DATA_BASE
from .models import Delivery

# lalal

def create_contact():
    user = User.query.filter_by(id=flask_login.current_user.id).first()
    if flask.request.method == "POST":
        first_name = flask.request.form["first_name"]
        last_name = flask.request.form["last_name"]
        second_name = flask.request.form["second_name"]
        date = flask.request.form["date"]
        phone = flask.request.form["phone"]
        email = flask.request.form["email"]
        user.first_name = first_name
        user.last_name = last_name
        user.second_name = second_name
        user.date_of_birth = date
        user.phone = phone
        user.email = email
        DATA_BASE.session.commit()
        return flask.make_response(flask.jsonify({
            "status": 200
        }))



def create_delivery():
    user_id = flask_login.current_user.id
    if flask.request.method == "POST":
        city = flask.request.form["city"]
        streat = flask.request.form["streat"]
        house = flask.request.form["house"]
        block = flask.request.form["block"]
        flat = flask.request.form["flat"]
        delivery = Delivery(
            city=city,
            streat=streat,
            house=house,
            block=block,
            user_id=user_id,
            flat = flat,
            is_selected = False
        )
        DATA_BASE.session.add(delivery)
        DATA_BASE.session.commit()
        return flask.make_response(flask.jsonify({
            "status": 200
        }))


def render_dashboard():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/login")
    user_id = flask_login.current_user.id
    user = User.query.filter_by(id=user_id).first()
    adresses = Delivery.query.filter_by(user_id=user.id).all()
    orders = Order.query.filter_by(user_id=user.id).all()

    return flask.render_template("dashboard.html", user=user, orders=orders, adresses=adresses)