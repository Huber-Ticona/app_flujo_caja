from flask import Flask, redirect, url_for, jsonify
from .extensions import db, migrate, login_manager


def create_app():
    app = Flask(__name__)

    # CARGA INSTANCIA CONFIGURACION
    if app.config['ENV'] == 'development':
        app.config.from_object('instance.config.ConfigDevelop')
    else:
        app.config.from_object('instance.config.ConfigProduction')

    # Inicializamos Extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    # Registramos blueprints
    from .main import main_bp
    from .auth.auth import auth_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/profile')

    # Registramos los modelos de base de datos
    from .models import Usuario, Empresa, IngresoGasto

    @login_manager.user_loader
    def load_user(id):
        return Usuario().get_by_id(id)

    return app
