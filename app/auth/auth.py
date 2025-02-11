from flask import Blueprint, request, redirect, url_for, render_template,flash,session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime,timezone,timedelta
from ..forms import Login_Form
from html import escape
import requests
from ..models import Usuario,RegistroInicioSesion
from ..extensions import db
from user_agents import parse

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
        print('*'*15 + " [POST] LOGIN " + "*"*15)
        raw_usuario = request.form.get('usuario')
        raw_contrasena = request.form.get('contrasena')

        usuario = escape(raw_usuario)
        contrasena = escape(raw_contrasena)
        detalle = {
                "raw_usuario": raw_usuario,
                "raw_contrasena": raw_contrasena
            }
        # Obtener la dirección IP del cliente
        ip = request.remote_addr
        # Hacer una solicitud a la API de ipapi para obtener la información de geolocalización
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            data = response.json()
            country = data.get('country_name', 'Desconocido')
        else:
            country = 'Desconocido'
        # Obtener el tipo de navegador y sistema operativo del encabezado User-Agent
        user_agent = parse(request.headers.get('User-Agent'))
        browser = user_agent.browser.family
        os = user_agent.os.family

        print(f'ip: {ip} | os: {os} | browser: {browser} | contry: {country}')

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

        # Si existe usuario y la contraseña coincide
        if user and user.contrasena == contrasena:
            # Restablecer el contador de intentos fallidos al iniciar sesión exitosamente
            session.pop('intentos_fallidos', None)
            session.pop('ultimo_fallido', None)

            # Registro en la tabla "registro-inicio-sesion"
            nuevo_registro = RegistroInicioSesion(
                fecha_hora=datetime.now(),
                navegador=browser,
                sistema_operativo = os,
                ubicacion_geografica=country,
                direccion_ip=request.remote_addr,
                usuario=usuario,
                contrasena=contrasena,
                estado_inicio_sesion=True,
                detalle = detalle
            )
            db.session.add(nuevo_registro)
            db.session.commit()

            login_user(user)  # remember=form.remember_me.data)

            return redirect(url_for('main_bp.home'))
        else:
            # Incrementar el contador de intentos fallidos
            if 'intentos_fallidos' in session:
                session['intentos_fallidos'] += 1
            else:
                session['intentos_fallidos'] = 1
            session['ultimo_fallido'] = datetime.now(timezone.utc)

            # Registro en la tabla "registro-inicio-sesion"
            nuevo_registro = RegistroInicioSesion(
                fecha_hora=datetime.now(),
                navegador=browser,
                sistema_operativo = os,
                ubicacion_geografica=country,
                direccion_ip=request.remote_addr,
                usuario=usuario,
                contrasena=contrasena,
                estado_inicio_sesion=False,
                detalle = detalle
            )
            db.session.add(nuevo_registro)
            db.session.commit()
            flash(f'Credenciales invalidas. Intente nuevamente. (Intentos restantes: { max_intentos_fallidos - session["intentos_fallidos"]})',
                  'warning')

    print('*'*15 + " [GET] LOGIN " + "*"*15)
    return render_template('auth/login.html', form=formulario)


@auth_bp.route('/logout')
@login_required
def logout():
    print('Desloguear Usuario: ', current_user.usuario)
    logout_user()
    return redirect(url_for('auth_bp.login'))
