# routes/auth_route.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# Login halaman


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == 'admin@gmail.com' and password == 'tes123':
            session['user'] = email
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Email atau password salah')

    return render_template('login.html')


# Logout
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
