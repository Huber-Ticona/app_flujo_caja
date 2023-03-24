from flask import Blueprint,request,redirect,url_for,render_template
from flask_login import login_user
from werkzeug.security import check_password_hash

from ..forms import Login_Form
from html import escape

from ..models import Usuario

auth_bp = Blueprint('auth_bp',__name__, static_folder='static',template_folder='templates')



@auth_bp.route('/dashboard')
def cuenta():

    return 'mi cuenta'

@auth_bp.route('/login', methods=['GET' ,'POST'])
def login():
    formulario = Login_Form()

    # Verifica peticion POST y valida el formulario
    if formulario.validate_on_submit():

        usuario = escape(request.form.get('usuario'))
        contrasena = escape(request.form.get('contrasena'))

        #print(f'POST | usuario: {usuario} | contraseña: {contrasena}')
        user = Usuario.query.filter_by(usuario=usuario).first()
        
        # Si existe usaurio y la contraseña coincide
        if user and user.contrasena == contrasena :
            print('xd')
            login_user(user)# remember=form.remember_me.data)
            return redirect(url_for('main_bp.home'))
        
    print('get login')
    return render_template('auth/login.html', form = formulario)

