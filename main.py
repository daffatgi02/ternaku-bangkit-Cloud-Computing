from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import secrets
from flask_cors import CORS
import jwt
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = secrets.token_hex(16)
mysql = MySQL(app)
CORS(app)


def validate_token(token):
    if not token:
        return False, 'Missing token'
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['userid']
        return True, user_id
    except jwt.ExpiredSignatureError:
        return False, 'Token Invalid. Please login or register!'
    except jwt.DecodeError:
        return False, 'Token Invalid. Please login or register!'


@app.route('/api/products', methods=['GET'])
def get_products():
    token = request.headers.get('Authorization', '').split()[1]
    valid_token, user_id = validate_token(token)
    if not valid_token:
        return jsonify({'error': True, 'message': user_id}), 500

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return jsonify({'products': products})


@app.route('/api/articles', methods=['GET'])
def get_articles():
    token = request.headers.get('Authorization', '').split()[1]
    valid_token, user_id = validate_token(token)
    if not valid_token:
        return jsonify({'error': True, 'message': user_id}), 500

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    cur.close()
    return jsonify({'articles': articles})


@app.route('/api/auth/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    fullname = request.json['fullname']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({'error': True, 'message': 'Email already taken'})

    cur = mysql.connection.cursor()
    hashed_password = generate_password_hash(password).decode('utf-8')
    cur.execute(
        "INSERT INTO users (email, password, fullname) VALUES (%s, %s, %s)",
        (email, hashed_password, fullname))
    mysql.connection.commit()
    cur.close()

    return jsonify({'error': False, 'message': 'User Created'})


@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user['password'], password):
        exp_time = datetime.utcnow() + timedelta(days=2)  # Set expiration time 2 days from now
        exp_time = int(time.mktime(exp_time.timetuple()))  # Convert to UNIX timestamp
        token = jwt.encode({
            'userid': user['user_id'],
            'exp': exp_time
        },
            app.config['SECRET_KEY'],
            algorithm='HS256')
        login_result = {
            'email': user['email'],
            'fullname': user['fullname'],
            'token': token,
            'userid': user['user_id']
        }
        return jsonify({
            'error': False,
            'loginResult': login_result,
            'message': 'Login Success'
        })

    return jsonify({
        'error': True,
        'message': 'Wrong Password or Account not found'
    })


@app.route('/api/auth/getdetail', methods=['GET'])
def get_user_detail():
    token = request.headers.get('Authorization', '').split()[1]
    valid_token, user_id = validate_token(token)
    if not valid_token:
        return jsonify({'error': True, 'message': user_id}), 500

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT email, fullname, user_id FROM users WHERE user_id = %s",
        (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify(user)

    return jsonify({'error': True, 'message': 'User Not Found'}), 500


@app.route('/api/homepage', methods=['GET'])
def get_homepage():
    token = request.headers.get('Authorization', '').split()[1]
    valid_token, user_id = validate_token(token)
    if not valid_token:
        return jsonify({'error': True, 'message': user_id}), 500

    cur = mysql.connection.cursor()
    cur.execute("SELECT fullname FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({
            'message':
            f"Hello! Welcome to the homepage, {user['fullname']}."
        })

    return jsonify({'error': True, 'message': 'User Not Found'}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    token = request.headers.get('Authorization', '').split()[1]
    valid_token, user_id = validate_token(token)
    if not valid_token:
        return jsonify({'error': True, 'message': user_id}), 500

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if product:
        return jsonify({'product': product})

    return jsonify({'error': True, 'message': 'Product Not Found'}), 404


@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    token = request.headers.get('Authorization', '').split()[1]
    valid_token, user_id = validate_token(token)
    if not valid_token:
        return jsonify({'error': True, 'message': user_id}), 500

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cur.fetchone()
    cur.close()

    if article:
        return jsonify({'article': article})

    return jsonify({'error': True, 'message': 'Article Not Found'}), 404


if __name__ == '__main__':
    app.run()
