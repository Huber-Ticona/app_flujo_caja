from .extensions import db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(255), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(10), nullable=False)
    nombre_completo = db.Column(db.String(255))

    @classmethod
    # cls hace referencia a la misma clase. En este caso a Usuario.
    # Al heredar de db.Model posee .query y .get para realizar consultas a en la tabla usuario.
    def get_by_id(cls, id):
        return cls.query.get(int(id))

    def get_id(self):
        return str(self.usuario_id)

    def is_active(self):
        # Aquí puedes implementar la lógica para determinar si el usuario está activo o no.
        # Por ejemplo, si tienes un campo en la tabla usuario que indica si el usuario está activo,
        # puedes devolver ese valor.
        return True

    def is_authenticated(self):
        # Aquí puedes implementar la lógica para determinar si el usuario ha iniciado sesión y ha sido autenticado correctamente.
        # Por ejemplo, si has verificado las credenciales del usuario en la base de datos, puedes devolver True.
        return True

    def is_anonymous(self):
        return False
    def get_full_name(cls):
        return str(cls.nombre_completo)



class Empresa(db.Model):
    __tablename__ = 'empresa'
    empresa_id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(255))
    rubro_empresa = db.Column(db.String(255))
    parametros = db.Column(db.JSON, nullable=False) #{ "ID_PARAM" : {"NOMBRE" : "HORTALIZAS","TIPO":"(lista,constante,json)" ,"VALOR": []}}
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))
    def update_from_dict(self, data):
        for key, value in data.items():
            print(f"|MODEL| Key : {key} -> value: {value} |actualizado")
            setattr(self, key, value)


class Periodo(db.Model):
    __tablename__ = 'periodo'
    periodo_id = db.Column(db.Integer, primary_key=True)

    # limitado a 4 digitos. evitando negativos.
    periodo_fiscal = db.Column(db.String(4), nullable=False)

    inicio = db.Column(db.Date, nullable=False)
    termino = db.Column(db.Date, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.empresa_id'))

    
class Embarque(db.Model):
    __tablename__ = "embarque"
    embarque_id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)
    detalle = db.Column(db.JSON)
    detalle_totales = db.Column(db.JSON)  # total_terreno , total_procesado
    extra = db.Column(db.JSON)

    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.periodo_id'))
    def to_json(self):
        return {
            'id': self.embarque_id,
            'fecha': self.fecha,
            'detalle': self.detalle,
            'detalle_totales': self.detalle_totales,
            'extra': self.extra,
            'periodo_id': self.periodo_id
        }
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class Liquidacion(db.Model):
    __tablename__ = 'liquidacion'
    liquidacion_id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)
    detalle = db.Column(db.JSON)
    detalles_extras = db.Column(db.JSON)  # total_terreno , total_procesado # vendedor? stefano u/o danilo , etc
    total_venta = db.Column(db.Integer)
    total_descuento = db.Column(db.Integer)
    total_pago = db.Column(db.Integer)

    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.periodo_id'))


class Gasto(db.Model):
    __tablename__ = 'gasto'
    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.DateTime, nullable=False)

    # Datos de empresa proveedora.
    prov_empresa =  db.Column(db.String(255), nullable=True) 
    prov_documento = db.Column(db.String(50), nullable=True)
    prov_folio = db.Column(db.Integer, nullable=True)

    detalle = db.Column(db.JSON, nullable=False) # (descripcion,cantidad,unidad,precio,tipo_gasto)
    total = db.Column(db.Integer, nullable=False) # 
    comentario =  db.Column(db.String(255), nullable=True) # 
    # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) #
    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'prov_empresa': self.prov_empresa,
            'prov_documento': self.prov_documento,
            'prov_folio': self.prov_folio,
            'detalle': self.detalle,
            'total': self.total,
            'comentario': self.comentario,
            'periodo_id': self.periodo_id
        }
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

class Aplicacion(db.Model):
    __tablename__ = 'aplicacion'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)
    detalle = db.Column(db.JSON, nullable=False) #(insumo,cantidad, unidad (saco ,litro))
    aplicador = db.Column(db.String(255), nullable=True)
    tipo_aplicacion = db.Column(db.String(255), nullable=False)
    comentario = db.Column(db.String(255), nullable=True)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'lugar': self.lugar,
            'nave': self.nave,
            'detalle': self.detalle,
            'aplicador': self.aplicador,
            'tipo_aplicacion': self.tipo_aplicacion,
            'comentario': self.comentario,
            'periodo_id': self.periodo_id,
        }
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

class Riego(db.Model):
    __tablename__ = 'riego'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)
    minutos = db.Column(db.Integer, nullable=False)
    regador = db.Column(db.String(100), nullable=True)

    comentario = db.Column(db.String(255), nullable=True)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) 
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)
    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'lugar': self.lugar,
            'nave': self.nave,
            'minutos': self.minutos,
            'regador': self.regador,
            'comentario': self.comentario,
            'periodo_id': self.periodo_id
        }

