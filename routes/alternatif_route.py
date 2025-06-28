from flask import Blueprint, render_template, request, redirect, url_for
from services.alternatif_service import get_all_alternatif, add_alternatif, update_alternatif, delete_alternatif
from services.alternatif_service import hitung_skoring_alternatif

alternatif_bp = Blueprint('alternatif', __name__)

@alternatif_bp.route('/alternatif', methods=['GET', 'POST'])
@alternatif_bp.route('/alternatif/', methods=['GET', 'POST'])
def list_alternatif():
    if request.method == 'POST':
        nama = request.form['nama']
        add_alternatif(nama)
        return redirect(url_for('alternatif.list_alternatif'))
    data = get_all_alternatif()
    return render_template('alternatif.html', data=data)

@alternatif_bp.route('/alternatif/edit/<int:id>', methods=['POST'])
@alternatif_bp.route('/alternatif/edit/<int:id>/', methods=['POST'])
def edit_alternatif(id):
    nama = request.form['nama']
    update_alternatif(id, nama)
    return redirect(url_for('alternatif.list_alternatif'))

@alternatif_bp.route('/alternatif/delete/<int:id>')
@alternatif_bp.route('/alternatif/delete/<int:id>/')
def hapus_alternatif(id):
    delete_alternatif(id)
    return redirect(url_for('alternatif.list_alternatif'))

@alternatif_bp.route('/alternatif/skor')
def skor_alternatif():
    hasil = hitung_skoring_alternatif()
    return render_template('skor_alternatif.html', hasil=hasil)
