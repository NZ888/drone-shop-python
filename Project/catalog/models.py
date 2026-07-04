from Project.db import DATA_BASE
from Project.db_tables import product_order

class Product(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key= True)
    slug = DATA_BASE.Column(DATA_BASE.String(120), nullable=True, unique=True)
    name = DATA_BASE.Column(DATA_BASE.String(100), nullable=False)
    price = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    old_price = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    image_url = DATA_BASE.Column(DATA_BASE.String(100), nullable=False)
    category = DATA_BASE.Column(DATA_BASE.String(50), nullable=False)
    description = DATA_BASE.Column(DATA_BASE.String(500), nullable=False)
    order = DATA_BASE.relationship(
        'Order',
        secondary=product_order,
        back_populates='products'
    )
    blocks = DATA_BASE.relationship(
        'ProductBlock',
        back_populates='product',
        cascade='all, delete-orphan',
        order_by='ProductBlock.number'
    )
    specifications = DATA_BASE.relationship(
        'ProductSpecifications',
        back_populates='product',
        cascade='all, delete-orphan',
        uselist=False
    )
    

class ProductBlock(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    product_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey('product.id'), nullable=False)
    title = DATA_BASE.Column(DATA_BASE.String(150), nullable=False)
    description = DATA_BASE.Column(DATA_BASE.Text, nullable=False)
    image = DATA_BASE.Column(DATA_BASE.String(150), nullable=True)
    number = DATA_BASE.Column(DATA_BASE.Integer, nullable=False, default=1)

    product = DATA_BASE.relationship('Product', back_populates='blocks')


class ProductSpecifications(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    product_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey('product.id'), nullable=False)
    title = DATA_BASE.Column(DATA_BASE.String(150), nullable=False)
    description = DATA_BASE.Column(DATA_BASE.Text, nullable=False)
    image = DATA_BASE.Column(DATA_BASE.String(150), nullable=True)
    code = DATA_BASE.Column(DATA_BASE.String(50), nullable=True)
    ufs = DATA_BASE.Column(DATA_BASE.String(50), nullable=True)
    emmc = DATA_BASE.Column(DATA_BASE.String(50), nullable=True)

    product = DATA_BASE.relationship('Product', back_populates='specifications')