class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=True)
    fecha_retiro = db.Column(db.DateTime, nullable=True)
    
    """ Pendiente (quisas) """
    """ nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.Integer, nullable=True) """

    detalle = db.Column(db.JSON, nullable=False) #{ nombre , apellido, telefono,estado(activo,inactivo),etc}
    empresa_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_json(self):
        return {
            'id': self.id,
            'fecha_ingreso': self.fecha_ingreso,
            'fecha_retiro': self.fecha_retiro,
            'detalle': self.detalle,
            'empresa_id': self.empresa_id
        }
class PagoPersonal(db.Model):
    __tablename__ = 'pago_personal'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    personal = db.Column(db.String(100), nullable=False)
    pago = db.Column(db.Integer, nullable=False)
    periodo_id = db.Column(db.Integer, nullable=False)
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'personal': self.personal,
            'pago': self.pago,
            'periodo_id': self.periodo_id
        }
class RegistroLaboral(db.Model):
    __tablename__ = 'registro_laboral'
    id = db.Column(db.Integer, primary_key=True) 
    detalle = db.Column(db.JSON, nullable=False) #(fecha,descripcion)
    periodo_id = db.Column(db.Integer, nullable=False)

    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_json(self):
        return {
            'id': self.id,
            'detalle': self.detalle,
            'periodo_id': self.periodo_id
        }



class Cosecha(db.Model):
    __tablename__ = 'cosecha'
    id = db.Column(db.Integer, primary_key=True) 
    fecha = db.Column(db.DateTime, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)

    detalle_totales = db.Column(db.JSON, nullable=False ) #(total_terrreno,total_procesado,unidad, hortaliza)
    detalle = db.Column(db.JSON, nullable=False ) #(calibre,cantidad)
    transporte = db.Column(db.JSON, nullable=False ) #(vehiculo,cantidad)

    extra = db.Column(db.JSON, nullable=False ) #anotaciones
    periodo_id = db.Column(db.Integer, nullable=False)
    packing_id = db.Column(db.Integer, nullable=False) #v.1.0.9
    liquidacion_id = db.Column(db.Integer, nullable=True) #v.1.0.9
    
    extra2 = [[1,2,3] , ["hola","mundo"] , {"grafico" : 'fecha'}]

    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,#.isoformat()
            'lugar': self.lugar,
            'nave':self.nave,
            'detalle': self.detalle,
            'detalle_totales': self.detalle_totales,
            'transporte': self.transporte,
            'extra': self.extra,
            'periodo_id': self.periodo_id,
            'packing_id': self.packing_id,
            'liquidacion_id': self.liquidacion_id  #v.1.0.9
        }




class Movimiento(db.Model):
    __tablename__ = 'movimiento'
    id = db.Column(db.Integer, primary_key=True) 
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(255))
    canal_sucursal = db.Column(db.String(255))
    cargo = db.Column(db.Integer)
    abono = db.Column(db.Integer)
    saldo = db.Column(db.Integer)

    gasto_id = db.Column(db.Integer, nullable=True,default=0)

# MODELOS DE AUDITORIA
class RegistroInicioSesion(db.Model):
    __tablename__ = 'registro_inicio_sesion'

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    usuario = db.Column(db.String(255))
    contrasena = db.Column(db.String(255))
    direccion_ip = db.Column(db.String(255), nullable=False)
    ubicacion_geografica = db.Column(db.String(255))
    navegador = db.Column(db.String(255))
    sistema_operativo = db.Column(db.String(255))
    estado_inicio_sesion = db.Column(db.Boolean, nullable=False)
    duracion_sesion = db.Column(db.Integer)
    detalle = db.Column(db.JSON)

# Modelo Packing
class Packing(db.Model):
    __tablename__ = 'packing'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    detalle = db.Column(db.JSON) #CALIBRE-NAVE-CANTIDAD
    comentario = db.Column(db.String(255), nullable=True)
    # Foreaneas
    cosechas = db.Column(db.JSON)
    periodo_id = db.Column(db.Integer, nullable=False)
    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'cosechas':self.cosechas,
            'detalle':self.detalle,
            'comentario':self.comentario,
            'periodo_id':self.periodo_id
        }
    
# Modelo Doc_Venta
""" class Doc_Venta(db.Model):
    __tablename__ = 'doc_venta'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    folio = db.Column(db.Integer, nullable=False)
    detalle = db.Column(db.JSON) #CALIBRE-NAVE-CANTIDAD

    comentario = db.Column(db.String(255), nullable=True)
    # Foreaneas
    packings = db.Column(db.JSON) # [Packings]
    periodo_id = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'cosechas':self.cosechas,
            'detalle':self.detalle,
            'comentario':self.comentario,
            'periodo_id':self.periodo_id
        } """