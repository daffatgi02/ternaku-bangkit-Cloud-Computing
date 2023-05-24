from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)


@app.route('/api/auth/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        # Check password
        if user['password_hash'] == password:
            login_result = {
                'email': user['email'],
                'fullname': user['fullname'],
                'token': 'your_generated_token',
                'userid': user['id']
            }
            return jsonify({
                'error': False,
                'loginResult': login_result,
                'message': 'Login Success'
            })
        else:
            return jsonify({
                'error': True,
                'message': 'Wrong Password'
            })
    else:
        return jsonify({
            'error': True,
            'message': 'Account not found'
        })


@app.route('/api/auth/register', methods=['POST'])
def register():
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user:
        return jsonify({
            'error': True,
            'message': 'Email already taken'
        })
    else:
        password_salt = request.form['password_salt']
        password_hash = request.form['password_hash']

        cur.execute("INSERT INTO users (email, password_salt, password_hash) VALUES (%s, %s, %s)",
                    (email, password_salt, password_hash))
        mysql.connection.commit()
        cur.close()

        return jsonify({
            'error': False,
            'message': 'User Created'
        })


@app.route('/api/auth/getdetail', methods=['GET'])
def get_detail():
    token = request.headers.get('Authorization').split()[1]

    # You can decode the token and validate it here if necessary

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE token = %s", (token,))
    user = cur.fetchone()
    cur.close()

    if user:
        user_detail = {
            'email': user['email'],
            'fullname': user['fullname'],
            'user_id': user['id']
        }
        return jsonify(user_detail)
    else:
        return jsonify({
            'error': True,
            'message': 'User not found'
        })


if __name__ == '__main__':
    app.run()
