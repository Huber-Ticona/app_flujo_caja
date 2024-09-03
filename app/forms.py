from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,DateField,SelectField,HiddenField,DateTimeField
from wtforms.validators import InputRequired, Email, Length
import json
from datetime import datetime,timedelta
from .models import Empleado


class Login_Form(FlaskForm):
    usuario = StringField('username')
    contrasena = StringField('contraseña')


class Crear_Empresa_Form(FlaskForm):
    nombre_empresa = StringField('nombre_empresa', validators=[
                                 InputRequired(), Length(min=4)])
    rubro_empresa = StringField('rubro_empresa')
    parametros = HiddenField('parametros' , default= {})


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

    detalle = db.Column(db.JSON, nullable=False) # Tipo de gasto (descripcion,cantidad,unidad,precio,etc)
    total = db.Column(db.Integer, nullable=False) # Tipo de gasto
    comentario =  db.Column(db.String(255), nullable=True) # Tipo de gasto
    # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto """

class Gasto_Form(FlaskForm):

    fecha = DateTimeField('fecha', validators=[InputRequired()],default=datetime.now())

    # Datos de empresa proveedora.
    prov_empresa = StringField('prov_empresa')
    prov_documento = SelectField('prov_documento', choices=[('factura', 'Factura'), ('boleta', 'Boleta'), ('guia', 'Guia')])
    prov_folio = IntegerField('prov_folio',default=0)
    detalle = HiddenField("detalle")
    total = IntegerField('total',validators=[InputRequired()],default=0)
    comentario = StringField('comentario') 
    # Foreaneas
    periodo_id =HiddenField('periodo_id',validators=[InputRequired()])
    endpoint = "/api/gastos"
    tablas = {"detalle":{
        "relacion":"muchos",
        "field":"detalle",
        "inputs":[
            {"name":"cantidad" ,"type": "number","default":1 },
            {"name":"unidad", "type":"text" ,
             "choices":["UND","SACO","CAJA","PACK (Bolsa)","kilogramo (KG)","Litro (LT)" ,"Mili-gramo (MG)","Mili-litro (ML)"]
            },
            {"name":"descripcion", "type":"text"},
            {"name":"precio_unitario", "type":"number","default":0 ,
             "onchange":{"target":"precio_total",
                          "result":["cantidad","*","precio_unitario"]}},
            {"name":"precio_total", "type":"number","default":0},
            {"name":"tipo", "type":"text" ,
             "choices":["HERRAMIENTA","MATERIAL","FERTILIZANTE","CONTROL-PLAGAS","MANTENCION-AUTOMOTRIZ","ALIMENTACION"]
            }
        ],
        
    }}
    show_in_table = ["fecha","total","detalle","prov_empresa","prov_documento","prov_folio","comentario"]

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

parcelas = ['Km 17 Parcela', 'Km 17 Olivo','Km 28 Sobraya']
naves = ['Nave 1','Nave 2','Nave 3','Nave 1 y 2','Nave 2 y 3','Nave 1 y 3','Nave 1, 2 y 3']

class Riego_form(FlaskForm):
    fecha = DateTimeField('fecha', validators=[InputRequired()],default=datetime.now())
    lugar = SelectField('lugar')
    nave = SelectField('nave')
    minutos = IntegerField('minutos',default=30)
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
    tipo_aplicacion = db.Column(db.String(255), nullable=False)
    comentario = db.Column(db.String(255), nullable=False)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto"""


class Aplicacion_form(FlaskForm):

    fecha = DateTimeField('fecha', validators=[InputRequired()],default=datetime.now())
    lugar = SelectField('lugar', choices=[(item, item) for item in parcelas])
    nave = SelectField('nave')
    
    detalle = HiddenField("detalle")

    aplicador = StringField('aplicador')
    tipo_aplicacion = SelectField('tipo_aplicacion',choices=[('VIA RIEGO', 'VIA RIEGO'), ('VIA FOLIAR', 'VIA FOLIAR')])
    comentario = StringField('comentario') # Tipo de gasto
    # Foreaneas
    periodo_id =HiddenField('periodo_id') # Tipo de gasto
    endpoint = "/api/aplicaciones"
    tablas = {"detalle" : {
                "relacion":"muchos", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle",
                "inputs" : [
                    {"name":"insumo", "type":"text"},
                    {"name":"cantidad_x_riego", "type":"number"},
                    {"name":"unidad_de_cantidad", "type":"text",
                     "choices":["Mili-litro (ML)","kilogramo (KG)","Litro (LTS)" ,"Mili-gramo (MG)"]
                     },
                    {"name":"total_aplicado", "type":"number"},
                    {"name":"unidad_de_total", "type":"text",
                     "choices":["Mili-litro (ML)","kilogramo (KG)","Litro (LTS)" ,"Mili-gramo (MG)"]
                     },
                    ]
            } ,
            }
    show_in_table = ["fecha","lugar","nave","detalle","aplicador","tipo_aplicacion"]
    


""" class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=True)
    fecha_retiro = db.Column(db.DateTime, nullable=True)
    detalle = db.Column(db.JSON, nullable=False) #{ nombre , apellido, telefono,estado(activo,inactivo),etc}
    empresa_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
     """
class Empleado_form(FlaskForm):
    fecha_ingreso = DateTimeField('fecha_ingreso', validators=[InputRequired()],default=datetime.now())
    
    fecha_retiro = DateTimeField('fecha_retiro', default=lambda: datetime.now() + timedelta(days=5*365))
    
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

""" class PagoPersonal(db.Model):
    __tablename__ = 'pago_personal'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    personal = db.Column(db.String(100), nullable=False)
    pago = db.Column(db.Integer, nullable=False)
    periodo_id = db.Column(db.Integer, nullable=False) """
class PagoPersonal_form(FlaskForm):
    fecha = DateTimeField('fecha', validators=[InputRequired()],default=datetime.now())
    
    personal = SelectField('personal')
    pago = IntegerField('pago',default=0)
    periodo_id = HiddenField("detalle")

    endpoint = "/api/pagos_personal"
    tablas = {}
    show_in_table = ["fecha","personal","pago"]


""" class RegistroLaboral(db.Model):
    __tablename__ = 'registro_laboral'
    id = db.Column(db.Integer, primary_key=True) 
    detalle = db.Column(db.JSON, nullable=False)
    periodo_id = db.Column(db.Integer, nullable=False) """

class RegistroLaboral_form(FlaskForm):
    detalle = HiddenField('detalle', )
    periodo_id = HiddenField("periodo_id")

    endpoint = "/api/registros_laborales"
    tablas = {"detalle" : {
                "relacion":"uno", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle",
                "inputs" : [
                    {"name":"fecha", "type":"datetime-local" ,"default":str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))},
                    {"name":"descripcion", "type":"text"},
                    ]
            } ,
            }
    show_in_table = ["detalle","periodo_id"]


""" __tablename__ = "embarque"
    embarque_id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)
    detalle = db.Column(db.JSON)
    detalle_totales = db.Column(db.JSON)  # total_terreno , total_procesado
    extra = db.Column(db.JSON)

    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.periodo_id')) """
