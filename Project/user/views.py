import flask

def render_login():
    return flask.render_template(
        template_name_or_list= "login.html"
    )

def render_register():
    return flask.render_template(
        template_name_or_list= "register.html"
    )