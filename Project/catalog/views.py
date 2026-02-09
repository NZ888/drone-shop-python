import flask
from Project.config_page import config_page
from .models import Product
from flask import request
from Project.db import DATA_BASE
import flask_login
import os

def render_catalog():
    page = request.args.get("page", 1, type= int)
    pagination = Product.query.paginate(page=page, per_page=1)
    return flask.render_template("catalog.html", products=pagination.items, pagination= pagination)

def render_admin():
    if flask_login.current_user.is_authenticated and flask_login.current_user.isAdmin:
        page = request.args.get("page", 1, type= int)
        pagination = Product.query.paginate(page=page, per_page=1)
        if flask.request.method == "POST":
            name = flask.request.form["name"]
            product = Product.query.filter_by(name= name).first()
            if not product:
                image = flask.request.files["image"]
                image.save(os.path.abspath(os.path.join(__file__, "..", "static", "media", f"{image.filename}")))
                product = Product(
                    name= name, 
                    price = flask.request.form["price"],
                    old_price = flask.request.form["old_price"],
                    image_url = image.filename,
                    category = flask.request.form["category"],
                    description = flask.request.form["description"]
                )
                DATA_BASE.session.add(product)
                DATA_BASE.session.commit()
        return flask.render_template("admin.html", products=pagination.items, pagination= pagination)
    else:
        return "404"
def delete_product():
    id = request.args.get(key= "id", type= int)
    product = Product.query.get(ident=id)
    if product:
        DATA_BASE.session.delete(product)
        DATA_BASE.session.commit()
    return flask.redirect("/admin/")

def add_to_cart():
    product_id = request.json.get("product_id")
    id_list = flask.request.cookies.get("id_list")
    if not id_list:
        new_id_list = product_id
    else:
        new_id_list = id_list + "|" + product_id
    final_product_list = new_id_list.split(sep="|")
    product_count = final_product_list.count(product_id)
    response = flask.make_response(flask.jsonify({
        "status": "succes",
        "productsCount": product_count
    }))
    response.set_cookie(key="id_list", value=new_id_list)    
    return response



def render_cart():
    product_list = []
    cookies_id = flask.request.cookies.get("id_list")
    if cookies_id:
        id_list = cookies_id.split(sep="|")
        id_list_copy = id_list.copy()
        id_list_copy = set(id_list_copy)
        for id in id_list_copy:
            product = Product.query.get(id)
            product_list.append({
                "product" : product,
                "count" : id_list.count(id)
            })
    return flask.render_template("cart.html", products_list = product_list)


def count_products():
    id = flask.request.cookies.get("id_list")
    if id:
        id_list = id.split(sep="|")
    else:
        id_list=[]
    response = flask.make_response(flask.jsonify({
        "status": "succes",
        "productsCount": len(id_list)
    }))

    return response

def delete_product_in_cart():
    product_id = request.json.get("product_id")
    id_list = flask.request.cookies.get("id_list").split(sep="|")
    id_list.remove(product_id)
    new_id_list = "|".join(id_list)
    finall_product_list = new_id_list.count(product_id)
    response = flask.make_response(flask.jsonify({
        "status" : "succes",
        "productsCount": finall_product_list
    }))
    if new_id_list:
        response.set_cookie(key="id_list", value=new_id_list)
    else:
        response.delete_cookie(key="id_list")
    return response