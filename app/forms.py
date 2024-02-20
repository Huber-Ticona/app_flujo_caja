from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,DateField,SelectField,HiddenField
from wtforms.validators import InputRequired, Email, Length


class Login_Form(FlaskForm):
    usuario = StringField('username')
    contrasena = StringField('contraseña')


class Crear_Empresa_Form(FlaskForm):
    nombre_empresa = StringField('nombre_empresa', validators=[
                                 InputRequired(), Length(min=4)])
    rubro_empresa = StringField('rubro_empresa')


class Crear_Periodo_Form(FlaskForm):
    periodo_fiscal = StringField('periodo_fiscal')
    inicio = StringField('inicio')
    termino = StringField('termino')

class Crear_Gasto_Form(FlaskForm):

    fecha = DateField('fecha', validators=[InputRequired()])

    # Datos de empresa proveedora.
    prov_empresa = StringField('prov_empresa')

    prov_documento = SelectField('prov_documento', choices=[('factura', 'Factura'), ('boleta', 'Boleta'), ('guia', 'Guia')])
    prov_folio = IntegerField('prov_folio')

    tipo = StringField('tipo',validators=[InputRequired()])

  
    
    comentario = StringField('comentario') # Tipo de gasto
    # Foreaneas
    periodo_id =IntegerField('periodo_id') # Tipo de gasto

""" APLICACION FORM """
""" class Aplicacion(db.Model):
    __tablename__ = 'aplicacion'
    aplicacion_id = db.Column(db.Integer, primary_key=True)
    
    fecha = db.Column(db.Date, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)

    detalle = db.Column(db.JSON, nullable=False) #(insumo,cantidad, unidad (saco ,litro))

    aplicador = db.Column(db.String(255), nullable=True)
    comentario = db.Column(db.String(255), nullable=False)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto """
class Crear_aplicacion_form(FlaskForm):

    fecha = DateField('fecha', validators=[InputRequired()])
    lugar = StringField('prov_empresa')
    nave = SelectField('prov_documento', choices=[('factura', 'Factura'), ('boleta', 'Boleta'), ('guia', 'Guia')])
    prov_folio = IntegerField('prov_folio')

    tipo = StringField('tipo',validators=[InputRequired()])

  
    
    comentario = StringField('comentario') # Tipo de gasto
    # Foreaneas
    periodo_id =IntegerField('periodo_id') # Tipo de gasto


""" class Empleado(db.Model):
    __tablename__ = 'empleado'
    empleado_id = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.JSON, nullable=False) #{ nombre , apellido, telefono,estado(activo,inactivo),etc}
    empresa_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
     """
class Empleado_form(FlaskForm):
    url = "/api/trabajadores/registrar"
    detalle = HiddenField('detalle',name="detalle",default='')
    empresa_id = IntegerField('empresa_id')
    tabla = ["nombre","apellido","telefono","estado"]
    tablas = {"detalle" : {
                "relacion":"uno", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle",
                "inputs" : [
                    {"name":"nombre", "type":"text"},
                    {"name":"apellido", "type":"text"},
                    {"name":"telefono", "type":"number"},
                    {"name":"estado", "type":"text"}
                    ]
            } ,
            }

