from flask import Blueprint,render_template,request,redirect,url_for,jsonify,session,Response,abort,flash
from flask_login import login_required
from .forms import Empleado_form,Aplicacion_form,Riego_form,Gasto_Form,PagoPersonal_form,RegistroLaboral_form,Embarque_form
from .models import Gasto,Riego,Empleado,Aplicacion,PagoPersonal,RegistroLaboral,Embarque
from .extensions import model_to_dict2,db,convertir_form_a_dict,establecer_valores_por_defecto_formulario,sanitize_json
from datetime import datetime
import json
import requests
from sqlalchemy import func,text, column,select, literal_column,JSON,cast,String,Integer
from sqlalchemy.orm import aliased

api_bp = Blueprint('api_bp' , __name__,template_folder='templates',static_folder='static')

""" Api gastos """
@api_bp.route('/gastos/registrar', methods=['GET', 'POST'])
@login_required
def crear_gasto():
    dicc = { "api":"Gastos" ,"entidad":"Gasto" }
    if request.method == 'GET':
        print("GET, enviando formulario")
        form = Gasto_Form()
        form.periodo_id.default = session['periodo_id']
        form.process()
        query = text("""
            SELECT g.fecha,g.prov_empresa, d.* 
            FROM gasto g 
            CROSS JOIN JSON_TABLE(g.detalle, '$[*]' COLUMNS(
                unidad varchar(255) path '$.unidad',
                cantidad int path '$.cantidad',
                descripcion VARCHAR(255) PATH '$.descripcion',
                precio_unitario int path '$.precio_unitario',
                precio_total int path '$.precio_total'
            )) d
            group by d.descripcion
            order by g.fecha desc
            """)

        # Ejecución de la consulta y obtención de los resultados
        results = db.session.execute(query).fetchall()
        lista = []
        for i in results:
            lista.append(i[4])
        print(lista)

        # Consulta para obtener descripciones únicas
        descripciones_unicas = Gasto.query \
            .filter_by(periodo_id=session["periodo_id"]) \
            .group_by(Gasto.prov_empresa) \
            .all()
        lista_empresa = []
        for i in descripciones_unicas:
            lista_empresa.append(i.prov_empresa)
            print("empresa: ",i.prov_empresa)

        dicc["extras"] = {
            "uno_uno": {"prov_empresa": lista_empresa,
                        "prov_folio": [500, 2000, 7500]
                        },
            "uno_muchos": {
                "detalle": {"descripcion": lista,
                            "cantidad": [9, 99, 999]}
            }}
        return render_template("components/base_form.html",form=form, prev="/api/gastos",dicc=dicc)
    elif request.method == 'POST':
        # Registrar
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Gasto_Form().tablas)
            print("new_data: ",new_data)
            sanitized_json = sanitize_json(new_data)
            new_entidad = Gasto(**sanitized_json)
            print("new entidad: ",new_entidad)
            db.session.add(new_entidad)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar {dicc["entidad"]}. Error: {str(e)}')