class Embarque_form(FlaskForm):


    fecha = DateField('fecha', validators=[InputRequired()],default=datetime.now())
    
    detalle = HiddenField("detalle")
    detalle_totales = HiddenField("detalle_totales")
    extra = HiddenField("extra")
    # Foreaneas
    periodo_id =HiddenField('periodo_id') 

    endpoint = "/api/embarques"
    tablas = {"detalle" : {
                "relacion":"muchos", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle",
                "inputs" : [
                    {"name":"parcela", "type":"text",
                     "choices":parcelas
                     },
                    {"name":"nave", "type":"text",
                     "choices":["1","2","3" ]
                     },
                    {"name":"hortaliza", "type":"text",
                     "choices":["Tomate Bola","Tomate Cherry"]
                     },
                    {"name":"total","type":"number"}
                    ]
            } ,
            "detalle_totales" : {
                "relacion":"muchos", # uno: uno a uno | muchos: uno a muchos
                "field": "detalle_totales",
                "inputs" : [
                    {"name":"total_terreno", "type":"number",},
                    {"name":"total_procesado", "type":"number"},
                    {"name":"hortaliza", "type":"text",
                     "choices":["Tomate Bola","Tomate Cherry"]
                     }
                   
                    ]
            } ,
            "extra" : {
                "relacion":"uno", # uno: uno a uno | muchos: uno a muchos
                "field": "extra",
                "inputs" : [
                    {"name":"observacion", "type":"text"},
                    ]
            } ,
            }
    show_in_table = ["detalle","detalle_totales","extra"]



class Cosecha_form(FlaskForm):

    fecha = DateTimeField('fecha', validators=[InputRequired()], default=datetime.now())
    lugar = SelectField('lugar')
    nave = SelectField('nave')

    detalle_totales = HiddenField("detalle_totales")
    detalle = HiddenField("detalle")
    transporte = HiddenField("transporte")
    extra = HiddenField("extra")

    # Foreaneas
    periodo_id =HiddenField('periodo_id') # Tipo de gasto
    endpoint = "/api/cosechas"
    tablas = {
        "detalle_totales":{
            "titulo":"Cosecha total a granel",
            "relacion":"muchos",
            "field": "detalle_totales",
            "inputs":[
                {"name":"hortaliza", "type":"text" , "choice_list_name":"hortaliza"},
                {"name":"unidad", "type":"text", "choice_list_name":"unidad_de_comercio"},
                {"name":"total_terreno", "type":"number"},
                {"name":"total_procesado", "type":"number"}
            ]
        },
        "detalle": {
            "titulo": "Proceso/Seleccion",
            "relacion": "muchos",
            "field": "detalle",
            "inputs": [
                {"name": "hortaliza", "type": "text",
                 "choice_list_name":"hortaliza"},
                {"name": "calibre", "type": "text"},
                {"name": "unidad", "type": "text",
                 "choice_list_name":"unidad_de_comercio"},
                {"name": "cantidad", "type": "number"}]
        },
        "transporte": {
            "titulo": "Transporte a packing",
            "relacion": "muchos",
            "field": "transporte",
            "inputs" : [
                {"name":"vehiculo", "type": "text","choice_list_name":"vehiculo"},
                {"name":"nro_gamelas", "type": "number"},
            ]
        },
        "extra":{
            "relacion":"uno",
            "field":"extra",
            "inputs":[
                {"name" : "comentario" , "type":"text"}
            ]
        }
    }
    show_in_table = ["fecha","lugar","nave","detalle_totales"]

class Embarque_form2(FlaskForm):
    x =  0
    detalle = HiddenField("detalle")
    tablas = {
        "detalle": {
            "relacion": "muchos",
            "field": "detalle",
            "inputs": [
                {"name":"calibre", "type": "text"}
            ]
        }
    }
