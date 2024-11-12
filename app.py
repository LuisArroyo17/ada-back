from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from main_logic import generar_grafico, determinar_tiempos_de_ejecucion


app = Flask(__name__)
app.secret_key = 'your_secret_key'  


@app.route('/')
def index():
    return redirect(url_for('iniciar_sesion'))

# Ruta para registrarse
@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')

        usuarios_registrados = session.get('usuarios', {})
        if correo in usuarios_registrados:
            return "Este correo ya está registrado", 400

        usuarios_registrados[correo] = {"nombre": nombre, "password": password}
        session['usuarios'] = usuarios_registrados

        return redirect(url_for('iniciar_sesion'))

    return render_template('registrarse.html')


@app.route('/iniciarsesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuarios_registrados = session.get('usuarios', {})
        if username in usuarios_registrados and usuarios_registrados[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('elegir_lenguaje'))
        else:
            return "Usuario o contraseña incorrectos", 401

    return render_template('iniciarsesion.html')

@app.route('/elegirlenguaje', methods=['GET', 'POST'])
def elegir_lenguaje():
    if request.method == 'POST':
        lenguaje = request.form.get('lenguaje')
        session['lenguaje'] = lenguaje
        return redirect(url_for('num_codigos'))
    return render_template('elegirlenguaje.html')

@app.route('/numcodigos', methods=['GET', 'POST'])
def num_codigos():
    if request.method == 'POST':
        try:
            num_codigos = int(request.form.get('num_codigos'))
            if num_codigos < 2 or num_codigos > 10:
                return "Número de códigos no válido. Debe ser entre 2 y 10.", 400
        except ValueError:
            return "Entrada no válida. Por favor, ingresa un número.", 400

        session['num_codigos'] = num_codigos
        return redirect(url_for('comparacion_vista'))
    return render_template('numcodigos.html')

@app.route('/comparacionvista', methods=['GET', 'POST'])
def comparacion_vista():
    num_codigos = session.get('num_codigos', 2)
    if request.method == 'POST':
        files = request.files.getlist('files')

        if not files or len(files) != num_codigos:
            return f"Por favor, sube exactamente {num_codigos} archivos.", 400

        for file in files:
            if file.filename == '':
                return "Uno o más archivos no tienen nombre.", 400

        codigos = {}
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                codigos[filename] = f.read()

        tiempos = determinar_tiempos_de_ejecucion(codigos)

        # Genera el gráfico
        grafico_filename = generar_grafico("comparacion", tiempos)
        grafico_url = url_for('static', filename=f'img/{grafico_filename}')

        return render_template('ComparacionVista.html', grafico_url=grafico_url, num_codigos=num_codigos)
    else:
        return render_template('ComparacionVista.html', num_codigos=num_codigos)

if __name__ == '__main__':
    os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join('static', 'img'), exist_ok=True)
    app.run(debug=True, use_reloader=False)
