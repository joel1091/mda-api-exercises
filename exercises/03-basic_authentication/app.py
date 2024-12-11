from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Base de datos simulada
usuarios = {}

@auth.verify_password
def verify_password(username, password):
    if username in usuarios and check_password_hash(usuarios.get(username), password):
        return username
    return None

@app.route('/usuarios', methods=['   '])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in usuarios:
        return jsonify({'message': 'User already exists.'}), 400
    
    # Hashear la contraseña antes de almacenarla
    usuarios[username] = _____(password)
    return jsonify({'message': 'User registered successfully.'}), 201

@app.route('/usuarios', methods=['   '])
@auth.login_required
def get_users():
    return jsonify({'users': list(usuarios.keys())}), 200

if __name__ == '__main__':
    app.run(debug=True)
