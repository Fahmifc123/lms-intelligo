from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'intelligoid'  # Digunakan untuk mengamankan session

# Fungsi untuk memuat data pengguna dari file JSON
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan data pengguna ke file JSON
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Fungsi untuk memeriksa login
def check_login(username, password, users):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False

# Fungsi untuk mengubah kata sandi
def change_password(username, old_password, new_password, users):
    for user in users:
        if user['username'] == username and user['password'] == old_password:
            user['password'] = new_password
            save_users(users)
            return True
    return False

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if check_login(username, password, users):
        session['username'] = username  # Menyimpan username dalam session
        flash('Login berhasil!', 'success')
        return redirect(url_for('home'))
    flash('Nama pengguna atau kata sandi salah.', 'error')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Menghapus username dari session saat logout
    flash('Anda telah logout.', 'success')
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('index'))
    return render_template('home.html', username=session['username'])

@app.route('/change_password', methods=['GET', 'POST'])
def change_password_route():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu untuk mengubah password.', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        users = load_users()
        if change_password(session['username'], old_password, new_password, users):
            flash('Password berhasil diubah.', 'success')
            return redirect(url_for('logout'))
        else:
            flash('Password lama salah.', 'error')
    return render_template('change_password.html')

# Contoh lain dari route yang memerlukan autentikasi
@app.route('/intro_intelligo')
def intro_intelligo():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('index'))
    return render_template('intro_intelligo.html')

@app.route('/intro_datascience')
def intro_datascience():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('index'))
    return render_template('intro_datascience.html')

@app.route('/posttest_intro')
def posttest_intro():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('index'))
    return render_template('posttest_intro.html')

if __name__ == '__main__':
    app.run(debug=True, port=52420)

