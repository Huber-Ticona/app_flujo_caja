from flask import Blueprint,render_template,request,redirect,url_for,jsonify,session,Response,abort,flash
from flask_login import login_required
from .forms import Crear_Gasto_Form,Empleado_form,Aplicacion_form,Riego_form,Gasto_Form
from .models import Gasto,Riego,Empleado,Aplicacion
from .extensions import get_fields_and_types,model_to_dict2,db,convertir_form_a_dict,establecer_valores_por_defecto_formulario
from html import escape
from datetime import datetime
import json

api_bp = Blueprint('api_bp' , __name__,template_folder='templates',static_folder='static')

""" @api_bp.route('/gasto/<int:periodo_id>')
@login_required
def obtener_gasto(periodo_id=None):

    return  render_template('pages/gasto/gasto.html',periodo_id=periodo_id)

@api_bp.route('/gasto/<int:periodo_id>/lista')
@login_required
def lista_gasto(periodo_id=None):
    gastos = Gasto.query.filter_by(periodo_id=periodo_id).all()
    
    print(f"|{'-'*10} Lista de gastos | periodo: {periodo_id} {'-'*10}| ")
    print(f"|Gastos: {gastos}")
    print(f"|{'-'*10} END {'-'*10}|")
    return  render_template('pages/gasto/lista_gasto.html',gastos=gastos)

@api_bp.route('/gasto/<int:periodo_id>/registrar' , methods=['GET', 'POST'])
@login_required
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
@login_required
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

    return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})

@api_bp.route('/test')
def test():
    return 'test' """

""" Api Gasto  """
@api_bp.route('/gastos/registrar', methods=['GET','POST'])
@login_required
def crear_gasto():
    if request.method =='GET':
        periodo_id = session["periodo_id"]
        fecha = datetime.now().date()
        print("|fecha: ",fecha)
        form = Riego_form()
        fecha = datetime.now()
        form.fecha.default = fecha
        form.periodo_id.default = periodo_id
        form.process()
        return render_template("components/base_form.html",form=form)
    if request.method =='POST':
        # Registrar Riego
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Riego_form().tablas)
            print("new_data: ",new_data)
            new_aplicacion = Riego(**new_data)
            print("new aplicacion: ",new_aplicacion)
            db.session.add(new_aplicacion)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg='Riego registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar Riego. Error: {str(e)}')
       
        

@api_bp.route('/gastos', methods=['GET'])
@api_bp.route('/gastos/<int:riego_id>', methods=['GET','DELETE','PUT'])
@login_required
def gastos(riego_id = None):
    print('*'*30 + ' Riegos ' + '*'*30)
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
        riego = Riego.query.filter_by(riego_id=riego_id).first()
        print(f'|Riego: {riego}')
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('pages/riego/riego_form.html',riego=riego,periodo_id=periodo_id)
    
    if request.method == 'PUT':
         print("|Idea: Actualizar riego con los datos obtenidos mediante PUT.")
         riego = Riego.query.filter_by(riego_id=riego_id).first()
         print(f'|Riego: {riego}')
         data = request.get_json()
         print("|Data: ", data)
         riego.update_from_dict(data)
         db.session.commit()
         try:
            return jsonify(status=True,title='Exito', msg='Riego actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error al actualizado.')

    if request.method == 'DELETE':
         print("|Idea: Eliminar riego.")
         riego = Riego.query.filter_by(riego_id=riego_id).first()
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
        return render_template("components/base_form.html",form=form)
    if request.method =='POST':
        # Registrar Riego
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Riego_form().tablas)
            print("new_data: ",new_data)
            new_aplicacion = Riego(**new_data)
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
    print('*'*30 + ' Riegos ' + '*'*30)
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
        riego = Riego.query.filter_by(riego_id=riego_id).first()
        print(f'|Riego: {riego}')
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('pages/riego/riego_form.html',riego=riego,periodo_id=periodo_id)
    
    if request.method == 'PUT':
         print("|Idea: Actualizar riego con los datos obtenidos mediante PUT.")
         riego = Riego.query.filter_by(riego_id=riego_id).first()
         print(f'|Riego: {riego}')
         data = request.get_json()
         print("|Data: ", data)
         riego.update_from_dict(data)
         db.session.commit()
         try:
            return jsonify(status=True,title='Exito', msg='Riego actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error al actualizado.')

    if request.method == 'DELETE':
         print("|Idea: Eliminar riego.")
         riego = Riego.query.filter_by(riego_id=riego_id).first()
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
        return render_template("components/base_form.html",form=form)
    elif request.method == 'POST':
        # Registrar Trabajador
        try:
            data = request.form
            print("form data: ",data)
            detalle = json.loads(request.form.get('detalle'))
            empresa_id = request.form.get('empresa_id')
            aux_empresa_id = session['empresa_id']
            print(f"Empresa_id: {empresa_id} | session empresa_id: {aux_empresa_id}")
            print(f"detalle: {detalle} | type: {type(detalle)}")
            new_empleado = Empleado(detalle = detalle, empresa_id=empresa_id)
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
    print('*'*30 + ' Trabajadores ' + '*'*30)
    
    if request.method == 'GET':
        try:
            empresa_id = session["empresa_id"]
            periodo_id = session["periodo_id"]
        except:
            return jsonify(status=False,title='Error', msg='Ocurrio un error durante la consulta a la /api/trabajadores.')
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Emprsa_id: ',empresa_id)
        if not empleado_id:
            # Enviar lista de riegos
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
        for item in form:
            print(f"|ID: {item.id} |name: {item.name}")
        print("|empleado detalle: ",empleado.detalle)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=empleado)
    
    if request.method == 'PUT':
         print("|Idea: Actualizar empleado con los datos obtenidos mediante PUT.")
         empleado = Empleado.query.filter_by(id=empleado_id).first()
         data = request.form
         print("|Request form: ", data)
         new_data = convertir_form_a_dict(data, Empleado_form().tablas)
         print("Sobrescribiendo datos...")
         empleado.update_from_dict(new_data)
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
    if request.method == 'GET':
        print("GET, enviando formulario")
        form = Aplicacion_form()
        fecha = datetime.now()
        form.fecha.default = fecha
        form.periodo_id.default = session['periodo_id']
        form.process()
        return render_template("components/base_form.html",form=form)
    elif request.method == 'POST':
        # Registrar Trabajador
        try:
            data = request.form
            print("form data: ",data)
            new_data = convertir_form_a_dict(data, Aplicacion_form().tablas)
            print("new_data: ",new_data)
            new_aplicacion = Aplicacion(**new_data)
            print("new aplicacion: ",new_aplicacion)
            db.session.add(new_aplicacion)
            db.session.commit() 
            return jsonify(status=True,title='Exito', msg='Aplicacaion registrado exitosamente.')
        except Exception as e:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al registrar Aplicacaion. Error: {str(e)}')