@api_bp.route('/gastos', methods=['GET'])
@api_bp.route('/gastos/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def gastos(id = None):
    dicc = {
        "entidad": "Gasto",
        "api":"Gastos",
        "url_api":"/api/gastos"
        }
    form = Gasto_Form()
    print('*'*30 + f' {dicc["api"]} ' + '*'*30)

    try:
        empresa_id = session["empresa_id"]
        periodo_id = session["periodo_id"]
    except:
        return jsonify(status=False,title='Error', msg=f'Ocurrio un error durante la consulta a la {dicc["url_api"]}.')
    
    if request.method == 'GET':
        
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Emprsa_id: ',empresa_id)
        if not id:
            # Enviar lista de riegos
            entidades = Gasto.query.filter_by(periodo_id=periodo_id).all()
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            #print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print("|Idea: Mostrar Gastos con datos.")
        entidad = Gasto.query.filter_by(id=id).first()
        print(f'|{dicc["api"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        #print("|empleado detalle: ",empleado.detalle)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc)
    
    if request.method == 'PUT':
        try:
            print(f'|Idea: Actualizar {dicc["api"]} con los datos obtenidos mediante PUT.')
            entidad = Gasto.query.filter_by(id=id).first()
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
            entidad = Gasto.query.filter_by(id=id).first()
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


""" Api Riego (login_required) """
@api_bp.route('/riegos/registrar', methods=['GET','POST'])
@login_required
def crear_riego():
    if request.method =='GET':
        print("|Idea: Mostrar RIEGO_FORM.")
        periodo_id = session["periodo_id"]
        fecha = datetime.now().date()
        print("|fecha: ",fecha)
        form = Riego_form()
        fecha = datetime.now()
        form.fecha.default = fecha
        form.periodo_id.default = periodo_id
        form.process()
        return render_template("components/base_form.html",form=form,prev="/api/riegos")
    if request.method =='POST':
        # Registrar Riego
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Riego_form().tablas)
            sanitized_json = sanitize_json(new_data)
            print("new_data: ",new_data)
            new_aplicacion = Riego(**sanitized_json)
            print("new aplicacion: ",new_aplicacion)
            db.session.add(new_aplicacion)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg='Riego registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar Riego. Error: {str(e)}')
       
        

@api_bp.route('/riegos', methods=['GET'])
@api_bp.route('/riegos/<int:riego_id>', methods=['GET','DELETE','PUT'])
@login_required
def riego(riego_id = None):
    dicc = {
        "entidad" : "Riego",
        "api":"Riegos",
        "url_api":"/api/riegos"
        }
    form = Riego_form()
    print('*'*30 + f' {dicc["entidad"]} ' + '*'*30)
    try:
        empresa_id = session["empresa_id"]
        periodo_id = session["periodo_id"]
    except:
        return jsonify(status=False,title='Error', msg='Ocurrio un error durante la consulta a la /api/riegos.')
    
    print('|(session) Periodo_id: ',periodo_id)
    print('|(session) Emprsa_id: ',empresa_id)
    if request.method == 'GET':
        if not riego_id:
            # Enviar lista de riegos
            riegos = Riego.query.filter_by(periodo_id=periodo_id).all()
            print("|Idea: Mostrar lista riegos.")
            print("|Riegos: ",riegos)
            return render_template('pages/riego/riego.html',riegos=riegos)
    
        print("|Idea: Mostrar riego_form con datos.")
        entidad = Riego.query.filter_by(id=riego_id).first()
        print(f'|{dicc["entidad"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc)
    
    if request.method == 'PUT':
         print("|Idea: Actualizar riego con los datos obtenidos mediante PUT.")
         riego = Riego.query.filter_by(id=riego_id).first()
         print(f'|Riego: {riego}')
         data = request.form
         print("|Request form: ", data)
         
         sanitized_json = sanitize_json(data)
         riego.update_from_dict(sanitized_json)
         db.session.commit()
         try:
            return jsonify(status=True,title='Exito', msg='Riego actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error al actualizado.')

    if request.method == 'DELETE':
         print("|Idea: Eliminar riego.")
         riego = Riego.query.filter_by(id=riego_id).first()
         print("|Riego a eliminar: ",riego)
         db.session.delete(riego)
         db.session.commit()
         data = {
            "class":"success",
            "msg": f"Exito al eliminar Riego {riego_id}.",
            "id": riego_id
         }
         try:
            return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})
         except:
            return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})

""" API Trabajadores """
@api_bp.route('/trabajadores/registrar', methods=['GET', 'POST'])
@login_required
def crear_trabajadores():
    if request.method == 'GET':
        print("GET, enviando formulario")
        model_form = model_to_dict2(Empleado)
        print(model_form)
        empresa_id = session['empresa_id']
        form = Empleado_form()
        form.empresa_id.default = empresa_id
        form.process()
        return render_template("components/base_form.html",form=form,prev="/api/trabajadores")
    elif request.method == 'POST':
        # Registrar Trabajador
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Empleado_form().tablas)
            print("new_data: ",new_data)
            sanitized_json = sanitize_json(new_data)
            empresa_id = request.form.get('empresa_id')
            aux_empresa_id = session['empresa_id']
            print(f"Empresa_id: {empresa_id} | session empresa_id: {aux_empresa_id}")
            print(f"detalle: {sanitized_json} | type: {type(sanitized_json)}")
            new_empleado = Empleado(**sanitized_json)
            print("new empleado: ",new_empleado)
            db.session.add(new_empleado)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg='Trabajador registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar Trabajador. Error: {str(e)}')

