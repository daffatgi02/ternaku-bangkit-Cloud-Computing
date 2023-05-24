from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import secrets
from flask_cors import CORS
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = secrets.token_hex(16)
mysql = MySQL(app)
CORS(app)


@app.route('/api/auth/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    fullname = request.json['fullname']  # Menambahkan pengambilan fullname

    # Check if email already exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({'error': True, 'message': 'Email already taken'})

    # Create a new user
    cur = mysql.connection.cursor()
    hashed_password = generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO users (email, password, fullname) VALUES (%s, %s, %s)", (email, hashed_password, fullname))  # Menyimpan fullname dalam database
    mysql.connection.commit()
    cur.close()

    return jsonify({'error': False, 'message': 'User Created'})



@app.route('/api/auth/getdetail', methods=['GET'])
def get_user_detail():
    token = request.headers.get('Authorization').split()[1]
    if not token:
        return jsonify({'error': True, 'message': 'Missing token'})
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['userid']
    except jwt.ExpiredSignatureError:
        return jsonify({'error': True, 'message': 'Invalid token'})

    cur = mysql.connection.cursor()
    cur.execute("SELECT email, fullname, user_id FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify(user)

    return jsonify({'error': True, 'message': 'User Not Found'})


@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user['password'], password):
        token = jwt.encode({'userid': user['user_id']}, app.config['SECRET_KEY'], algorithm='HS256')
        login_result = {
            'email': user['email'],
            'fullname': user['fullname'],
            'token': token,
            'userid': user['user_id']
        }
        return jsonify({'error': False, 'loginResult': login_result, 'message': 'Login Success'})

    return jsonify({'error': True, 'message': 'Wrong Password or Account not found'})


if __name__ == '__main__':
    app.run()