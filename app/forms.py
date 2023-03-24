from flask_wtf import FlaskForm
from wtforms import StringField

class Login_Form(FlaskForm):
    usuario = StringField('username')
    contrasena = StringField('contraseña')
