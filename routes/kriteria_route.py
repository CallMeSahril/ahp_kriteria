from flask import Blueprint, render_template, request, redirect, url_for
from services.kriteria_service import get_all_kriteria, add_kriteria, update_kriteria, delete_kriteria
from flask import make_response, render_template
from weasyprint import HTML
from io import BytesIO
from datetime import datetime


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


@kriteria_bp.route('/kriteria/print')
def print_kriteria():
    data = get_all_kriteria()
    html = render_template('kriteria_pdf.html', data=data, now=datetime.now())

    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=daftar_kriteria.pdf'
    return response


@kriteria_bp.route('/kriteria/print/pdf')
def print_kriteria_pdf():
    data = get_all_kriteria()
    print(data)  #

    html = render_template('kriteria_pdf.html',
                           data=data,
                           now=datetime.now())

    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=daftar_kriteria.pdf'
    return response
