from flask import Blueprint, render_template
from services.perhitungan_service import hitung_bobot_kriteria, uji_konsistensi

perhitungan_bp = Blueprint('perhitungan', __name__)

@perhitungan_bp.route('/bobot')
def tampil_bobot():
    hasil = hitung_bobot_kriteria()
    konsistensi = uji_konsistensi()
    return render_template('bobot.html', hasil=hasil, konsistensi=konsistensi)
