from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, json,send_file,current_app
from flask_login import login_required, current_user
from .extensions import convertir_fecha, db ,cache
from flask_minify import decorators as minify_decorators
from html import escape
from .forms import Crear_Empresa_Form, Crear_Periodo_Form
from .models import Empresa, Periodo, Embarque, Liquidacion
import subprocess
from datetime import datetime

main_bp = Blueprint('main_bp', __name__,
                    static_folder='static', template_folder='templates')


@main_bp.route('/')
@main_bp.route('/empresa')
@login_required
def home():
    empresas = Empresa.query.filter_by(usuario_id=current_user.get_id()).all()
    print(f"******** USUARIO: {current_user.usuario} *********")
    print('empresas: ', empresas)
    print(f"*****************")
    return render_template('inicio.html', empresas=empresas)


@main_bp.route('/empresa/<int:id>')
@login_required
def empresa(id=None):
    session['empresa_id'] = id
    empresa = Empresa.query.filter_by(empresa_id=id).first()
    periodos = Periodo.query.filter_by(empresa_id=id).all()
    
    session["empresa_parametros"] = empresa.parametros
    print(f"******** EMPRESA: {id} *********")
    print(f'Empresa: {empresa} | nombre: {empresa.nombre_empresa} | rubro: {empresa.rubro_empresa}')
    print('Periodos: ', periodos)
    print(f"*****************")
    return render_template('empresa.html', periodos=periodos, id=id,empresa=empresa)


@main_bp.route('/empresa/<int:id>/<int:periodo_id>', methods=['GET'])
@minify_decorators.minify(html=True, js=True, cssless=True)
@cache.cached(timeout=10)
@login_required
def empresa_dashboard(id=None, periodo_id=None):
    session['periodo_id'] = periodo_id
    parametros = session["empresa_parametros"]
    empresa = Empresa.query.filter_by(empresa_id=id).first()
    periodo = Periodo.query.filter_by(periodo_id=periodo_id).first()
    print(f"******** EMPRESA: {id} | Periodo: {str(periodo)} *********")
    print(" parametros type: ", type(parametros))
    #print("cache empresa: ", empresa)
    print(" parametros: ", parametros)
    print("DASHBOARD")
    print(f"*****************")
    return render_template('dashboard.html', id=id, periodo=periodo,empresa=empresa,periodo_id=periodo_id)


""" @main_bp.route('/tipo/<string:tipo>')
@login_required
def comercio(tipo=None):
    print('empresa tipo: ', tipo)

    empresas = Empresa.query.filter_by(usuario_id=current_user.get_id()).all()
    print("empresas: ",empresas)

    return render_template('dashboard.html', tipo=tipo, empresas=empresas)
 """
@main_bp.route('/test', methods=['get'])
@login_required
def test2():
    
    return render_template('test/test2.html')

@main_bp.route('/embarque', methods=['POST'])
@login_required
def embarque():
    if request.method == 'POST':
        return render_template('registrar_embarque.html')


@main_bp.route('/lista/embarque', methods=['POST'])
@login_required
def lista_embarque():
    if request.method == 'POST':
        periodo_id = session['periodo_id']
        lista_embarque = Embarque.query.filter_by(periodo_id=periodo_id).all()
        print('nro embarque: ', str(len(lista_embarque)))
        return render_template('lista_embarque.html', lista_embarque=lista_embarque)


