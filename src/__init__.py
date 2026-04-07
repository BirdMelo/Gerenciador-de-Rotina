#PAGINA INICIAL DO PROJETO

from flask import Flask, render_template
from src.config import Config
from .extentions import db, migrate
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # inicializa ORM e migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprints
    from .blueprints.home import bp as home_bp
    from .blueprints.user import bp as user_bp
    from .blueprints.task import bp as task_bp

    # Registrando rotas dos blueprints no app principal
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(task_bp, url_prefix='/task')

    # erro 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    return app