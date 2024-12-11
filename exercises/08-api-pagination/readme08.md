# Ejercicio 8: Implementación de Paginación en Endpoints

## Objetivo
- **Implementar Paginación en Endpoints:** Aprender a manejar grandes conjuntos de datos dividiéndolos en páginas más pequeñas.
- **Optimización de Respuestas:** Mejorar la eficiencia y usabilidad de la API al limitar la cantidad de datos retornados en cada solicitud.
- **Manejo de Parámetros de Consulta:** Utilizar parámetros de consulta para controlar la paginación.

## Descripción
En este ejercicio, ampliarás la API desarrollada en los ejercicios anteriores para incluir paginación en la ruta que retorna la lista de "estudiantes". La paginación permitirá a los usuarios solicitar un subconjunto específico de estudiantes en cada solicitud, mejorando la eficiencia y manejabilidad de las respuestas. Deberás completar los espacios en blanco en el código proporcionado para implementar esta funcionalidad.

## Requisitos
1. **Instalación de Dependencias Adicionales:**
   - Asegúrate de tener instalada la biblioteca `Flask` y las extensiones utilizadas en ejercicios anteriores.
   - Instala la biblioteca `math` si aún no la tienes (aunque generalmente viene incluida con Python):
     ```bash
     pip install math
     ```

2. **Estructura de la API:**
   - **Ruta Paginada (`GET /estudiantes`):** Retorna una lista paginada de estudiantes, permitiendo especificar el número de página y la cantidad de estudiantes por página mediante parámetros de consulta.

3. **Implementación de Paginación:**
   - Utiliza parámetros de consulta como `page` y `per_page` para controlar la paginación.
   - Calcula los índices de inicio y fin para retornar el subconjunto correcto de estudiantes.
   - Retorna información adicional como el número total de páginas y el número actual de página.

4. **Pruebas:**
   - Utiliza herramientas como Postman o `curl` para probar la paginación, solicitando diferentes páginas y tamaños de página.
   - Asegúrate de que la paginación funcione correctamente y que se manejen los errores de manera adecuada (por ejemplo, páginas fuera de rango).

## Pasos Sugeridos

### 1. Actualiza el Archivo `app.py`
- Importa las bibliotecas necesarias.
- Modifica la ruta para obtener estudiantes (`GET /estudiantes`) para que soporte paginación.

### 2. Desarrolla la Paginación en `app.py`

Completa el siguiente código en `ejercicios/07-implementacion-paginacion-endpoints/app.py`, llenando los espacios en blanco indicados por `_____`:

```python
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from math import _____  # Importa la función necesaria para la paginación
import secrets
from urllib.parse import urlencode

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_jwt'  # Cambia esto por una clave secreta segura
jwt = JWTManager(app)

# Base de datos simulada para almacenar estudiantes
estudiantes = {
    # 'nombre_estudiante': {'password': 'hashed_password', 'api_key': 'api_key'}
}

@auth.verify_password
def verify_password(username, password):
    if username in estudiantes and check_password_hash(estudiantes.get(username)['password'], password):
        return username
    return None

@app.route('/register', methods=['POST'])
def register_student():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in estudiantes:
        return jsonify({'message': 'User already exists.'}), 400
    
    estudiantes[username] = {
        'password': generate_password_hash(password),
        'api_key': secrets.token_hex(16)  # Genera una API Key segura
    }
    return jsonify({'message': 'User registered successfully.', 'api_key': estudiantes[username]['api_key']}), 201

@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    current_user = auth.current_user()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200

@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    current_user = get_jwt_identity()
    return jsonify({'perfil': f'Información del perfil de {current_user}'}), 200

# Crear Estudiante
@app.route('/estudiantes', methods=['POST'])
@jwt_required()
def crear_estudiante():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in estudiantes:
        return jsonify({'message': 'Student already exists.'}), 400
    
    estudiantes[username] = {
        'password': generate_password_hash(password),
        'api_key': secrets.token_hex(16)  # Genera una API Key segura
    }
    return jsonify({'message': 'Student created successfully.'}), 201

# Obtener Estudiantes con Paginación
@app.route('/estudiantes', methods=['GET'])
@jwt_required()
def obtener_estudiantes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if per_page <= 0:
            return jsonify({'message': 'per_page debe ser un entero positivo.'}), 400
        if per_page > 100:
            per_page = 100  # Límite máximo
        
        total_students = len(estudiantes)
        total_pages = _____(total_students, per_page)  # Completa la función para calcular total_pages
        
        if page > total_pages or page < 1:
            return jsonify({'message': 'Página no encontrada.'}), 404
        
        start = (page - 1) * per_page
        end = start + per_page
        students_list = list(estudiantes.keys())[start:end]
        
        base_url = request.base_url
        query_params = request.args.to_dict()
        
        def build_url(new_page):
            query = query_params.copy()
            query['page'] = new_page
            return f"{base_url}?{urlencode(query)}"
        
        links = {}
        if page > 1:
            links['prev'] = build_url(page - 1)
        if page < total_pages:
            links['next'] = build_url(page + 1)
        
        return jsonify({
            'students': students_list,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'total_students': total_students,
            'links': links
        }), 200
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al procesar la solicitud.', 'details': str(e)}), 500

# Actualizar Estudiante
@app.route('/estudiantes/<username>', methods=['PUT'])
@jwt_required()
def actualizar_estudiante(username):
    if username not in estudiantes:
        return jsonify({'message': 'Student not found.'}), 404
    
    data = request.get_json()
    password = data.get('password')
    
    if password:
        estudiantes[username]['password'] = generate_password_hash(password)
        return jsonify({'message': 'Student updated successfully.'}), 200
    else:
        return jsonify({'message': 'Nothing to update.'}), 400

# Eliminar Estudiante
@app.route('/estudiantes/<username>', methods=['DELETE'])
@jwt_required()
def eliminar_estudiante(username):
    if username not in estudiantes:
        return jsonify({'message': 'Student not found.'}), 404
    
    del estudiantes[username]
    return jsonify({'message': 'Student deleted successfully.'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found.'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed.'}), 405

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'Ocurrió un error inesperado.', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)