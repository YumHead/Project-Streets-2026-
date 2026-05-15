from flask import Flask
from webapp.pages.home import bp as home_bp
from webapp.pages.latest import bp as latest_bp
from webapp.pages.about import bp as about_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(latest_bp)
    app.register_blueprint(about_bp)
    return app