from ..models import Empresa

def get_empresa(id):
    print('Obteniendo empresa: ',id)
    empresa = Empresa.query.filter_by(empresa_id=id).first()
    print(1)
    