@main_bp.route('/embarque/registrar', methods=['POST','GET'])
@login_required
def registrar_embarque():
    if request.method == 'POST':

        empresa_id = session['empresa_id']
        periodo_id = session['periodo_id']

        print('----- post embarque --------')
        print(f'empresa_id: {empresa_id} | periodo_id: {periodo_id}')
        dato = request.get_json()
        print(dato)

        print('fecha: ', dato['fecha'])
        print('detalle: ', dato['detalle'])
        print('detalle_totales: ', dato['detalle_totales'])
        print('extra: ', dato['extra'])
        if dato['fecha'] == '' or dato['detalle'] == [] or dato['detalle_totales'] == []:
            return jsonify(
                exito=False,
                title='Datos Incompletos',
                msg='Asegurese de ingresar fecha y detalles del embarque.'
            )

        new_embarque = Embarque(
            fecha=convertir_fecha(dato['fecha']),
            detalle=dato['detalle'],
            detalle_totales=dato['detalle_totales'],
            extra=dato['extra'],
            periodo_id=periodo_id
        )
        try:
            db.session.add(new_embarque)
            db.session.commit()
            return jsonify(
                exito=True,
                title='Exito!!',
                msg='Embarque registrado correctamente.'
            )
        except:
            return jsonify(
                exito=False,
                title='Error!!',
                msg='Error al registrar embarque.'
            )


@main_bp.route('/empresa/crear', methods=['GET', 'POST'])
@login_required
def crear_empresa():
    form = Crear_Empresa_Form()

    if request.method == 'POST':
        print('POST: CREANDO EMPRESA')
        nombre_empresa = escape(request.form.get('nombre_empresa'))
        rubro_empresa = escape(request.form.get('rubro_empresa'))
        parametros = {}
        print('nombre:', nombre_empresa)
        print('rubro: ', rubro_empresa)
        # crear una nueva empresa y asociarla al usuario
        new_empresa = Empresa(nombre_empresa=nombre_empresa, rubro_empresa=rubro_empresa,
                              parametros=parametros,
                              usuario_id=current_user.get_id())
        db.session.add(new_empresa)
        db.session.commit()
        print('Empresa registrada con exito')

        return redirect(url_for('main_bp.home'))

    return render_template('crear_empresa.html', form=form)


@main_bp.route('/empresa/<int:id>/crear-periodo', methods=['GET', 'POST'])
@login_required
def crear_periodo(id=None):
    form = Crear_Periodo_Form()

    if request.method == 'POST':
        print('POST: CREANDO periodo')
        periodo_fiscal = escape(request.form.get('periodo_fiscal'))
        inicio = convertir_fecha(escape(request.form.get('inicio')))
        termino = convertir_fecha(escape(request.form.get('termino')))
        print('usaurio: ', current_user.get_id())
        print('CREANDO PERIODO: ', periodo_fiscal)
        print('inicio: ', inicio)
        print('termino:', termino)

        new_periodo = Periodo(periodo_fiscal=periodo_fiscal, inicio=inicio,
                              termino=termino, empresa_id=id)

        db.session.add(new_periodo)
        db.session.commit()

        return redirect(url_for('main_bp.empresa', id=id))

    return render_template('crear_periodo.html', form=form)


@main_bp.route('/empresa/<int:id>/crear-parametros', methods=['GET', 'POST'])
@login_required
def crear_parametro(id=None):
    if request.method == 'POST':
        dato = request.get_json()
        print("Dato: ",dato)
        empresa = Empresa.query.filter_by(empresa_id=id).first()
        print(f'Empresa: {empresa} | nombre: {empresa.nombre_empresa} | rubro: {empresa.rubro_empresa}')
        print("|Parametros: ",empresa.parametros)

        if empresa.parametros == None:
            print("No existen parametros. -> Se procede a registrar.")
            empresa.parametros = {} 

        print("existe parametros. > se agrega nuevo parametros.")

        new_parametros = {}
        for key,value in empresa.parametros.items():
            print(f"key:{key} | val: {value}")
            new_parametros[key] = value

        if dato['tipo'] == 'lista':
            new_parametros[dato['nombre']] = {"tipo": "lista",
                                                "valor": []}
        elif dato['tipo'] == 'constante':
            new_parametros[dato['nombre']] = {"tipo": "constante",
                                                "valor": 0}
        else: 
            print("|Tipo de parametro no autorizado.")

        print("|New parametros: ", new_parametros)
        
        empresa.parametros = new_parametros
        db.session.commit()
        return jsonify(exito=True ,msg = "exito bro")
    

