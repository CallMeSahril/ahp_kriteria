from flask import Blueprint, render_template
from db import get_connection
from weasyprint import HTML
from io import BytesIO
from flask import make_response
from datetime import datetime

riwayat_bp = Blueprint('riwayat', __name__)


@riwayat_bp.route('/riwayat/skoring')
def riwayat_skoring():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, waktu_upload FROM hasil_upload ORDER BY waktu_upload DESC")
    uploads = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('riwayat_upload.html', uploads=uploads)


@riwayat_bp.route('/riwayat/skoring/<int:upload_id>')
def riwayat_detail(upload_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM hasil_skoring WHERE upload_id = %s ORDER BY skor_total DESC", (upload_id,))
    hasil = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('riwayat_detail.html', hasil=hasil)


@riwayat_bp.route('/riwayat/skoring/<int:upload_id>/print')
def riwayat_detail_pdf(upload_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM hasil_skoring WHERE upload_id = %s ORDER BY skor_total DESC", (upload_id,))
    hasil = cursor.fetchall()
    cursor.close()
    conn.close()

    html = render_template('riwayat_detail_pdf.html',
                           hasil=hasil, now=datetime.now(), upload_id=upload_id)

    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers[
        'Content-Disposition'] = f'inline; filename=riwayat_skoring_{upload_id}.pdf'
    return response
