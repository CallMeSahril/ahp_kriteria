from services.perbandingan_service import get_all_kriteria, get_matrix_nilai, simpan_perbandingan
from services.perbandingan_service import get_matrix_nilai
from flask import Blueprint, render_template, request, redirect, url_for
from services.perbandingan_service import get_all_kriteria, simpan_perbandingan

perbandingan_bp = Blueprint('perbandingan', __name__)


@perbandingan_bp.route('/perbandingan', methods=['GET', 'POST'])
def input_perbandingan():
    kriteria = get_all_kriteria()
    if request.method == 'POST':
        pairs = []
        for i in range(len(kriteria)):
            for j in range(i + 1, len(kriteria)):
                key = f'pair_{kriteria[i]["id_kriteria"]}_{kriteria[j]["id_kriteria"]}'
                nilai = request.form.get(key)
                if nilai:
                    pairs.append({
                        'k1': kriteria[i]['id_kriteria'],
                        'k2': kriteria[j]['id_kriteria'],
                        'nilai': float(nilai)
                    })
        simpan_perbandingan(pairs)
        return redirect(url_for('perbandingan.input_perbandingan'))

    kriteria, matrix = get_matrix_nilai()
    return render_template('perbandingan.html', kriteria=kriteria, matrix=matrix)


def tampil_matriks():
    kriteria, matrix = get_matrix_nilai()
    return render_template('tampil_matriks.html', kriteria=kriteria, matrix=matrix)
