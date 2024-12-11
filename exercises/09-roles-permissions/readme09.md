# Ejercicio 9: Implementación de Roles y Permisos en una API Flask

## Objetivo
- **Implementar Roles y Permisos:** Aprender a asignar y gestionar diferentes niveles de acceso dentro de una API.
- **Control de Acceso:** Restringir o permitir el acceso a ciertas rutas o funcionalidades basado en el rol del usuario.
- **Mejora de la Seguridad:** Asegurar que solo los usuarios autorizados puedan realizar acciones específicas, aumentando la seguridad de la API.

## Descripción
En este ejercicio, ampliarás la API desarrollada en los ejercicios anteriores para incluir un sistema de roles y permisos. Asignarás roles a los usuarios (por ejemplo, "admin", "estudiante") y protegerás ciertas rutas para que solo sean accesibles por usuarios con roles específicos. Deberás completar los espacios en blanco en el código proporcionado para implementar esta funcionalidad.

## Requisitos
1. **Instalación de Dependencias Adicionales:**
   - Asegúrate de tener instalada la biblioteca `Flask` y las extensiones utilizadas en ejercicios anteriores.
   - Instala la biblioteca `Flask-Principal` para manejar roles y permisos:
     ```bash
     pip install Flask-Principal
     ```

2. **Estructura de la API:**
   - **Asignación de Roles:** Permitir asignar roles a los usuarios durante el registro o actualización.
   - **Protección de Rutas por Rol:** Restringir el acceso a ciertas rutas basado en el rol del usuario.

3. **Implementación de Roles y Permisos:**
   - Define diferentes roles (por ejemplo, "admin", "estudiante").
   - Asigna permisos específicos a cada rol.
   - Protege las rutas utilizando decoradores que verifiquen el rol del usuario.

4. **Pruebas:**
   - Utiliza herramientas como Postman o `curl` para probar el acceso a rutas protegidas con diferentes roles.
   - Asegúrate de que los usuarios solo puedan acceder a las rutas para las que tienen permisos.

## Pasos Sugeridos

### 1. Actualiza el Archivo `app.py`
- Importa las bibliotecas necesarias.
- Configura `Flask-Principal` para manejar roles y permisos.
- Define los roles y permisos.
- Modifica las rutas para asignar roles y proteger rutas específicas.

### 2. Desarrolla la Funcionalidad de Roles y Permisos en `app.py`

Completa el siguiente código en `ejercicios/09-implementacion-roles-permisos/app.py`, llenando los espacios en blanco indicados por `_____`:

```python
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
    from math import _____  # PISTA: Necesitas una función que redondee hacia arriba (en inglés "ceiling")

    app = Flask(__name__)
    auth = HTTPBasicAuth()

    # Configuración de JWT
    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_jwt'  # Cambia esto por una clave secreta segura
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
        role = data.get('role', 'student')  # Rol por defecto: 'student'
        
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

    # ... (código intermedio igual)

    @app.route('/usuarios', methods=['GET'])
    @jwt_required()
    def obtener_usuarios():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        total_users = len(usuarios)
        total_pages = _____(total_users / per_page)  # PISTA: Usa la función que importaste arriba para redondear hacia arriba

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

    @app.route('/usuarios/<username>', methods=['PUT'])
    @jwt_required()
    def actualizar_usuario(username):
        current_user = get_jwt_identity()
        
        if username not in usuarios:
            return jsonify({'message': 'User not found.'}), 404
        
        if not _____:  # PISTA: Usa el objeto admin_permission y el método que verifica si tiene permiso (can)
            return jsonify({'message': 'Permission denied.'}), 403
        
        data = request.get_json()
        password = data.get('password')
        role = data.get('role')
        
        if password:
            usuarios[username]['password'] = generate_password_hash(password)
        if role:
            usuarios[username]['role'] = role
        
        return jsonify({'message': 'User updated successfully.'}), 200

    @app.route('/usuarios/<username>', methods=['DELETE'])
    @jwt_required()
    @_____  # PISTA: Usa el decorador admin_permission.require() con el parámetro http_exception
    def eliminar_usuario(username):
        if username not in usuarios:
            return jsonify({'message': 'User not found.'}), 404
        
        del usuarios[username]
        return jsonify({'message': 'User deleted successfully.'}), 200

    @app.route('/admin/dashboard', methods=['GET'])
    @jwt_required()
    @_____  # PISTA: El mismo decorador que usaste arriba para requerir permiso de admin
    def admin_dashboard():
        return jsonify({'message': f'Bienvenido al dashboard de admin, {get_jwt_identity()}.'}), 200

    @app.route('/student/data', methods=['GET'])
    @jwt_required()
    @_____  # PISTA: Similar al decorador de admin, pero usa student_permission en su lugar
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