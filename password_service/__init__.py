from flask import Flask
app = Flask(__name__)

# Set sort keys off to return JSON in expected order.
app.config['JSON_SORT_KEYS'] = False

# Import routes into application.
from .views import configure_routes

configure_routes(app)