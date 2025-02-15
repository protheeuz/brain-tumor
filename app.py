import MySQLdb
from auth import auth
from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_mysqldb import MySQL
from deteksi import detect_image
from werkzeug.utils import secure_filename
from config import Config
from auth import generate_password_hash
import os
import logging
import pyotp


app = Flask(__name__)
app.config.from_object(Config)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# app.secret_key = os.urandom(24)

# Konfigurasi upload folder sudah diatur lewat config.py
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Inisialisasi MySQL dengan konfigurasi dari app.config
mysql = MySQL(app)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Import dan register Blueprint untuk otentikasi
app.register_blueprint(auth, url_prefix='/auth')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT COUNT(*) AS total_patients FROM riwayat_deteksi WHERE user_id = %s", (session['user_id'],))
        total_patients = cursor.fetchone()['total_patients']

        cursor.execute("SELECT COUNT(*) AS normal_patients FROM riwayat_deteksi WHERE user_id = %s AND hasil_label = 'notumor'", (session['user_id'],))
        normal_patients = cursor.fetchone()['normal_patients']

        cursor.execute("SELECT COUNT(*) AS pituitary_patients FROM riwayat_deteksi WHERE user_id = %s AND hasil_label = 'pituitary'", (session['user_id'],))
        pituitary_patients = cursor.fetchone()['pituitary_patients']

        cursor.execute("SELECT COUNT(*) AS meningioma_patients FROM riwayat_deteksi WHERE user_id = %s AND hasil_label = 'meningioma'", (session['user_id'],))
        meningioma_patients = cursor.fetchone()['meningioma_patients']

        cursor.execute("SELECT COUNT(*) AS glioma_patients FROM riwayat_deteksi WHERE user_id = %s AND hasil_label = 'glioma'", (session['user_id'],))
        glioma_patients = cursor.fetchone()['glioma_patients']

        cursor.close()

        # Pass the data to the dashboard template
        return render_template('dashboard.html', 
                               total_patients=total_patients, 
                               normal_patients=normal_patients,
                               pituitary_patients=pituitary_patients,
                               meningioma_patients=meningioma_patients,
                               glioma_patients=glioma_patients)
    return redirect(url_for('index'))

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if session.get('role') != 'admin':
        flash("Access denied: Admin only.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password tidak sesuai', 'danger')
            return render_template('add_user.html')

        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username sudah digunakan', 'danger')
            return render_template('add_user.html')

        otp_secret = pyotp.random_base32()

        cursor.execute(''' 
            INSERT INTO user (nama, username, password, role, otp_secret) 
            VALUES (%s, %s, %s, 'admin', %s)
        ''', (nama, username, hashed_password, otp_secret))
        mysql.connection.commit()

        flash('Admin berhasil dibuat!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_user.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Mengecek apakah file ada dalam request
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = detect_image(filepath)

            if 'user_id' not in session:
                flash('You must be logged in to perform this action.', 'danger')
                return redirect(url_for('auth.login'))

            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO riwayat_deteksi (user_id, hasil_label, confidence, created_at) 
                VALUES (%s, %s, %s, NOW())
            ''', (session['user_id'], result['tumor_type'], result['confidence']))
            mysql.connection.commit()

            return jsonify(result)
    return render_template('predict.html')

@app.route('/history')
def history():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT hasil_label, confidence, created_at FROM riwayat_deteksi WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
    riwayat_list = cursor.fetchall()
    cursor.close()
    return render_template('history.html', riwayat_list=riwayat_list)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
