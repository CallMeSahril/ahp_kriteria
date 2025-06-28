from flask import Blueprint, render_template, request, redirect, url_for
from services.kriteria_service import get_all_kriteria, add_kriteria, update_kriteria, delete_kriteria

kriteria_bp = Blueprint('kriteria', __name__)

@kriteria_bp.route('/kriteria')
def home():
    return redirect(url_for('kriteria.list_kriteria'))

@kriteria_bp.route('/kriteria/', methods=['GET', 'POST'])

def list_kriteria():
    if request.method == 'POST':
        nama = request.form['nama']
        add_kriteria(nama)
        return redirect(url_for('kriteria.list_kriteria'))
    data = get_all_kriteria()
    return render_template('kriteria.html', data=data)

@kriteria_bp.route('/kriteria/edit/<int:id>', methods=['POST'])
def edit_kriteria(id):
    nama = request.form['nama']
    update_kriteria(id, nama)
    return redirect(url_for('kriteria.list_kriteria'))

@kriteria_bp.route('/kriteria/delete/<int:id>')
def hapus_kriteria(id):
    delete_kriteria(id)
    return redirect(url_for('kriteria.list_kriteria'))
