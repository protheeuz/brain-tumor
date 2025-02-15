from flask import Blueprint, request, render_template, redirect, url_for, session, flash, send_file, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import io
import qrcode
import pyotp

# Membuat Blueprint untuk otentikasi
auth = Blueprint('auth', __name__)

mysql = MySQL()

@auth.route('/check_username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
    user = cursor.fetchone()
    
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})

@auth.route('/generate_qr', methods=['GET'])
def generate_qr():
    email = request.args.get('email')
    if not email:
        return "Email is required", 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT otp_secret FROM user WHERE username = %s', (email,))
    user = cursor.fetchone()
    if not user or not user.get('otp_secret'):
        return "User not found or OTP not configured", 404

    otp_secret = user['otp_secret']
    totp = pyotp.TOTP(otp_secret)
    provisioning_uri = totp.provisioning_uri(name=email, issuer_name="Cancer Detection Platform")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@auth.route('/verify_qr', methods=['POST'])
def verify_qr():
    data = request.get_json()
    username = data.get('username')
    otp = data.get('otp')
    
    if not username or not otp:
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT otp_secret, role FROM user WHERE username = %s', (username,))
    user = cursor.fetchone()
    
    if not user or not user.get('otp_secret'):
        return jsonify({'status': 'error', 'message': 'OTP not configured for this user'}), 400

    totp = pyotp.TOTP(user['otp_secret'])
    if totp.verify(otp):
        session['username'] = username
        session['role'] = user['role']
        return jsonify({'status': 'success', 'redirect': url_for('dashboard')})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid OTP'}), 400

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['role'] = user['role']
            session['user_id'] = user['id_user']
            if user['role'] == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Password Salah', 'error')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@auth.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_user():
    nama = request.form['nama']
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash('Password tidak sesuai', 'error')
        return redirect(url_for('auth.register'))

    hashed_password = generate_password_hash(password)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash('Username sudah digunakan', 'error')
        return redirect(url_for('auth.register'))
    
    import pyotp
    otp_secret = pyotp.random_base32()
    
    cursor.execute('''
        INSERT INTO user (nama, username, password, role, otp_secret)
        VALUES (%s, %s, %s, 'pengunjung', %s)
    ''', (nama, username, hashed_password, otp_secret))
    mysql.connection.commit()

    flash('Pendaftaran berhasil! Kamu bisa langsung login.', 'success')
    return redirect(url_for('auth.login'))