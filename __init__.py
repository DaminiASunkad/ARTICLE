"""
The flask application package.
"""
import logging
import sys
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix   # ✅ ADD THIS

app = Flask(__name__)
app.config.from_object(Config)

# 🔐 IMPORTANT: Fix HTTPS redirect issue on Azure
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# --- Logging Configuration ---
# Set the logging level to INFO so we catch login events
app.logger.setLevel(logging.INFO)

# Create a handler that writes to the standard output (console)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))

# Add the handler to the app logger
app.logger.addHandler(stream_handler)
# -----------------------------

Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views
