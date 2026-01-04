import user, home

home.home.add_url_rule(
    rule='/',
    view_func=home.render_home,
    methods=['GET', 'POST']
)
user.user.add_url_rule(
    rule='/login/',
    view_func=user.render_login,
    methods=['GET', 'POST']
)
user.user.add_url_rule(
    rule='/register/',
    view_func=user.render_register,
    methods=['GET', 'POST']
)
user.user.add_url_rule(
    rule='/verify_code/',
    view_func=user.render_verify,
    methods=['GET', 'POST']
)
user.user.add_url_rule(
    rule='/logout/',
    view_func=user.logout,
    methods=['GET']
)