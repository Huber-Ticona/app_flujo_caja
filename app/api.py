from flask import Blueprint,render_template,request,redirect,url_for,jsonify,session,Response,abort
from .forms import Crear_Gasto_Form
from .models import Gasto,Riego
from .extensions import get_fields_and_types,model_to_dict2,db
from html import escape
from datetime import datetime
import json

api_bp = Blueprint('api_bp' , __name__,template_folder='templates',static_folder='static')

@api_bp.route('/gasto/<int:periodo_id>')
def obtener_gasto(periodo_id=None):

    return  render_template('pages/gasto/gasto.html',periodo_id=periodo_id)

@api_bp.route('/gasto/<int:periodo_id>/lista')
def lista_gasto(periodo_id=None):
    gastos = Gasto.query.filter_by(periodo_id=periodo_id).all()
    
    print(f"|{'-'*10} Lista de gastos | periodo: {periodo_id} {'-'*10}| ")
    print(f"|Gastos: {gastos}")
    print(f"|{'-'*10} END {'-'*10}|")
    return  render_template('pages/gasto/lista_gasto.html',gastos=gastos)

@api_bp.route('/gasto/<int:periodo_id>/registrar' , methods=['GET', 'POST'])
def registrar_gasto(periodo_id=None):
    model_gasto_json = model_to_dict2(Gasto)
    list_gasto_form = get_fields_and_types(Gasto)

    print("(Form model_to_dict) : ",model_gasto_json)

    if request.method == 'POST':
        print("|post registrar gasto ...")
        data = request.get_json()
        print("|data: ",data)
        try:
            for key,value in data.items():
                if model_gasto_json[key] and model_gasto_json[key]['type'] == 'int':
                    data[key] = int(data[key])
                    print(f"|key: {key} -> value: {value} | type esperado: {model_gasto_json[key]['type']} |sanitized: {data[key]}")
                elif model_gasto_json[key]  and model_gasto_json[key]['type'] == 'str':
                    data[key] = escape(data[key])
                    print(f"|key: {key} -> value: {value} | type esperado: {model_gasto_json[key]['type']} |sanitized: {data[key]}")
                
                #data[key] = int(data[key]) if list_gasto_form[key][]
            print("|data sanitisado: ",data)
            new_gasto = Gasto(**data)
            db.session.add(new_gasto)
            db.session.commit()

            print("new gasto: ",new_gasto)
            return  jsonify( status = True,msg='Gasto Registrado correctamente')
        except Exception as e:
            print(str(e))
            return  jsonify( status = False,msg='Error al Registrar Gasto.')


        
    

    print("|get registrar gasto ...")
    fecha = datetime.now().date()
    print("|fecha: ",fecha)
    return render_template('pages/gasto/registrar_gasto.html' ,form_gasto = model_gasto_json,list_gasto = list_gasto_form,periodo_id=periodo_id ,fecha=fecha)

@api_bp.route('/gasto/<int:gasto_id>' ,methods=['DELETE'])
def eliminar_gasto(gasto_id=None):
    print("|eliminar gasto: ",gasto_id)
    data = {
            "class":"",
            "msg": f"Error al eliminar Gasto {gasto_id}.",
            "id": gasto_id
        }
    
    try:
        gasto = Gasto.query.filter_by(gasto_id=gasto_id).first()
        print("|gasto obj: ", gasto)

        db.session.delete(gasto)
        db.session.commit()
        print("|Gasto eliminado.")
        data['msg'] =  f"Gasto {gasto_id} eliminado correctamente."
        data['class'] = "bg-success"
    except:
        data['msg'] =  f"Gasto {gasto_id} no encontrado en la DB."
        data['class'] = "bg-danger"

    return Response(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "eliminar_gasto": data,
                
            })
        })

@api_bp.route('/test')
def test():
    return 'test'


""" Api Riego (login_required) """
@api_bp.route('/riegos/registrar', methods=['GET','POST'])
def crear_riego():
    if request.method =='GET':
        print("|Idea: Mostrar RIEGO_FORM.")
        periodo_id = session["periodo_id"]
        fecha = datetime.now().date()
        print("|fecha: ",fecha)
        return render_template('pages/riego/riego_form.html',fecha=fecha,periodo_id=periodo_id) 
    if request.method =='POST':
        print("|Idea: Registrar RIEGO.")
        data = request.get_json()
        print("|Data: ", data)
        new_riego = Riego(**data)
        print("|New riego: ",new_riego)
        db.session.add(new_riego)
        db.session.commit()
        try:
            return jsonify(status=True,title='Exito', msg='Riego registrado exitosamente.')
        except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error al registrar.')
        

@api_bp.route('/riegos', methods=['GET'])
@api_bp.route('/riegos/<int:riego_id>', methods=['GET','DELETE','PUT'])
def riego(riego_id = None):
    print('*'*30 + ' Riegos ' + '*'*30)
    empresa_id = session["empresa_id"]
    periodo_id = session["periodo_id"]
    if request.method == 'GET':
        if not riego_id:
            # Enviar lista de riegos
            riegos = Riego.query.filter_by(periodo_id=periodo_id).all()
            print("|Idea: Mostrar lista riegos.")
            print("|Riegos: ",riegos)
            return render_template('pages/riego/riego.html',riegos=riegos)
         
        

        print("|Idea: Mostrar riego_form con datos.")
        riego = Riego.query.filter_by(riego_id=riego_id).first()
        print(f'|Riego: {riego}')
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Emprsa_id: ',empresa_id)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('pages/riego/riego.html')
    
    if request.method == 'PUT':
         print("|Idea: Mostrar riego_form con datos.")

    if request.method == 'DELETE':
         print("|Idea: Eliminar riego.")
         riego = Riego.query.filter_by(riego_id=riego_id).first()
         print("|Riego a eliminar: ",riego)
         db.session.delete(riego)
         db.session.commit()
         return jsonify(status=True,msg="elimiando")
        

    
@api_bp.route('/riego2', methods=['GET', 'POST'])
def riego2():
    if request.method == 'GET':
        riegos= ['riego 1', 'riego 2']
        # Obtener lista de riego o aplicar filtros según sea necesario
        return jsonify(riegos)
    elif request.method == 'POST':
        # Crear un nuevo producto
        data = request.json
        # Validar y agregar el nuevo producto a la lista
        nuevo_producto = {"id": len(productos) + 1, "nombre": data["nombre"], "precio": data["precio"]}
        productos.append(nuevo_producto)
        return jsonify(nuevo_producto), 201  # 201 Created

@api_bp.route('/riego/<int:riego_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_producto(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404  # 404 Not Found

    if request.method == 'GET':
        # Obtener detalles del producto
        return jsonify(producto)
    elif request.method == 'PUT':
        # Actualizar el producto
        data = request.json
        producto.update({"nombre": data["nombre"], "precio": data["precio"]})
        return jsonify(producto)
    elif request.method == 'DELETE':
        # Eliminar el producto
        productos.remove(producto)
        return jsonify({"mensaje": "Producto eliminado"})