@api_bp.route('/aplicaciones', methods=['GET'])
@api_bp.route('/aplicaciones/<int:id>', methods=['GET','DELETE','PUT'])
@login_required
def aplicaciones(id = None):
    dicc = {
        "api":"Aplicaciones",
        "url_api":"/api/aplicaciones"
        }
    form = Aplicacion_form()

    print('*'*30 + f' {dicc["api"]} ' + '*'*30)
    try:
            empresa_id = session["empresa_id"]
            periodo_id = session["periodo_id"]
    except:
        return jsonify(status=False,title='Error', msg='Ocurrio un error durante la consulta a la /api/aplicaciones.')
    
    if request.method == 'GET':
        
        print('|(session) Periodo_id: ',periodo_id)
        print('|(session) Emprsa_id: ',empresa_id)
        if not id:
            # Enviar lista de riegos
            entidades = Aplicacion.query.filter_by(periodo_id=periodo_id).all()
            entidades = [ item.to_json() for item in entidades ]
            print(f'|Idea: Mostrar lista {dicc["api"]}.')
            print(f'|{dicc["api"]}: ',entidades)
            return render_template('components/base_list.html',entidades=entidades,dicc=dicc,form=form)
    
        print("|Idea: Mostrar aplicaciones con datos.")
        entidad = Aplicacion.query.filter_by(id=id).first()
        print(f'|{dicc["api"]}: {entidad}')

        establecer_valores_por_defecto_formulario(form,entidad)
        print("Form: ",form)
        for item in form:
            print(f"|ID: {item.id} |name: {item.name}")
        #print("|empleado detalle: ",empleado.detalle)
        # Obtener lista de riego o aplicar filtros según sea necesario
        return render_template('components/base_form.html',form=form,entidad=entidad)
    
    if request.method == 'PUT':
         print(f'|Idea: Actualizar {dicc["api"]} con los datos obtenidos mediante PUT.')
         entidad = Aplicacion.query.filter_by(id=id).first()
         data = request.form
         print("|Request form: ", data)
         new_data = convertir_form_a_dict(data, form.tablas)
         print("Sobrescribiendo datos...")
         entidad.update_from_dict(new_data)
         print(f'|{dicc["api"]}: {entidad.to_json()}')
         db.session.commit()
         try:
            return jsonify(status=True,title='Exito', msg=f'{dicc["api"]} actualizado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al actualizado.')

    if request.method == 'DELETE':
         print(f'|Idea: Eliminar {dicc["api"]}.')
         entidad = Aplicacion.query.filter_by(id=id).first()
         print(f'|{dicc["api"]} a eliminar: ',entidad)
         db.session.delete(entidad)
         db.session.commit()
         data = {
            "class":"danger",
            "msg": f"Error al eliminar {dicc['api']} {id}.",
            "id": id
         }
         try:
            return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})
         except:
            return Response(status=204,headers={'HX-Trigger': json.dumps({"eliminar_registro": data,})})
