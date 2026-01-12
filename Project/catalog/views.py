import flask
from Project.config_page import config_page
from .models import Product
from flask import request
from Project.db import DATA_BASE
import flask_login


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
                product = Product(
                    name= name, 
                    price = flask.request.form["price"],
                    old_price = flask.request.form["old_price"],
                    image_url = flask.request.form["image_url"],
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

