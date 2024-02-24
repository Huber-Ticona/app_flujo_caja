from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,DateField,SelectField,HiddenField,DateTimeField
from wtforms.validators import InputRequired, Email, Length
import json

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
""" class Gasto(db.Model):
    __tablename__ = 'gasto'
    gasto_id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.DateTime, nullable=False)

    # Datos de empresa proveedora.
    prov_empresa =  db.Column(db.String(255), nullable=True) 
    prov_documento = db.Column(db.String(50), nullable=True)
    prov_folio = db.Column(db.Integer, nullable=True)

    tipo = db.Column(db.String(255), nullable=False) # Tipo de gasto
    detalle = db.Column(db.JSON, nullable=False) # Tipo de gasto (descripcion,cantidad,unidad,precio,etc)
    total = db.Column(db.Integer, nullable=False) # Tipo de gasto
    comentario =  db.Column(db.String(255), nullable=True) # Tipo de gasto
    # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto """
class Gasto_Form(FlaskForm):

    fecha = DateTimeField('fecha', validators=[InputRequired()])

    # Datos de empresa proveedora.
    prov_empresa = StringField('prov_empresa')
    prov_documento = SelectField('prov_documento', choices=[('factura', 'Factura'), ('boleta', 'Boleta'), ('guia', 'Guia')])
    prov_folio = IntegerField('prov_folio')
    tipo = StringField('tipo',validators=[InputRequired()])
    detalle = HiddenField("detalle")
    comentario = StringField('comentario') 
    # Foreaneas
    periodo_id =IntegerField('periodo_id') 
    endpoint = "/api/gastos"
    tablas = {"detalle":{
        
    }}

""" Riego form  class Riego(db.Model):
    __tablename__ = 'riego'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)
    minutos = db.Column(db.Integer, nullable=False)
    regador = db.Column(db.String(100), nullable=True)

    comentario = db.Column(db.String(255), nullable=True)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto """
class Riego_form(FlaskForm):
    fecha = DateTimeField('fecha', validators=[InputRequired()])
    lugar = SelectField('lugar', choices=[('Km 17 Parcela', 'Km 17 Parcela'), ('Km 17 Olivo', 'Km 17 Olivo'), ('Km 28 Sobraya', 'Km 28 Sobraya')])
    nave = SelectField('nave', choices=[('Nave 1', 'Nave 1'), ('Nave 2', 'Nave 2'), ('Nave 3', 'Nave 3')])
    minutos = IntegerField('minutos')
    regador = StringField('regador')

    comentario = StringField('comentario') # Tipo de gasto
    # Foreaneas
    periodo_id = HiddenField('periodo_id') # Tipo de gasto
    endpoint = "/api/riegos"
    tablas = {}

""" APLICACION FORM """
""" class Aplicacion(db.Model):
    __tablename__ = 'aplicacion'
    id = db.Column(db.Integer, primary_key=True)
    
    fecha = db.Column(db.Date, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)

    detalle = db.Column(db.JSON, nullable=False) #(insumo,cantidad, unidad (saco ,litro))

    aplicador = db.Column(db.String(255), nullable=True)
    comentario = db.Column(db.String(255), nullable=False)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto"""
class Aplicacion_form(FlaskForm):

    fecha = DateTimeField('fecha', validators=[InputRequired()])
    lugar = SelectField('lugar', choices=[('Km 17 Parcela', 'Km 17 Parcela'), ('Km 17 Olivo', 'Km 17 Olivo'), ('Km 28 Sobraya', 'Km 28 Sobraya')])
    nave = SelectField('nave', choices=[('Nave 1', 'Nave 1'), ('Nave 2', 'Nave 2'), ('Nave 3', 'Nave 3')])
    
    detalle = HiddenField("detalle")

    aplicador = StringField('aplicador')
    comentario = StringField('comentario') # Tipo de gasto
    # Foreaneas
    periodo_id =HiddenField('periodo_id') # Tipo de gasto
    endpoint = "/api/aplicaciones"
    tablas = {"detalle" : {
                "relacion":"muchos", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle",
                "inputs" : [
                    {"name":"insumo", "type":"text"},
                    {"name":"cantidad", "type":"number"},
                    {"name":"unidad", "type":"text",
                     "choices":["Mili-litro (ML)","kilogramo (KG)","Litro (LTS)" ,"Mili-gramo (MG)"]
                     },
                    ]
            } ,
            }
    show_in_table = ["fecha","lugar","nave","detalle","aplicador"]
    


""" class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=True)
    fecha_retiro = db.Column(db.DateTime, nullable=True)
    detalle = db.Column(db.JSON, nullable=False) #{ nombre , apellido, telefono,estado(activo,inactivo),etc}
    empresa_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
     """
class Empleado_form(FlaskForm):
    fecha_ingreso = DateTimeField('fecha_ingreso', validators=[InputRequired()])
    
    fecha_retiro = DateTimeField('fecha_retiro', validators=[InputRequired()])
    
    detalle = HiddenField('detalle',name="detalle",default='')
    empresa_id = HiddenField('empresa_id')
    endpoint = "/api/trabajadores"
    tabla = ["nombre","apellido","telefono","estado"]
    tablas = {"detalle" : {
                "relacion":"uno", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle",
                "inputs" : [
                    {"name":"nombre", "type":"text"},
                    {"name":"apellido", "type":"text"},
                    {"name":"telefono", "type":"number"},
                    {"name":"estado", "type":"text" ,"choices":["ACTIVO","INACTIVO"]}
                    ]
            } ,
            }
