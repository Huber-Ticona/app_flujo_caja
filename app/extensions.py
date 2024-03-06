from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_minify import  Minify
from flask_wtf.csrf import CSRFProtect
import json
import bleach
import datetime
from sqlalchemy import inspect
from html import escape

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
minify = Minify( passive=True)
csrf = CSRFProtect()


def sanitize_json(input_json):
    if isinstance(input_json, list):
        # Si es una lista, aplicar la sanitización a cada elemento
        return [sanitize_json(item) for item in input_json]
    elif isinstance(input_json, dict):
        # Si es un diccionario, aplicar la sanitización a cada valor de forma recursiva
        return {key: sanitize_json(value) for key, value in input_json.items()}
    elif isinstance(input_json, str):
        # Si es una cadena, sanitizar el contenido HTML
        return bleach.clean(input_json, tags=[], attributes={})
    else:
        # Mantener otros tipos de datos sin cambios
        return input_json

def convertir_fecha(fecha_a):
    # Crear un objeto datetime a partir de la fecha en formato A usando el método strptime
    fecha_datetime = datetime.datetime.strptime(fecha_a, "%m/%d/%Y")
    # Formatear el objeto datetime a una cadena en formato B usando el método strftime
    fecha_b = fecha_datetime.strftime("%Y-%m-%d")
    # Devolver la fecha en formato B
    return fecha_b
def establecer_valores_por_defecto_formulario(formulario, modelo):
    for campo in formulario:
        print(f"-> Analisando Campo: {campo}")
        if hasattr(modelo, campo.name):
            valor_por_defecto = getattr(modelo, campo.name)
            campo.default = valor_por_defecto
            print(f"-> Campo: {campo} pertenece a la entidad: * |Defecto: {valor_por_defecto}")
            campo.process_data(campo.default)
        else:
            print(f"-> Campo: {campo} NO pertenece a la entidad: * |Defecto: {valor_por_defecto}")

def convertir_form_a_dict(request_form,form_tablas):
    new_data = {}
    for key, value in request_form.items():
            if key in form_tablas:
                print(f"|key: {key} | type: {type(request_form[key])} en form.tablas -> Se convierte en json")
                try:
                    new_data[key] = json.loads(request_form[key])
                except json.JSONDecodeError:
                    pass
            else:
                new_data[key] = request_form[key]
    return new_data

def get_fields_and_types(model):
    mapper = inspect(model)
    fields_and_types = []

    for column in mapper.columns:
        field_name = column.key
        field_type = column.type.python_type.__name__
        is_nullable = column.nullable  # True si el campo es nullable, False si no lo es

        fields_and_types.append({
            "name_field": field_name,
            "type": field_type,
            "nullable": 1 if is_nullable else 0
        })

    return fields_and_types

def model_to_dict(model):
    mapper = inspect(model)
    fields_and_types = {}

    for column in mapper.columns:
        field_name = column.key
        field_type = column.type.python_type.__name__
        fields_and_types[field_name] = field_type

    return fields_and_types

def model_to_dict2(model):
    mapper = inspect(model)
    fields_and_types = {}

    for column in mapper.columns:
        field_name = column.key
        field_type = column.type.python_type.__name__
        is_nullable = column.nullable

        fields_and_types[field_name] = {
            "type": field_type,
            "nullable": 1 if is_nullable else 0
        }

    return fields_and_types
def sanitize_and_validate(data, model_rules):
    sanitized_data = {}

    for key, value in data.items():
        if key in model_rules:
            rule = model_rules[key]
            expected_type = rule.get('type')
            nullable = rule.get('nullable', False)

            if value is None and nullable:
                # Si el valor es nulo y el campo es nullable, acepta el valor nulo
                sanitized_data[key] = value
            elif expected_type == 'int':
                # Si se espera un entero, intenta convertir a entero
                try:
                    sanitized_data[key] = int(value)
                except (ValueError, TypeError):
                    # Si la conversión falla, puedes manejar el error aquí según tus necesidades
                    sanitized_data[key] = None
            elif expected_type == 'str':
                # Si se espera una cadena, escapa la cadena
                sanitized_data[key] = escape(value)
            else:
                # Puedes agregar lógica adicional para otros tipos según sea necesario
                sanitized_data[key] = value
        else:
            # Si no hay reglas definidas para el campo, acepta el valor sin cambios
            sanitized_data[key] = value

    return sanitized_data