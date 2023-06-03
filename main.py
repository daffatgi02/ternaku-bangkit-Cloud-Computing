from flask import Flask, request, jsonify
import jwt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError
import secrets
from flask_cors import CORS
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import time
import pymysql.cursors
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
from google.cloud import storage
from io import BytesIO
import uuid

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = '34.143.132.191'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'daffa123'
app.config['MYSQL_DB'] = 'python'
app.config['MYSQL_CURSORCLASS'] = 'pymysql.cursors.DictCursor'
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
db = pymysql.connections.Connection(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)
jwt = JWTManager(app)
# key json google serviceacc
service_account_key_path = 'key.json'

model_bucket = 'ternaku-tes2'
sapi_model_blob = 'model_sapi.tflite'
kambing_model_blob = 'model_kambing.tflite'

def download_model_from_gcs(model_blob, model_path):
    storage_client = storage.Client.from_service_account_json(service_account_key_path)
    bucket = storage_client.bucket(model_bucket)
    blob = bucket.blob(model_blob)
    blob.download_to_filename(model_path)

def load_model(model_blob, model_path):
    try:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
    except FileNotFoundError:
        download_model_from_gcs(model_blob, model_path)
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

    return interpreter, input_details, output_details

def preprocess_image(image, input_shape):
    image = image.resize((input_shape[1], input_shape[2]))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32) / 255.0 
    return image

def predict_image(image, interpreter, input_details, output_details):
    image = preprocess_image(image, input_details[0]['shape'])
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = "Mata Terjangkit Penyakit Pinkeye" if output[0][0] < 0.5 else "Selamat Mata Kambing Kamu Sehat :)" 
    probability = output[0][0]

    return predicted_class, probability

bucket_name = 'ternaku-tes2'
image_folder = 'image'

def upload_image_to_gcs(image):
    filename = str(uuid.uuid4()) + '.jpg'
    storage_client = storage.Client.from_service_account_json(service_account_key_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{image_folder}/{filename}")
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    blob.upload_from_file(image_bytes, content_type='image/jpeg')
    return blob.public_url

def validate_token(token):
    if not token:
        return False, 'Missing token'

    try:
        decoded_token = decode_token(token)
        user_id = decoded_token['sub']
        return True, user_id
    except ExpiredSignatureError:
        return False, 'Token has expired. Please log in again.'
    except (JWTDecodeError, KeyError):
        return False, 'Invalid token. Please log in again.'


@app.route('/api/auth/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    fullname = request.json['fullname']

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({'error': True, 'message': 'Email already taken'})

    cur = db.cursor()
    hashed_password = generate_password_hash(password).decode('utf-8')
    cur.execute(
        "INSERT INTO users (email, password, fullname) VALUES (%s, %s, %s)",
        (email, hashed_password, fullname))
    db.commit()
    cur.close()

    return jsonify({'error': False, 'message': 'User Created'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user['password'], password):
        exp_time = datetime.utcnow() + timedelta(days=2)  # Set expiration time 2 days from now
        exp_time = int(time.mktime(exp_time.timetuple()))  # Convert to UNIX timestamp
        token = create_access_token(identity=user['user_id'], expires_delta=timedelta(days=2))
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

# Endpoint /predictsapi
@app.route('/api/predictsapi', methods=['POST'])
def predict_sapi():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    image_file = request.files['image']
    image = Image.open(image_file)

    interpreter, input_details, output_details = load_model(sapi_model_blob, 'model_sapi.tflite')

    image_url = upload_image_to_gcs(image)

    predicted_class, probability = predict_image(image, interpreter, input_details, output_details)

    result = {'class': predicted_class, 'probability': float(probability), 'image_url': image_url}
    return jsonify(result)

# Endpoint /predictkambing
@app.route('/api/predictkambing', methods=['POST'])
def predict_kambing():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    image_file = request.files['image']
    image = Image.open(image_file)

    interpreter, input_details, output_details = load_model(kambing_model_blob, 'model_kambing.tflite')

    image_url = upload_image_to_gcs(image)

    predicted_class, probability = predict_image(image, interpreter, input_details, output_details)

    result = {'class': predicted_class, 'probability': float(probability), 'image_url': image_url}
    return jsonify(result)

# Endpoint /api/products
@app.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()

    return jsonify(products)

# Endpoint /api/products/<int:product_id>
@app.route('/api/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if not product:
        return jsonify({'error': True, 'message': 'Product not found'})

    return jsonify({'error': False, 'product': product})

# Endpoint /api/articles
@app.route('/api/articles', methods=['GET'])
def get_articles():
    cur = db.cursor()
    cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    cur.close()

    return jsonify({'articles': articles})

# Endpoint /api/articles/<int:article_id>
@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cur.fetchone()
    cur.close()

    if article:
        return jsonify({'article': article})
    else:
        return jsonify({'error': 'Article not found'})

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    token = request.headers.get('Authorization').split()[1]
    is_valid, user_id = validate_token(token)

    if not is_valid:
        return jsonify({'error': True, 'message': user_id})

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'error': True, 'message': 'User not found'})

    profile = {
        'email': user['email'],
        'fullname': user['fullname']
    }

    return jsonify({'error': False, 'profile': profile})
    
# Endpoint homepage
@app.route('/homepage')
@jwt_required()
def homepage():
    token = request.headers.get('Authorization').split()[1]
    is_valid, user_id = validate_token(token)

    if not is_valid:
        return jsonify({'error': True, 'message': user_id})

    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({'error': True, 'message': 'User not found'})

    fullname = user['fullname']

    return f'Selamat Datang, {fullname}'


# Endpoint root
@app.route('/')
def index():
    return 'Welcome to the Ternaku'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
