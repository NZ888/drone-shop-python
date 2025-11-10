import flask

def render_home():
    return flask.render_template("home.html")