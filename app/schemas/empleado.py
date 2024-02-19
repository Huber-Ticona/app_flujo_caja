
import strawberry
from typing import List,Optional
from ..models import Empleado
from ..extensions import db

""" class Empleado(db.Model):
    __tablename__ = 'empleado'
    empleado_id = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.JSON, nullable=False) #{ nombre , apellido, telefono,estado(activo,inactivo),etc}
    empresa_id = db.Column(db.Integer, nullable=False) # Tipo de gasto
 """