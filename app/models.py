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
    gasto_id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)

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

class Aplicacion(db.Model):
    __tablename__ = 'aplicacion'
    aplicacion_id = db.Column(db.Integer, primary_key=True)
    
    fecha = db.Column(db.Date, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)

    detalle = db.Column(db.JSON, nullable=False) #(insumo,cantidad, unidad (saco ,litro))

    aplicador = db.Column(db.String(255), nullable=True)
    comentario = db.Column(db.String(255), nullable=False)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto

class Riego(db.Model):
    __tablename__ = 'riego'
    riego_id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    nave = db.Column(db.String(100), nullable=False)
    minutos = db.Column(db.Integer, nullable=False)
    regador = db.Column(db.String(100), nullable=True)

    comentario = db.Column(db.String(255), nullable=False)
     # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
    def update_from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

class Empleado(db.Model):
    __tablename__ = 'empleado'
    empleado_id = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.JSON, nullable=False) #{ nombre , apellido, telefono,estado(activo,inactivo),etc}
    empresa_id = db.Column(db.Integer, nullable=False) # Tipo de gasto

""" class PagoPersonal(db.Model):
    __tablename__ = 'pago_personal'
    gasto_id = db.Column(db.Integer, primary_key=True)

class RegistroLaboral(db.Model):
    __tablename__ = 'registro_laboral'
    gasto_id = db.Column(db.Integer, primary_key=True) """




