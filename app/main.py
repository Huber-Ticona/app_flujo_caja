from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
main_bp = Blueprint('main_bp', __name__,
                    static_folder='static', template_folder='templates')


@main_bp.route('/')
@login_required
def home():
    return render_template('home.html')


@main_bp.route('/comercio')
def comercio():
    return render_template('dashboard.html')


@main_bp.route('/parcela')
def parcela():
    return render_template('dashboard.html')


@main_bp.route('/parcela/embarque', methods=['POST'])
def embarque():
    if request.method == 'POST':
        return render_template('embarque.html')


@main_bp.route('/parcela/embarque/registrar', methods=['POST'])
def registrar_embarque():
    if request.method == 'POST':
        print('----- post embarque registro')
        dato = request.get_json()
        print(dato)
        return 'recibido'
