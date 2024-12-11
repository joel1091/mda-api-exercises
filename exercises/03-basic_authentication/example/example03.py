
### **Solución Opcional (`ejercicios/02-autenticacion-basica/solucion/app.py`)**

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Base de datos simulada
estudiantes = {}

@auth.verify_password
def verificar_estudiante(nombre, contrasena):
    if nombre in estudiantes and check_password_hash(estudiantes.get(nombre), contrasena):
        return nombre
    return None

@app.route('/estudiantes', methods=['POST'])
def registrar_estudiante():
    datos = request.get_json()
    nombre = datos.get('username')
    contrasena = datos.get('password')
    
    if not nombre or not contrasena:
        return jsonify({'message': 'Nombre de usuario y contraseña son obligatorios.'}), 400
    if nombre in estudiantes:
        return jsonify({'message': 'El estudiante ya está registrado.'}), 400
    
    # Hashear la contraseña antes de almacenarla
    estudiantes[nombre] = generate_password_hash(contrasena)
    return jsonify({'message': 'Estudiante registrado exitosamente.'}), 201

@app.route('/estudiantes', methods=['GET'])
@auth.login_required
def obtener_estudiantes():
    return jsonify({'estudiantes': list(estudiantes.keys())}), 200

@app.errorhandler(404)
def recurso_no_encontrado(error):
    return jsonify({'error': 'Recurso no encontrado.'}), 404

@app.errorhandler(405)
def metodo_no_permitido(error):
    return jsonify({'error': 'Método no permitido.'}), 405

if __name__ == '__main__':
    app.run(debug=True)