@api_bp.route('/trabajadores', methods=['GET'])
@api_bp.route('/trabajadores/<int:empleado_id>', methods=['GET','DELETE','PUT'])
@login_required
def trabajadores(empleado_id = None):
    dicc = {
        "entidad" : "Trabajador",
        "api":"Trabajadores",
        "url_api":"/api/trabajadores"
        }
    print('*'*30 + f' {dicc["entidad"]} ' + '*'*30)
    
    if request.method == 'GET':
        try:
            empresa_id = session["empresa_id"]
            periodo_id = session["periodo_id"]
        except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error durante la consulta a la /api/trabajadores.')
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Emprsa_id: ',empresa_id)
        if not empleado_id:
            # Enviar lista
            empleados = Empleado.query.filter_by(empresa_id=empresa_id).all()
            print("|Idea: Mostrar lista Trabajadores.")
            print("|Trabajadores: ",empleados)
            return render_template('pages/empleado/empleado.html',empleados=empleados)
    
        print("|Idea: Mostrar empleado con datos.")
        empleado = Empleado.query.filter_by(id=empleado_id).first()
        print(f'|empleado: {empleado}')
        form = Empleado_form()
        form.empresa_id.default = empresa_id
        
        form.process()
        print("Form: ",form)
        print("|empleado detalle: ",empleado.detalle)
        establecer_valores_por_defecto_formulario(form,empleado)
        # Obtener lista  o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=empleado,dicc=dicc)
    
    if request.method == 'PUT':
         print("|Idea: Actualizar empleado con los datos obtenidos mediante PUT.")
         empleado = Empleado.query.filter_by(id=empleado_id).first()
         data = request.form
         print("|Request form: ", data)
         new_data = convertir_form_a_dict(data, Empleado_form().tablas)
         #print(json.dumps(new_data, indent=2))
         # Llamar a la función para sanitizar el JSON completo
         sanitized_json = sanitize_json(new_data)
         # Imprimir el JSON sanitizado
         #print(json.dumps(sanitized_json, indent=2))
         print("Sobrescribiendo datos...")
         empleado.update_from_dict(sanitized_json)
         print(f'|Empleado: {empleado.to_json()}')
         db.session.commit()
         try:
            return jsonify(status=True,title='Exito', msg='Riego actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error al actualizado.')

    if request.method == 'DELETE':
         print("|Idea: Eliminar empleado.")
         empleado = Empleado.query.filter_by(id=empleado_id).first()
         print("|empleado a eliminar: ",empleado)
         db.session.delete(empleado)
         db.session.commit()
         data = {
            "class":"danger",
            "msg": f"Error al eliminar Empleado {empleado_id}.",
            "id": empleado_id
         }
         try:
            return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})
         except:
            return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})

""" Api APLICACIONES """
@api_bp.route('/aplicaciones/registrar', methods=['GET', 'POST'])
@login_required
def crear_aplicaciones():
    dicc = { "api":"Aplicaciones" ,"entidad":"Aplicacion" }
    if request.method == 'GET':
        print("GET, enviando formulario")
        form = Aplicacion_form()
        fecha = datetime.now()
        form.fecha.default = fecha
        form.periodo_id.default = session['periodo_id']
        form.process()
        query = text("""
        SELECT l.id,l.fecha ,l.lugar, l.nave ,l.comentario, d.*,
            CASE
            WHEN d.unidad_de_total IN ('kilogramo (KG)', 'Litro (LTS)') THEN d.total_aplicado
            WHEN d.unidad_de_total = 'Mili-litro (ML)' THEN d.total_aplicado / 1000
            WHEN d.unidad_de_total = 'Mili-gramo (MG)' THEN d.total_aplicado / 1000
            ELSE NULL
            END AS total_kg_lt
        FROM aplicacion l
        CROSS JOIN JSON_TABLE(l.detalle, '$[*]' COLUMNS (
            insumo VARCHAR(255) PATH '$.insumo',
            total_aplicado float PATH '$.total_aplicado',
            unidad_de_total varchar(255) PATH '$.unidad_de_total'
)) d
                     GROUP BY d.insumo
        """)

        # Ejecución de la consulta y obtención de los resultados
        results = db.session.execute(query).fetchall()
        lista = []
        for i in results:
            lista.append(i[5])
        print(lista)
        return render_template("components/base_form.html",form=form,prev="/api/aplicaciones",dicc=dicc)
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

