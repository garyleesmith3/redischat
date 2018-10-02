from flask import Flask
from config import Config

da_app = Flask(__name__)
da_app.config.from_object(Config)

from app_package import routes