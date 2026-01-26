import user, home, catalog


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
catalog.catalog.add_url_rule(
    rule="/add-to-cart/",
    view_func= catalog.add_to_cart,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/cart/",
    view_func= catalog.render_cart
)
catalog.catalog.add_url_rule(
    rule="/count_products/",
    view_func= catalog.count_products
)