@api_bp.route('/aplicaciones', methods=['GET'])
@api_bp.route('/aplicaciones/<int:id>', methods=['GET','DELETE','PUT'])
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
            print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print(f"|Idea: Mostrar {dicc['entidad']} con datos.")
        entidad = Aplicacion.query.filter_by(id=id).first()
        print(f'|{dicc["entidad"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc)
    
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

""" Api pago personal """
@api_bp.route('/pagos_personal/registrar', methods=['GET', 'POST'])
@login_required
def crear_pago_personal():
    dicc = { "api":"Pagos_personal" ,"entidad":"Pago_personal" }
    form = PagoPersonal_form()
    if request.method == 'GET':
        print("GET, enviando formulario")
        form.personal.choices = [(f"{empleado.detalle['nombre']} {empleado.detalle['apellido']}",
                                f"{empleado.detalle['nombre']} {empleado.detalle['apellido']}") for empleado in Empleado.query.all()]
        form.periodo_id.default = session['periodo_id']
        form.process()
        return render_template("components/base_form.html",form=form,prev="/api/pagos_personal",dicc=dicc)
    elif request.method == 'POST':
        # Registrar Trabajador
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, form.tablas)
            print("new_data: ",new_data)
            new_aplicacion = PagoPersonal(**new_data)
            print("new aplicacion: ",new_aplicacion)
            db.session.add(new_aplicacion)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar {dicc["entidad"]}. Error: {str(e)}')

