import flask
from Project.config_page import config_page
from .models import Product
from flask import request
from Project.db import DATA_BASE
import flask_login
import os

def render_catalog():
    categories = []
    page = request.args.get("page", 1, type= int)
    queryParam = request.args.get("category")
    query = Product.query
    if flask.request.method == "POST":
        if queryParam == "filter":
            category = request.form.get("categories")
            if category != "all":
                query = query.filter(Product.category == category)
            else:
                query = query.all()
    pagination = query.paginate(page=page, per_page=1)
    for product in Product.query.all():
        if product.category not in categories:
            categories.append(product.category)
    return flask.render_template("catalog.html", products=pagination.items, pagination= pagination, categories=categories)

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

@config_page(name="product.html")
def render_product_by_id(id: int):
    product = Product.query.get(ident=id)
    return {
        "product": product
    }


def filter_products():
    category_request = request.get_json()
    selected_category = category_request["selectCategory"]
    query = Product.query
    if selected_category != "all":
        query = query.filter(Product.category == selected_category)
    page = category_request["page"]
    pagination = query.paginate(page=page, per_page=2)
    products = pagination.items
    list_products = []
    for product in products:
        list_products.append({
            "id": product.id,
            "name": product.name, 
            "description": product.description,
            "image_url": product.image_url, 
            "category": product.category,
            "old_price": product.old_price,
            "price": product.price
        })
    response = flask.make_response(flask.jsonify({
        "status": "succes",
        "filtrated_products": list_products,
        "pagination": {
            "page": pagination.page,
            "total_count": pagination.pages,
            "next_page": pagination.next_num,
            "prev_num": pagination.prev_num,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }))

    return response