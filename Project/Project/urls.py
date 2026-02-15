import cart, catalog, home, user

home.home.add_url_rule(
    rule= '/',
    view_func= home.render_home,
    methods=['GET', 'POST']
)
user.user.add_url_rule(
    rule='/login/', 
    view_func= user.render_login, 
    methods=['GET', 'POST']
    )
user.user.add_url_rule(
    rule='/register/', 
    view_func= user.render_register, 
    methods=['GET', 'POST']
    )
user.user.add_url_rule(
    rule="/verify_code/",
    view_func= user.render_verify,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/catalog/",
    view_func= catalog.render_catalog,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/admin/",
    view_func= catalog.render_admin,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/delete/",
    view_func= catalog.delete_product
)
cart.cart.add_url_rule(
    rule="/add-to-cart/",
    view_func= cart.add_to_cart,
    methods=['GET', 'POST']
)
cart.cart.add_url_rule(
    rule="/cart-modal/",
    view_func= cart.render_cart_modal
)
cart.cart.add_url_rule(
    rule="/cart/",
    view_func= cart.render_cart
)
cart.cart.add_url_rule(
    rule="/count_products/",
    view_func= cart.count_products
)
cart.cart.add_url_rule(
    rule="/delete_in_cart/",
    view_func= cart.delete_product_in_cart,
    methods=['GET', 'POST']
)