@main_bp.route('/empresa/<int:id>/parametros', methods=['GET', 'POST'])
@login_required
def parametros(id=None):
    if request.method == 'POST':
        print("args",request.args)
        empresa = Empresa.query.filter_by(empresa_id=id).first()
        print(f'Empresa: {empresa} | nombre: {empresa.nombre_empresa} | rubro: {empresa.rubro_empresa}')
        print("|Parametros: ",empresa.parametros)
        print("key: ",request.args.get('key'))
        print("|new value: ", request.args.get('new_value'))
        new_key = request.args.get('key')
        new_value = request.args.get('new_value')
        if not new_value or not new_key:
            print("Key no ingresada")
            return jsonify(exito=False , msg=True)
        
        if not new_key in empresa.parametros:
            print("key no existe en parametros.")
        
        new_parametros = dict(empresa.parametros)
        
        if new_parametros[new_key]['tipo'] == 'lista':
            print(f"Agregando {new_value} a value key: {new_key}")
            new_parametros[new_key]['valor'].append(new_value)
            
        
        dicc = {"parametros" : new_parametros}
        print("|Final parametros: ", new_parametros)
        #empresa.update_from_dict(dicc)
        
        
        empresa.parametros = {}
        db.session.commit()
        print("|Final empresa.parametros: ", empresa.parametros)
        empresa.parametros = new_parametros
        session["empresa_parametros"] = empresa.parametros
        db.session.commit()
        return jsonify(exito=True , msg=True)
        
    
    
    
# Liquidacion
@main_bp.route('/liquidacion', methods=['POST'])
@login_required
def liquidacion():
    if request.method == 'POST':
        print('OBTENIENDO COMPONENTE REGISTRAR LIQUIDACION ...')
        empresa_parametros = session["empresa_parametros"]
        print(empresa_parametros)
        clientes = empresa_parametros['cliente']['valor']
        print(clientes)
        return render_template('registrar_liquidacion.html',clientes=clientes)
    return render_template('registrar_liquidacion.html')


@main_bp.route('/lista/liquidacion', methods=['POST'])
@login_required
def lista_liquidacion():
    if request.method == 'POST':
        periodo_id = session['periodo_id']
        lista_liquidacion = Liquidacion.query.filter_by(
            periodo_id=periodo_id).all()
        print('nro liquidaciones: ', str(len(lista_liquidacion)))
        page = 'liquidacion'
       
      
        return render_template('lista_liquidacion.html', lista_liquidacion=lista_liquidacion, page=page)


@main_bp.route('/liquidacion/registrar', methods=['POST'])
@login_required
def registrar_liquidacion():
    if request.method == 'POST':
        dato = request.get_json()
        print("DATO: ", dato)
        periodo_id = session["periodo_id"]
        # ? FALTA SANITIZAR VALORES !!
        new_liquidacion = Liquidacion(
            fecha=dato["fecha"],
            detalle=dato["detalle"],
            detalles_extras=dato["detalles_extras"],
            total_venta=dato["total_venta"],
            total_descuento=dato["total_descuento"],
            total_pago=dato["total_pago"],
            periodo_id=periodo_id
        )
        try:
            db.session.add(new_liquidacion)
            db.session.commit()
            return jsonify(
                exito=True,
                title='Exito!!',
                msg='Liquidacion registrada correctamente.'
            )
        except:
            return jsonify(
                exito=False,
                title='Error!!',
                msg='Error al registrar Liquidacion.'
            )

