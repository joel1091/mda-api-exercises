# Ejercicio 9: Implementación de Roles y Permisos en una API Flask

## Solución

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_principal import (
    Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, AnonymousIdentity, identity_changed
)

import os
from math import ceil

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_jwt'
jwt = JWTManager(app)

# Configuración de Flask-Principal
app.config['SECRET_KEY'] = 'tu_clave_secreta_flask'
principals = Principal(app)

# Definición de Roles
admin_permission = Permission(RoleNeed('admin'))
student_permission = Permission(RoleNeed('student'))

# Base de datos simulada para almacenar usuarios
usuarios = {
    # 'nombre_usuario': {'password': 'hashed_password', 'api_key': 'api_key', 'role': 'admin'}
}

@auth.verify_password
def verify_password(username, password):
    if username in usuarios and check_password_hash(usuarios.get(username)['password'], password):
        return username
    return None

@app.route('/usuarios', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in usuarios:
        return jsonify({'message': 'User already exists.'}), 400
    
    usuarios[username] = {
        'password': generate_password_hash(password),
        'api_key': 'api_key_placeholder',
        'role': role
    }
    return jsonify({'message': 'User registered successfully.'}), 201

@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    current_user = auth.current_user()
    access_token = create_access_token(identity=current_user)
    identity_changed.send(app, identity=Identity(current_user))
    return jsonify({'access_token': access_token}), 200

@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    current_user = get_jwt_identity()
    return jsonify({'perfil': f'Información del perfil de {current_user}'}), 200

# Asignación de Roles después de la carga de la identidad
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = identity.id
    identity.provides.add(UserNeed(identity.id))
    
    if identity.id in usuarios:
        role = usuarios[identity.id].get('role')
        if role:
            identity.provides.add(RoleNeed(role))

# Crear Usuario con Roles
@app.route('/usuarios', methods=['POST'])
@jwt_required()
def crear_usuario():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in usuarios:
        return jsonify({'message': 'User already exists.'}), 400
    
    usuarios[username] = {
        'password': generate_password_hash(password),
        'api_key': 'api_key_placeholder',
        'role': role
    }
    return jsonify({'message': 'User created successfully.'}), 201

# Obtener Usuarios con Paginación
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    total_users = len(usuarios)
    total_pages = ceil(total_users / per_page)
    
    if page > total_pages or page < 1:
        return jsonify({'message': 'Page not found.'}), 404
    
    start = (page - 1) * per_page
    end = start + per_page
    users_list = list(usuarios.keys())[start:end]
    
    return jsonify({
        'users': users_list,
        'total_pages': total_pages,
        'current_page': page
    }), 200

# Actualizar Usuario
@app.route('/usuarios/<username>', methods=['PUT'])
@jwt_required()
def actualizar_usuario(username):
    current_user = get_jwt_identity()
    
    if username not in usuarios:
        return jsonify({'message': 'User not found.'}), 404
    
    if not admin_permission.can():
        return jsonify({'message': 'Permission denied.'}), 403
    
    data = request.get_json()
    password = data.get('password')
    role = data.get('role')
    
    if password:
        usuarios[username]['password'] = generate_password_hash(password)
    if role:
        usuarios[username]['role'] = role
    
    return jsonify({'message': 'User updated successfully.'}), 200

# Eliminar Usuario
@app.route('/usuarios/<username>', methods=['DELETE'])
@jwt_required()
@admin_permission.require(http_exception=403)
def eliminar_usuario(username):
    if username not in usuarios:
        return jsonify({'message': 'User not found.'}), 404
    
    del usuarios[username]
    return jsonify({'message': 'User deleted successfully.'}), 200

# Ruta protegida solo para administradores
@app.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@admin_permission.require(http_exception=403)
def admin_dashboard():
    return jsonify({'message': f'Bienvenido al dashboard de admin, {get_jwt_identity()}.'}), 200

# Ruta protegida solo para estudiantes
@app.route('/student/data', methods=['GET'])
@jwt_required()
@student_permission.require(http_exception=403)
def student_data():
    return jsonify({'message': f'Datos del estudiante {get_jwt_identity()}.'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found.'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed.'}), 405

if __name__ == '__main__':
    app.run(debug=True)
