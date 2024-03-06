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
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))



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

    tipo = db.Column(db.String(255), nullable=False) # Tipo de gasto
    detalle = db.Column(db.JSON, nullable=False) # Tipo de gasto (descripcion,cantidad,unidad,precio,etc)
    total = db.Column(db.Integer, nullable=False) # Tipo de gasto
    comentario =  db.Column(db.String(255), nullable=True) # Tipo de gasto
    # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
    def to_json(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'prov_empresa': self.prov_empresa,
            'prov_documento': self.prov_documento,
            'prov_folio': self.prov_folio,
            'tipo': self.tipo,
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
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
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




