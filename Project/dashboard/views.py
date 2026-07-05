import flask, flask_login
from sqlalchemy.exc import IntegrityError

from user.models import User
from order.models import Order
from Project.db import DATA_BASE
from .models import Delivery

# lalal

def json_response(data, status=200):
    return flask.make_response(flask.jsonify(data), status)


def get_dashboard_user():
    if not flask_login.current_user.is_authenticated:
        return None

    return User.query.filter_by(id=flask_login.current_user.id).first()


def delivery_to_dict(delivery):
    return {
        "id": delivery.id,
        "city": delivery.city,
        "streat": delivery.streat,
        "house": delivery.house,
        "flat": delivery.flat,
        "block": delivery.block,
        "is_selected": delivery.is_selected
    }


def create_contact():
    user = get_dashboard_user()

    if not user:
        return json_response({
            "success": False,
            "message": "Потрібно увійти в кабінет"
        }, 401)

    if flask.request.method != "POST":
        return flask.redirect("/dashboard/")

    first_name = flask.request.form.get("first_name", "").strip()
    last_name = flask.request.form.get("last_name", "").strip()
    second_name = flask.request.form.get("second_name", "").strip()
    date = flask.request.form.get("date", "").strip()
    phone = flask.request.form.get("phone", "").strip()
    email = flask.request.form.get("email", "").strip()

    if not first_name or not email:
        return json_response({
            "success": False,
            "message": "Заповніть ім'я та E-mail"
        }, 400)

    same_email_user = User.query.filter(User.email == email, User.id != user.id).first()

    if same_email_user:
        return json_response({
            "success": False,
            "message": "Такий E-mail вже використовується"
        }, 400)

    user.first_name = first_name
    user.last_name = last_name
    user.second_name = second_name
    user.date_of_birth = date
    user.phone = phone
    user.email = email

    try:
        DATA_BASE.session.commit()
    except IntegrityError:
        DATA_BASE.session.rollback()

        return json_response({
            "success": False,
            "message": "Не вдалося зберегти E-mail"
        }, 400)

    return json_response({
        "success": True,
        "message": "Контактні дані збережено"
    })


def create_delivery():
    user = get_dashboard_user()

    if not user:
        return json_response({
            "success": False,
            "message": "Потрібно увійти в кабінет"
        }, 401)

    if flask.request.method != "POST":
        return flask.redirect("/dashboard/")

    delivery_id = flask.request.form.get("delivery_id", type=int)
    city = flask.request.form.get("city", "").strip()
    streat = flask.request.form.get("streat", "").strip()
    house = flask.request.form.get("house", "").strip()
    block = flask.request.form.get("block", "").strip()
    flat = flask.request.form.get("flat", "").strip()

    if not city or not streat or not house:
        return json_response({
            "success": False,
            "message": "Заповніть місто, вулицю та будинок"
        }, 400)

    delivery = None
    has_addresses = Delivery.query.filter_by(user_id=user.id).first()

    if delivery_id:
        delivery = Delivery.query.filter_by(id=delivery_id, user_id=user.id).first()

        if not delivery:
            return json_response({
                "success": False,
                "message": "Адресу не знайдено"
            }, 404)

    if not delivery:
        delivery = Delivery(user_id=user.id)
        DATA_BASE.session.add(delivery)

    delivery.city = city
    delivery.streat = streat
    delivery.house = house
    delivery.block = block
    delivery.flat = flat

    should_select = flask.request.form.get("is_selected") == "1"
    if not has_addresses or delivery.is_selected:
        should_select = True

    if should_select:
        Delivery.query.filter_by(user_id=user.id).update({
            "is_selected": False
        })
        delivery.is_selected = True

    DATA_BASE.session.commit()

    return json_response({
        "success": True,
        "message": "Адресу доставки збережено",
        "delivery": delivery_to_dict(delivery)
    })


def select_delivery(id):
    user = get_dashboard_user()

    if not user:
        return json_response({
            "success": False,
            "message": "Потрібно увійти в кабінет"
        }, 401)

    delivery = Delivery.query.filter_by(id=id, user_id=user.id).first()

    if not delivery:
        return json_response({
            "success": False,
            "message": "Адресу не знайдено"
        }, 404)

    Delivery.query.filter_by(user_id=user.id).update({
        "is_selected": False
    })
    delivery.is_selected = True
    DATA_BASE.session.commit()

    return json_response({
        "success": True,
        "message": "Адресу обрано",
        "delivery": delivery_to_dict(delivery)
    })


def delete_delivery(id):
    user = get_dashboard_user()

    if not user:
        return json_response({
            "success": False,
            "message": "Потрібно увійти в кабінет"
        }, 401)

    delivery = Delivery.query.filter_by(id=id, user_id=user.id).first()

    if not delivery:
        return json_response({
            "success": False,
            "message": "Адресу не знайдено"
        }, 404)

    was_selected = delivery.is_selected

    DATA_BASE.session.delete(delivery)
    DATA_BASE.session.commit()

    if was_selected:
        next_delivery = Delivery.query.filter_by(user_id=user.id).first()

        if next_delivery:
            next_delivery.is_selected = True
            DATA_BASE.session.commit()

    return json_response({
        "success": True,
        "message": "Адресу видалено"
    })


def cancel_order(id):
    user = get_dashboard_user()

    if not user:
        return json_response({
            "success": False,
            "message": "Потрібно увійти в кабінет"
        }, 401)

    order = Order.query.filter_by(id=id, user_id=user.id).first()

    if not order:
        return json_response({
            "success": False,
            "message": "Замовлення не знайдено"
        }, 404)

    order.products.clear()
    DATA_BASE.session.delete(order)
    DATA_BASE.session.commit()

    return json_response({
        "success": True,
        "message": "Замовлення скасовано"
    })


def render_dashboard():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/login")

    user = User.query.filter_by(id=flask_login.current_user.id).first()
    adresses = Delivery.query.filter_by(user_id=user.id).order_by(
        Delivery.is_selected.desc(),
        Delivery.id.desc()
    ).all()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).all()

    return flask.render_template(
        "dashboard.html",
        user=user,
        orders=orders,
        adresses=adresses
    )
