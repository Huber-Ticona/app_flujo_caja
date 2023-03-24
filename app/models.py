from .extensions import db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(255), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
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

    def get_id(self):
        return str(self.usuario_id)


class Empresa(db.Model):
    __tablename__ = 'empresa'
    empresa_id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(255))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'))


class IngresoGasto(db.Model):
    __tablename__ = 'ingreso_gasto'
    ingreso_gasto_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    ingreso = db.Column(db.Integer)
    gasto = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.empresa_id'))
