import os
import secrets
from datetime import timedelta

from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))           
PROJECT_DIR = os.path.dirname(CURRENT_DIR)                        
BASE_DIR = os.path.dirname(PROJECT_DIR)                          


project = Flask(
    __name__,
    root_path=CURRENT_DIR,
    template_folder=os.path.join(PROJECT_DIR, "templates"),
    static_folder=os.path.join(PROJECT_DIR, "static"),
    static_url_path="/static",
    instance_path=os.path.join(BASE_DIR, "instance"),
)


project.secret_key = os.getenv("SECRET_KEY", secrets.token_hex())
project.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=7)


project.config["MAIL_SERVER"] = "smtp.gmail.com"
project.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
project.config["MAIL_USE_TLS"] = True
project.config["MAIL_USE_SSL"] = False
project.config["MAIL_USERNAME"] = os.getenv("MAIL")
project.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")
project.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL")

mail = Mail()
mail.init_app(project)
