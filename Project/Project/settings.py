import flask, os


project = flask.Flask(
    import_name= 'Project',
    template_folder= 'templates',
    static_folder= 'static',
    static_url_path= '/static/',
    instance_path= os.path.abspath(os.path.join(__file__, '..', 'instance'))
)