@api_bp.route('/pagos_personal', methods=['GET'])
@api_bp.route('/pagos_personal/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def pagos_personal(id = None):
    dicc = {
        "entidad" : "Pago_personal",
        "api":"Pagos_personal",
        "url_api":"/api/pagos_personal"
        }
    form = PagoPersonal_form()

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
            entidades = PagoPersonal.query.filter_by(periodo_id=periodo_id).all()
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print(f"|Idea: Mostrar {dicc['entidad']} con datos.")
        entidad = PagoPersonal.query.filter_by(id=id).first()
        print(f'|{dicc["entidad"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc)
    
    if request.method == 'PUT':
         print(f'|Idea: Actualizar {dicc["entidad"]} : {id}. con los datos obtenidos mediante PUT.')
         try:
            entidad = PagoPersonal.query.filter_by(id=id).first()
            data = request.form
            print("|Request form: ", data)
            new_data = convertir_form_a_dict(data, form.tablas)
            print("Sobrescribiendo datos...")
            entidad.update_from_dict(new_data)
            print(f'|{dicc["entidad"]}: {entidad.to_json()}')
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al actualizar {dicc["entidad"]} : {id}.')

    if request.method == 'DELETE':
         print(f'|Idea: Eliminar {dicc["entidad"]} : {id}.')
         try:
            entidad = PagoPersonal.query.filter_by(id=id).first()
            print(f'|{dicc["entidad"]} a eliminar: ',entidad)
            db.session.delete(entidad)
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} : {id} eliminado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al eliminar {dicc["entidad"]} : {id}.')

""" Api registro laboral """
@api_bp.route('/registros_laborales/registrar', methods=['GET', 'POST'])
@login_required
def crear_registro_laboral():
    dicc = { "api":"Registros_laborales" ,"entidad":"Registro_laboral" }
    print(datetime.now())
    form = RegistroLaboral_form()
    if request.method == 'GET':
        print("GET, enviando formulario")
        form.periodo_id.default = session['periodo_id']
        form.process()
        return render_template("components/base_form.html",form=form,prev="/api/registros_laborales",dicc=dicc)
    elif request.method == 'POST':
        # Registrar 
        try:
            data = request.form
            print("|form data: ",data)
            new_data = convertir_form_a_dict(data, form.tablas)
            print("|new_data: ",new_data)
            #print(json.dumps(new_data, indent=2))
            # Llamar a la función para sanitizar el JSON completo
            sanitized_json = sanitize_json(new_data)
            # Imprimir el JSON sanitizado
            #print(json.dumps(sanitized_json, indent=2))
            new_aplicacion = RegistroLaboral(**sanitized_json)
            print(f"|new {dicc['entidad']}: ",new_aplicacion)
            db.session.add(new_aplicacion)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar {dicc["entidad"]}. Error: {str(e)}')

@api_bp.route('/registros_laborales', methods=['GET'])
@api_bp.route('/registros_laborales/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def registro_laboral(id = None):
    dicc = {
        "entidad" : "Registro_laboral",
        "api":"Registros_laborales",
        "url_api":"/api/registros_laborales"
        }
    form = RegistroLaboral_form()

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
            entidades = RegistroLaboral.query.filter_by(periodo_id=periodo_id).all()
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print(f"|Idea: Mostrar {dicc['entidad']} con datos.")
        entidad = RegistroLaboral.query.filter_by(id=id).first()
        print(f'|{dicc["entidad"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc)
    
    if request.method == 'PUT':
         print(f'|Idea: Actualizar {dicc["entidad"]} : {id}. con los datos obtenidos mediante PUT.')
         try:
            entidad = RegistroLaboral.query.filter_by(id=id).first()
            data = request.form
            print("|Request form: ", data)
            new_data = convertir_form_a_dict(data, form.tablas)
            print("Sobrescribiendo datos...")
            #print(json.dumps(new_data, indent=2))
            # Llamar a la función para sanitizar el JSON completo
            sanitized_json = sanitize_json(new_data)
            # Imprimir el JSON sanitizado
            #print(json.dumps(sanitized_json, indent=2))
            entidad.update_from_dict(sanitized_json)
            print(f'|{dicc["entidad"]}: {entidad.to_json()}')
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al actualizar {dicc["entidad"]} : {id}.')

    if request.method == 'DELETE':
         print(f'|Idea: Eliminar {dicc["entidad"]} : {id}.')
         try:
            entidad = RegistroLaboral.query.filter_by(id=id).first()
            print(f'|{dicc["entidad"]} a eliminar: ',entidad)
            db.session.delete(entidad)
            db.session.commit()
            return jsonify(status=True,title='Exito', msg=f'{dicc["entidad"]} : {id} eliminado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al eliminar {dicc["entidad"]} : {id}.')

""" Api EMBARQUE """
@api_bp.route('/embarques/registrar', methods=['GET', 'POST'])
@login_required
def crear_embarque():
    if request.method == 'GET':
        print("GET, enviando formulario")
        form = Embarque_form()
        form.periodo_id.default = session['periodo_id']
        form.process()
        return render_template("components/base_form.html",form=form, prev="/api/embarques")
    elif request.method == 'POST':
        # Registrar
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Embarque_form().tablas)
            print("new_data: ",new_data)
            sanitized_json = sanitize_json(new_data)
            new_entidad = Embarque(**sanitized_json)
            print("new entidad: ",new_entidad)
            #db.session.add(new_entidad)
            #db.session.commit() 
            return jsonify(status=True,title='Exito', msg='Embarque registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar Embarque. Error: {str(e)}')

@api_bp.route('/embarques', methods=['GET'])
@api_bp.route('/embarques/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def embarques(id = None):
    dicc = {
        "entidad": "Embarque",
        "api":"Embarques",
        "url_api":"/api/embarques"
        }
    form = Embarque_form()
    print('*'*30 + f' {dicc["api"]} ' + '*'*30)

    try:
        empresa_id = session["empresa_id"]
        periodo_id = session["periodo_id"]
    except:
        return jsonify(status=False,title='Error', msg=f'Ocurrio un error durante la consulta a la {dicc["url_api"]}.')
    
    if request.method == 'GET':
        
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Emprsa_id: ',empresa_id)
        if not id:
            # Enviar lista de riegos
            entidades = Embarque.query.filter_by(periodo_id=periodo_id).all()
           
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print("|Idea: Mostrar aplicaciones con datos.")
        entidad = Embarque.query.filter_by(embarque_id=id).first()
        print(f'|{dicc["api"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        #print("|empleado detalle: ",empleado.detalle)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad,dicc=dicc)
    
    if request.method == 'PUT':
        try:
            print(f'|Idea: Actualizar {dicc["api"]} con los datos obtenidos mediante PUT.')
            entidad = Embarque.query.filter_by(embarque_id=id).first()
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
            entidad = Embarque.query.filter_by(embarque_id=id).first()
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

@api_bp.route('/odepa')
@login_required
def odepa():
    
    fecha_search = datetime.now().date() 
    try:
        print("arg: ",request.args)
        print("arg fecha: ",request.args['fechaInput'])

        if request.args['fechaInput']:
            fecha_search =  datetime.strptime(request.args['fechaInput'], "%Y-%m-%d").date()
    except:
        print('|--> Error en la fecha. Defecto fecha actual.')
        return render_template("components/odepa.html",fecha=fecha_search)
    
    print("|Fecha busqueda: ",fecha_search)
    url_token = 'https://api-token.odepa.gob.cl/oauth/token'
    headers_token = {
        'Authorization': 'Basic b2F1dGgyLXJlcG9ydGVzOjEyMzQ1Njc4OTA=',
        'Content-Type': 'application/x-www-form-urlencoded '
    }
    data_token = {
        'grant_type': 'password',
        'username': 'dev-user-r',
        'password': '12345678'
    }
    print('*'*15 + f' Obteniendo datos api TOKEN '+ '*'*15 )
    response = requests.post(url_token,headers=headers_token,data=data_token)
    if response.status_code == 200:
        print("|- Mostrando datos token ...")
        # La solicitud fue exitosa, puedes procesar los datos de la respuesta
        data = response.json()
        print(f"|Exito - Token valido hasta: {data['expires_in']} segundos.")
        print('*'*15 + f' Obteniendo datos api REPORTES '+ '*'*15 )
        # URL de la API
        url = f"https://api-reportes.odepa.gob.cl/apps-odepa/v1/noticias-mercado/precio-volumen-diario-fruta-hortaliza?fechaInicio={fecha_search}&fechaTermino={fecha_search}&mercados=3002,3001,3011,3004,3022,3023,3021,3009,3013,3020,3024,3025&subSector=4&productos=2,3,10,9,11,12,29,35,51,55,262,59,942,68,79,501,946,91,81,93,102,947,132,131,950,150,160,166,944,192,214,220,229,230,233,239,246,247,251,255,948,263,201,271,287,311,312,314&mostrarMercado=true&mostrarVariedad=true&mostrarCalidad=true&mostrarOrigen=true&mostrarPrecioIva=true"

    
        # Encabezados de la solicitud, incluyendo el token de autorización
        token = data["access_token"]
        refresh_token = data["refresh_token"]
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json, text/plain, */*'
        }

        # Realizar la solicitud GET
        response = requests.get(url,headers=headers)
        print("|- Enviando request...")
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            print("|- Obteniendo datos...")
            # La solicitud fue exitosa, puedes procesar los datos de la respuesta
            data = response.json()
            print("|Exito: ",data['success'])
            return render_template("components/odepa.html",fecha=fecha_search,data = data['objParams'])
        else:
            # La solicitud falló, imprime el código de estado y el mensaje de error
            print(f"Error {response.status_code}: {response.text}")
            return 'error'
    else:
        # La solicitud falló, imprime el código de estado y el mensaje de error
        print(f"Error {response.status_code}: {response.text}")
        return 'error'
    