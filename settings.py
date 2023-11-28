import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
#from flask_gravatar import Gravatar
import secrets
from dotenv import load_dotenv
import logging
from logging.config import dictConfig


load_dotenv()

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
            "json_formatter": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 100000,
                "backupCount": 5,
                "formatter": "json_formatter",
            },
            "werkzeug_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "werkzeug.log",
                "maxBytes": 100000,
                "backupCount": 5,
                "formatter": "json_formatter",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "file"]},
        "loggers": {
            "werkzeug": {
                "level": "DEBUG",
                "handlers": ["werkzeug_file", "console"],
                "propagate": False,
            },
        }
    }
)

werkzeug_logger = logging.getLogger("werkzeug")

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bootstrap = Bootstrap5(app)

csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# gravatar = Gravatar(app,
#                     size=100,
#                     rating='g',
#                     default='retro',
#                     force_default=False,
#                     force_lower=False,
#                     use_ssl=False,
#                     base_url=None)
