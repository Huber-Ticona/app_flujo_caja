from flask import Blueprint, request, redirect, url_for, render_template,flash,session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime,timezone,timedelta
from ..forms import Login_Form
from html import escape

from ..models import Usuario

auth_bp = Blueprint('auth_bp', __name__,
                    static_folder='static', template_folder='templates')


""" @auth_bp.route('/reset')
def cuenta():
    session.pop('intentos_fallidos', None)
    session.pop('ultimo_fallido', None)
    return 'time reset' """


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    formulario = Login_Form()

    # Verifica peticion POST y valida el formulario
    if formulario.validate_on_submit():

        usuario = escape(request.form.get('usuario'))
        contrasena = escape(request.form.get('contrasena'))

        # Intentos de inicio de sesión fallidos permitidos antes de bloqueo
        max_intentos_fallidos = 3

        # Duración del bloqueo después de 3 intentos fallidos (en minutos)
        tiempo_bloqueo = 3  # minutos

        # Verificar si el usuario está bloqueado
        if 'intentos_fallidos' in session and 'ultimo_fallido' in session:
            intentos_fallidos = session['intentos_fallidos']
            ultimo_fallido = session['ultimo_fallido']
            tiempo_actual = datetime.now(timezone.utc)
            """ print('|Intentos fallidos: ',intentos_fallidos)
            print(f"|Tiempo actual: {tiempo_actual} |type: {type(tiempo_actual)}",)
            print(f"|ultimo intento: {ultimo_fallido} | type{type(ultimo_fallido)}",)
            print(f"|resta: {tiempo_actual- ultimo_fallido}") """
            # Si ha pasado el tiempo de bloqueo, restablecer los intentos
            if (tiempo_actual - ultimo_fallido).total_seconds() / 60 >= tiempo_bloqueo:
                print("|Tiempo de bloqueo finalizado -> Reseteando tiempo de bloqueo.")
                session.pop('intentos_fallidos', None)
                session.pop('ultimo_fallido', None)
                intentos_fallidos = 0

            # Si el usuario está bloqueado, muestra un mensaje
            if intentos_fallidos >= max_intentos_fallidos:
                tiempo_restante = timedelta(minutes=tiempo_bloqueo) - (tiempo_actual - ultimo_fallido)
                segundos_restantes = int(tiempo_restante.total_seconds())
                flash(f'Demasiados intentos fallidos. Inténtalo de nuevo en {segundos_restantes} segundos.','danger')
                return redirect(url_for('auth_bp.login'))

        # print(f'POST | usuario: {usuario} | contraseña: {contrasena}')
        user = Usuario.query.filter_by(usuario=usuario).first()

        # Si existe usaurio y la contraseña coincide
        if user and user.contrasena == contrasena:
            # Restablecer el contador de intentos fallidos al iniciar sesión exitosamente
            session.pop('intentos_fallidos', None)
            session.pop('ultimo_fallido', None)
            login_user(user)  # remember=form.remember_me.data)
            return redirect(url_for('main_bp.home'))
        else:
            # Incrementar el contador de intentos fallidos
            if 'intentos_fallidos' in session:
                session['intentos_fallidos'] += 1
            else:
                session['intentos_fallidos'] = 1
            session['ultimo_fallido'] = datetime.now(timezone.utc)
            flash(f'Credenciales invalidas. Intente nuevamente. (Intentos restantes: { max_intentos_fallidos - session["intentos_fallidos"]})',
                  'warning')

    print('get login')
    return render_template('auth/login.html', form=formulario)


@auth_bp.route('/logout')
@login_required
def logout():
    print('Desloguear Usuario: ', current_user.usuario)
    logout_user()
    return redirect(url_for('auth_bp.login'))
