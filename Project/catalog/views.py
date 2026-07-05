import flask
from Project.config_page import config_page
from .models import Product, ProductBlock, ProductSpecifications
from flask import request
from Project.db import DATA_BASE
import flask_login
import os
import re


def create_slug(name):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return slug or "product"


def unique_slug(name):
    slug = create_slug(name)
    current_slug = slug
    number = 2

    while Product.query.filter_by(slug=current_slug).first():
        current_slug = f"{slug}-{number}"
        number += 1

    return current_slug


def save_product_image(file):
    if not file or not file.filename:
        return None

    file.save(os.path.abspath(os.path.join(__file__, "..", "static", "media", file.filename)))
    return file.filename


def create_product_from_form():
    name = flask.request.form["name"]
    product = Product.query.filter_by(name=name).first()

    if product:
        return product

    image = flask.request.files["image"]
    image_name = save_product_image(image)
    price = flask.request.form["price"]
    old_price = flask.request.form.get("old_price") or price

    product = Product(
        slug=unique_slug(name),
        name=name,
        price=price,
        old_price=old_price,
        image_url=image_name,
        category=flask.request.form["category"],
        description=flask.request.form["description"]
    )
    DATA_BASE.session.add(product)
    DATA_BASE.session.flush()

    block_titles = flask.request.form.getlist("block_title")
    block_descriptions = flask.request.form.getlist("block_description")
    block_numbers = flask.request.form.getlist("block_number")
    block_images = flask.request.files.getlist("block_image")

    for index, title in enumerate(block_titles):
        if not title:
            continue

        block_image = save_product_image(block_images[index]) if index < len(block_images) else None
        block = ProductBlock(
            product_id=product.id,
            title=title,
            description=block_descriptions[index] if index < len(block_descriptions) else "",
            image=block_image,
            number=block_numbers[index] if index < len(block_numbers) and block_numbers[index] else index + 1
        )
        DATA_BASE.session.add(block)

    if flask.request.form.get("spec_title"):
        spec_image = save_product_image(flask.request.files.get("spec_image"))
        specifications = ProductSpecifications(
            product_id=product.id,
            title=flask.request.form["spec_title"],
            description=flask.request.form["spec_description"],
            image=spec_image,
            code=flask.request.form.get("spec_code"),
            ufs=flask.request.form.get("spec_ufs"),
            emmc=flask.request.form.get("spec_emmc")
        )
        DATA_BASE.session.add(specifications)

    DATA_BASE.session.commit()
    return product


def create_product():
    if not flask_login.current_user.is_authenticated or not flask_login.current_user.isAdmin:
        return flask.redirect("/catalog/")

    if flask.request.method == "POST":
        create_product_from_form()

    return flask.redirect("/catalog/")

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
    pagination = query.paginate(page=page, per_page=4)
    for product in Product.query.all():
        if product.category not in categories:
            categories.append(product.category)
    return flask.render_template("catalog.html", products=pagination.items, pagination= pagination, categories=categories)

# lalalabebebeb
def render_admin():
    if flask_login.current_user.is_authenticated and flask_login.current_user.isAdmin:
        page = request.args.get("page", 1, type= int)
        pagination = Product.query.paginate(page=page, per_page=1)
        if flask.request.method == "POST":
            create_product_from_form()
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

def get_product_page_context(product):
    blocks = ProductBlock.query.filter_by(product_id=product.id).order_by(ProductBlock.number).all()
    specifications = ProductSpecifications.query.filter_by(product_id=product.id).first()
    related_products = Product.query.filter(
        Product.id != product.id,
        Product.category == product.category
    ).limit(4).all()

    if len(related_products) < 4:
        extra_products = Product.query.filter(Product.id != product.id).limit(4 - len(related_products)).all()
        related_products.extend(extra_products)

    return {
        "product": product,
        "blocks": blocks,
        "specifications": specifications,
        "related_products": related_products
    }


@config_page(name="product.html")
def render_product_by_id(id: int):
    product = Product.query.get(ident=id)

    if not product:
        return {
            "product": None
        }

    return get_product_page_context(product)


def render_product_by_slug(slug: str):
    product = Product.query.filter_by(slug=slug).first_or_404()
    return flask.render_template("product.html", **get_product_page_context(product))


def filter_products():
    category_request = request.get_json()
    selected_category = category_request["selectCategory"]
    query = Product.query
    if selected_category != "all":
        query = query.filter(Product.category == selected_category)
    page = category_request["page"]
    pagination = query.paginate(page=page, per_page=4)
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
            "price": product.price,
            "slug": product.slug
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
