import flask
from catalog.models import Product
def render_home():
    new_products = Product.query.order_by(Product.id.desc()).limit(3).all()
    catalog = Product.query.limit(4)
    return flask.render_template("home.html", new_products=new_products, catalog=catalog)


def render_contacts():
    return flask.render_template("contacts.html")


def render_about():
    return flask.render_template("about-page.html")
