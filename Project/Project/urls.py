import user, home, catalog, cart, order, dashboard


home.home.add_url_rule(
    rule= '/',
    view_func= home.render_home,
    methods=['GET', 'POST']
)
home.home.add_url_rule(
    rule='/contacts/',
    view_func=home.render_contacts,
    methods=['GET', 'POST']
)
home.home.add_url_rule(
    rule='/about/',
    view_func=home.render_about,
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
user.user.add_url_rule(
    rule="/logout/",
    view_func=user.logout
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
    rule="/admin/create-product/",
    view_func=catalog.create_product,
    methods=['POST']
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
    rule="/cart/",
    view_func= cart.render_cart
)
cart.cart.add_url_rule(
    rule="/count_sum/",
    view_func= cart.count_sum
)
cart.cart.add_url_rule(
    rule="/delete_in_cart/",
    view_func= cart.delete_product_in_cart,
    methods=['GET', 'POST']
)
order.order.add_url_rule(
    rule="/pay/",
    view_func= order.pay,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/catalog/<int:id>/",
    view_func= catalog.render_product_by_id,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/product/<slug>/",
    view_func= catalog.render_product_by_slug,
    methods=['GET', 'POST']
)
catalog.catalog.add_url_rule(
    rule="/catalog/filter",
    view_func= catalog.filter_products,
    methods=['GET', 'POST']
)
order.order.add_url_rule(
    rule= '/order/',
    view_func= order.render_order,
    methods=['GET', 'POST']
)
order.order.add_url_rule(
    rule="/order/<city_name>",
    view_func= order.get_warehouses,
    methods=['GET', 'POST']
)
dashboard.dashboard.add_url_rule(
    rule="/contact-page/",
    view_func= dashboard.create_contact,
    methods=['GET', 'POST']
)
dashboard.dashboard.add_url_rule(
    rule="/delivery-info/",
    view_func= dashboard.create_delivery,
    methods=['GET', 'POST']
)
dashboard.dashboard.add_url_rule(
    rule="/delivery-info/select/<int:id>/",
    view_func=dashboard.select_delivery,
    methods=['POST']
)
dashboard.dashboard.add_url_rule(
    rule="/delivery-info/delete/<int:id>/",
    view_func=dashboard.delete_delivery,
    methods=['POST']
)
dashboard.dashboard.add_url_rule(
    rule="/dashboard/orders/cancel/<int:id>/",
    view_func=dashboard.cancel_order,
    methods=['POST']
)
dashboard.dashboard.add_url_rule(
    rule="/dashboard/",
    view_func= dashboard.render_dashboard,
    methods=['GET', 'POST']
)