@main_bp.route('/liquidacion/actualizar/<int:id>', methods=['POST','GET'])
@login_required
def actualizar_liquidacion(id = None):
    if request.method == 'POST':
        print('actualizando liquidacion ...')
        dato = request.get_json()
        print(dato)
        periodo_id = session["periodo_id"]
        # Se obtiene la liquidacion
        liquidacion = Liquidacion.query.filter_by(liquidacion_id = id).first()
        
        # ? FALTA SANITIZAR VALORES !!
        liquidacion.fecha=dato["fecha"]
        liquidacion.detalle=dato["detalle"]
        liquidacion.detalles_extras=dato["detalles_extras"]
        liquidacion.total_venta=dato["total_venta"]
        liquidacion.total_descuento=dato["total_descuento"]
        liquidacion.total_pago=dato["total_pago"]
        liquidacion.periodo_id=periodo_id
        
        try:
            db.session.add(liquidacion)
            db.session.commit()
            return jsonify(
                exito=True,
                title='Exito!!',
                msg='Liquidacion registrada correctamente.'
            )
        except:
            return jsonify(
                exito=False,
                title='Error!!',
                msg='Error al registrar Liquidacion.'
            )
    print("Obteniendo liquidacion: ", id)
    liquidacion = Liquidacion.query.filter_by(liquidacion_id = id).first()
    print("liquidacion: ", liquidacion)
    empresa_parametros = session["empresa_parametros"]
    print(empresa_parametros)
    clientes = empresa_parametros['cliente']['valor']
    print(clientes)
    return render_template("registrar_liquidacion.html", liquidacion = liquidacion,clientes=clientes)

@main_bp.route('/liquidacion/<int:id>', methods=['DELETE'])
@login_required
def eliminar_liquidacion(id=None):
    if request.method == 'DELETE':
         try:
            print(f'|Idea: Eliminar LIQUIDACION -> ',id)
            entidad = Liquidacion.query.filter_by(liquidacion_id=id).first()
            print(f'|LIQUIDACION a eliminar: ',entidad)
            db.session.delete(entidad)
            db.session.commit()
            data = {
                "class":"danger",
                "msg": f"Error al eliminar LIQUIDACION {id}.",
                "id": id 
            }
            return jsonify(status=True,title='Exito', msg=f'LIQUIDACION : {id} eliminado exitosamente.')
         except:
            return jsonify(status=False,title='Error', msg=f'Ocurrio un error al eliminar LIQUIDACION : {id}.')
         
@main_bp.route('/subir_csv', methods=['POST'])
@login_required
def subir_csv():
    if request.method == 'POST':
        print('--- POST CSV READ ----')
        try:
            csv_file = request.files['csv-file']
            csv_data = csv_file.read().decode('utf-8')
            csv_rows = csv_data.split('\n')
            #clave_valor = {}
            datos = []
            tabla_datos = []
            array_json_liquidacion = []
            print("Range: ", range(len(csv_rows)))
            for index in range(len(csv_rows)):
                row = csv_rows[index]
                cols = row.split(';')
                print(f"Row {index} : {row}")
                print(f"Cols {index} : {cols}")
                
                if index < 9:  # clave - valor => primeras 9 filas [0..8]
                    #clave_valor[cols[0]] = cols[1].replace('\r', '')
                    datos.append(cols[1].replace('\r', ''))

                elif index >= 9 and len(cols)>6:  # tabla => Resto de las filas
                    item_json = {
                        "producto": cols[0],
                        "cantidad": cols[1],
                        "precio_venta": cols[2],
                        "neto": cols[3],
                        "iva_guia": cols[4],
                        "precio": cols[5],
                        "total": cols[6].replace('\r', '')
                    }
                    array_json_liquidacion.append(item_json)
            print('--- datos ---')
            print(datos)
            array_json_liquidacion.pop(0)  # eliminar encabezados de la tabla
            # print(array_json_liquidacion)
            response = {
                'exito': True,
                'title': 'Exito',
                'msg': 'CSV examinado correctamente',
                'datos': datos,
                'tabla': array_json_liquidacion}
            return jsonify(response)
        except KeyError:
            response = {
                'exito': False,
                'title': 'Error',
                'msg': 'Error al examinar el CSV.',
                'datos': [],
                'tabla': []}
            return jsonify(response)

# OBTENER BACKUP