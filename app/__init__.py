from flask import Flask, redirect, url_for, jsonify,render_template
from .extensions import db, migrate, login_manager,minify
from .config import ConfigDevelop,ConfigProduction
from dotenv import load_dotenv


def create_app():
    load_dotenv()  # Carga las variables de entorno desde el archivo .env
    app = Flask(__name__)

    # CARGA INSTANCIA CONFIGURACION
    if app.config['DEBUG'] == True:
        app.config.from_object(ConfigDevelop)
    else:
        app.config.from_object(ConfigProduction)

    print(f"|-- ENV CONFIG: {app.config['DEBUG']}")
    # Inicializamos Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    minify.init_app(app)

    # Registramos blueprints
    from .main import main_bp
    from .auth.auth import auth_bp
    from .api import api_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/profile')

    # Registramos los modelos de base de datos
    from .models import Usuario, Empresa, Embarque, Periodo, Liquidacion
    
    @login_manager.user_loader
    def load_user(id):
        return Usuario().get_by_id(id)
    
    @app.route("/test1")
    def test1():
        return render_template('test/test1.html')


    return app
