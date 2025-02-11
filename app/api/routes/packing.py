from flask import Blueprint,jsonify,request,render_template,session
from flask_login import login_required
from ...extensions import model_to_dict2,db,convertir_form_a_dict,establecer_valores_por_defecto_formulario,sanitize_json,establecer_choices_en_form
from ...forms import Packing_form
from ...models import Packing,Empresa,Cosecha
from sqlalchemy import func,text
packing_bp = Blueprint('Packing_bp', __name__)  # Define a Blueprint for person routes

""" Api Packings """
dicc = {
        "entidad": "Packing",
        "api":"packings",
        "url_api":"/api/packings"
        }

@packing_bp.route(f'/{dicc["api"]}/registrar', methods=['GET', 'POST' ])
@login_required
def crear_packing():
    print("-"*20 +f" {request.method} {request.path} START "+ "-"*20)
    form = Packing_form()

    if request.method == 'GET':
        form.periodo_id.default = session['periodo_id']
        form.process()
        cosechas = Cosecha.query.filter_by(packing_id=0,periodo_id=session['periodo_id']).all() #v1.0.9
        
        cosechas = [ item.to_json() for item in cosechas ]
        print(f"Cosechas: {cosechas}")
        print("-"*20 +f" {request.method} {request.path} END "+ "-"*20)
        return render_template("components/packing_form.html",form=form, prev=dicc["url_api"],dicc=dicc,cosechas=cosechas)
    elif request.method == 'POST':
        # Registrar packing
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, form.tablas)
            
            sanitized_json = sanitize_json(new_data)
            print("new_data sanitized: ",new_data)
            new_entidad = Packing(**sanitized_json)
            print("new entidad: ",new_entidad)
            db.session.add(new_entidad)
            db.session.flush()  # Commit the changes to get the new ID
            packing_id = new_entidad.id
            for id in new_data['cosechas']:
                cosecha = Cosecha.query.get(id)
                if cosecha:
                    cosecha.packing_id = packing_id
                    db.session.add(cosecha)
                #buscar cosecha por id y actualizar Cosecha.packing_id = packing_id
            db.session.commit() 
            print("-"*20 +f" {request.method} {request.path} END "+ "-"*20)
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar {dicc["entidad"]}. Error: {str(e)}')


@packing_bp.route(f'/{dicc["api"]}', methods=['GET'])
@packing_bp.route(f'/{dicc["api"]}/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def Packings(id = None):
    form = Packing_form()
    print('*'*30 + f' {dicc["api"]} ' + '*'*30)
    try:
        empresa_id = session["empresa_id"]
        periodo_id = session["periodo_id"]
    except:
        return jsonify(status=False,title='Error', msg=f'Ocurrio un error durante la consulta a la {dicc["url_api"]}.')
    
    if request.method == 'GET':
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Empresa_id: ',empresa_id)
        if not id:
            # Enviar lista de riegos
            entidades = Packing.query.filter_by(periodo_id=periodo_id).all()
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            #print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print("|Idea: Mostrar Packing con datos.")
        entidad = Packing.query.filter_by(id=id).first()
        empresa = Empresa.query.filter_by(empresa_id=empresa_id).first()
        establecer_choices_en_form(form, empresa.parametros)
        print(f'|{dicc["api"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        #print("|empleado detalle: ",empleado.detalle)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/packing_form.html',form=form,entidad=entidad,dicc=dicc,prev=dicc["url_api"])
    
    if request.method == 'PUT':
        try:
            print(f'|Idea: Actualizar {dicc["api"]} con los datos obtenidos mediante PUT.')
            entidad = Packing.query.filter_by(id=id).first()
            data = request.form
            print("|Request form: ", data)
            new_data = convertir_form_a_dict(data, form.tablas)
            sanitized_json = sanitize_json(new_data)
            print("Sobrescribiendo datos...")
            entidad.update_from_dict(sanitized_json)
            print(f'|{dicc["api"]}: {entidad.to_json()}')
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["api"]} actualizado exitosamente.')
        except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al actualizado.')

    if request.method == 'DELETE':
         try:
            print(f'|Idea: Eliminar {dicc["api"]}.')
            entidad = Packing.query.filter_by(id=id).first()
            print(f'|{dicc["api"]} a eliminar: ',entidad)
            db.session.delete(entidad)
            db.session.commit()
            data = {
                "class":"danger",
                "msg": f"Error al eliminar {dicc['api']} {id}.",
                "id": id 
            }
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} : {id} eliminado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al eliminar {dicc["entidad"]} : {id}.')
