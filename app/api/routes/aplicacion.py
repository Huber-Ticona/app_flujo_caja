from flask import Blueprint,jsonify,request,render_template,session
from flask_login import login_required
from ...extensions import model_to_dict2,db,convertir_form_a_dict,establecer_valores_por_defecto_formulario,sanitize_json,cache,establecer_choices_en_form
from ...forms import Aplicacion_form
from ...models import Aplicacion
from sqlalchemy import func,text
from ..tools import get_empresa
aplicacion_bp = Blueprint('aplicacion_bp', __name__)  # Define a Blueprint for person routes

""" Api Aplicacion """
dicc = {
        "entidad": "Aplicacion",
        "api":"Aplicaciones",
        "url_api":"/api/aplicaciones"
        }
@aplicacion_bp.route('/aplicaciones/registrar', methods=['GET', 'POST'])
@login_required
def crear_aplicaciones():
    if request.method == 'GET':
        print("GET, enviando formulario")
        x = get_empresa(1222)
        form = Aplicacion_form()
        form.periodo_id.default = session['periodo_id']
        empresa_parametros = session["empresa_parametros"]
        establecer_choices_en_form(form, empresa_parametros)
        form.process()
        query = text("""
            SELECT l.fecha ,l.lugar, l.nave , d.*
            FROM aplicacion l
            CROSS JOIN JSON_TABLE(l.detalle, '$[*]' COLUMNS (
                insumo VARCHAR(255) PATH '$.insumo'
            )) d
            GROUP BY d.insumo
            """)

        # Ejecución de la consulta y obtención de los resultados
        results = db.session.execute(query).fetchall()
        lista = []
        for i in results:
            lista.append(i[3])
        print(lista)
        dicc["completer"] = {
            "uno_muchos": {
                "detalle": {"insumo": lista,}
            }}
        return render_template("components/base_form.html",form=form,prev=dicc["url_api"],dicc=dicc)
    elif request.method == 'POST':
        # Registrar Trabajador
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Aplicacion_form().tablas)
            print("new_data: ",new_data)
            #print(json.dumps(new_data, indent=2))
            # Llamar a la función para sanitizar el JSON completo
            sanitized_json = sanitize_json(new_data)
            # Imprimir el JSON sanitizado
            #print(json.dumps(sanitized_json, indent=2))
            new_aplicacion = Aplicacion(**sanitized_json)
            print("new aplicacion: ",new_aplicacion)
            db.session.add(new_aplicacion)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg='Aplicacion registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar Aplicacaion. Error: {str(e)}')

@aplicacion_bp.route('/aplicaciones', methods=['GET'])
@aplicacion_bp.route('/aplicaciones/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def aplicaciones(id = None):
    dicc = {
        "entidad" : "Aplicacion",
        "api":"Aplicaciones",
        "url_api":"/api/aplicaciones"
        }
    form = Aplicacion_form()

    print('*'*30 + f' API: {dicc["entidad"]} ' + '*'*30)
    try:
            empresa_id = session["empresa_id"]
            periodo_id = session["periodo_id"]
    except:
        return jsonify(status=False,title='Error', msg=f'Ocurrio un error durante la consulta a la {dicc["url_api"]}.')
    
    if request.method == 'GET':
        
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Empresa_id: ',empresa_id)
        if not id:
            # Enviar lista
            entidades = Aplicacion.query.filter_by(periodo_id=periodo_id).all()
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            print(f'|Nro de {dicc["api"]}: ',len(entidades))
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print(f"|Idea: Mostrar {dicc['entidad']} con datos.")
        entidad = Aplicacion.query.filter_by(id=id).first()
        print(f'|{dicc["entidad"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc,prev=dicc["url_api"])
    
    if request.method == 'PUT':
         print(f'|Idea: Actualizar {dicc["entidad"]} : {id}. con los datos obtenidos mediante PUT.')
         try:
            entidad = Aplicacion.query.filter_by(id=id).first()
            data = request.form
            print("|Request form: ", data)
            new_data = convertir_form_a_dict(data, form.tablas)
            #print(json.dumps(new_data, indent=2))
            # Llamar a la función para sanitizar el JSON completo
            sanitized_json = sanitize_json(new_data)
            # Imprimir el JSON sanitizado
            #print(json.dumps(sanitized_json, indent=2))
            print("Sobrescribiendo datos...")
            entidad.update_from_dict(sanitized_json)
            print(f'|{dicc["entidad"]}: {entidad.to_json()}')
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al actualizar {dicc["entidad"]} : {id}.')

    if request.method == 'DELETE':
         print(f'|Idea: Eliminar {dicc["entidad"]} : {id}.')
         try:
            entidad = Aplicacion.query.filter_by(id=id).first()
            print(f'|{dicc["entidad"]} a eliminar: ',entidad)
            db.session.delete(entidad)
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} : {id} eliminado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al eliminar {dicc["entidad"]} : {id}.')