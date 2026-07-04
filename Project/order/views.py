import flask, requests, flask_login
from Project.db import DATA_BASE
from .models import Order
from user.models import User
import os
from catalog.models import Product
from cart.utils import count_products_price


def get_products_from_raw_ids(raw_id_list):
    product_list = []

    if not raw_id_list:
        return product_list

    id_list = raw_id_list.split(sep="|")
    id_list_copy = set(id_list)

    for id in id_list_copy:
        product = Product.query.get(id)

        if product:
            product_list.append({
                "product": product,
                "count": id_list.count(id)
            })

    return product_list


def render_order():
    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/login")

    product_id = flask.request.args.get("product_id")

    if product_id:
        raw_id_list = product_id
    else:
        raw_id_list = flask.request.cookies.get("id_list")

    product_list = get_products_from_raw_ids(raw_id_list)

    return flask.render_template(
        'order.html',
        products_list=product_list,
        checkout_ids=raw_id_list or ""
    )

def get_warehouses(city_name: str):
    TOKEN = os.environ["NOVA_POST_TOKEN"]
    delivery_type = flask.request.args.get('type')

    payload = {
        "api_key": TOKEN,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityName": city_name
        }
    }
    response = requests.post(
        "https://api.novaposhta.ua/v2.0/json/",
        json=payload
    )
    result = response.json()
    warehouses = []
    for data in result["data"]:
        # print(data["TypeOfWarehouse"], data["Description"])
        if data["TypeOfWarehouse"] == "841339c7-591a-42e2-8233-7a0a00f0ed6f" and delivery_type == "warehouse":
            warehouses.append(data["Description"])
        elif data["TypeOfWarehouse"] == "f9316480-5f2d-425d-bc2c-ac7cd29decf0" and delivery_type == "parcel_machine":
            warehouses.append(data["Description"])
        elif data["TypeOfWarehouse"] == "6f8c7162-4b72-4b0a-88e5-906948c6a92f" and delivery_type == "expres_delivery":
            warehouses.append(data["Description"])
        elif data["TypeOfWarehouse"] == "9a68df70-0267-42a8-bb5c-37f427e36ee4" and delivery_type == "courier":
            warehouses.append(data["Description"])
    response = flask.make_response(flask.jsonify({
        "warehouses" : warehouses
    }))
    return response

def pay():
    if flask.request.method == "POST":
        raw_id_list = flask.request.form.get("checkout_ids") or flask.request.cookies.get("id_list")
        product_list = get_products_from_raw_ids(raw_id_list)
        first_name = flask.request.form["first_name"]
        second_name = flask.request.form["second_name"]
        surname = flask.request.form["surname"]
        phone = flask.request.form["telephone"]
        email = flask.request.form["email"]
        message = flask.request.form["message"]
        payment = flask.request.form["payment"]
        user_id = flask_login.current_user.id
        order = Order(
            first_name= first_name,
            second_name= second_name,
            surname= surname,
            phone= phone,
            email= email,
            message= message,
            pay_method = payment,
            warehouse = "",
            user_id=user_id
        )
        for product in product_list:
            order.products.append(product["product"])
        DATA_BASE.session.add(order)
        DATA_BASE.session.commit()
    raw_id_list = flask.request.form.get("checkout_ids") or flask.request.cookies.get("id_list")
    sum = count_products_price(raw_id_list=raw_id_list)

    if payment == "card":
        TOKEN = os.environ["MONOBANK_TOKEN"]
        payload = {
            "amount": sum * 100,
            "ccy": 980,
            "redirectUrl": "http://127.0.0.1:8000"
        }
        headers = {
            "X-Token": TOKEN
        }
        response = requests.post(
            "https://api.monobank.ua/api/merchant/invoice/create",
            json=payload,
            headers=headers
            )
        request = response.json()
        pay_url = request["pageUrl"]
        return flask.redirect(pay_url)

    return flask.redirect("/")
