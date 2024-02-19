

""" class Gasto(db.Model):
    __tablename__ = 'gasto'
    gasto_id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)

    # Datos de empresa proveedora.
    prov_empresa =  db.Column(db.String(255), nullable=True) 
    prov_documento = db.Column(db.String(50), nullable=True)
    prov_folio = db.Column(db.Integer, nullable=True)

    tipo = db.Column(db.String(255), nullable=False) # Tipo de gasto
    descripcion =  db.Column(db.String(255), nullable=False) # Tipo de gasto
    cantidad =  db.Column(db.Integer, nullable=False) # Tipo de gasto
    unidad =  db.Column(db.String(255), nullable=False) # Tipo de gasto

    comentario =  db.Column(db.String(255), nullable=True) # Tipo de gasto
    # Foreaneas
    periodo_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
 """
