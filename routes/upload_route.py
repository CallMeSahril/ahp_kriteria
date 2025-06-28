import os
import io
import pandas as pd
from flask import Blueprint, request, render_template, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from db import get_connection

upload_bp = Blueprint('upload_pesanan', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

# Fungsi: validasi ekstensi file


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi: konversi bahan ke skor kualitas (dummy rules)


def bahan_to_quality(bahan_nama):
    bahan_nama = (bahan_nama or '').lower()

    if 'stretch' in bahan_nama:
        return 9  # A
    elif 'ceruty' in bahan_nama:
        return 9  # A
    elif 'cringkle' in bahan_nama:
        if 'dobby' in bahan_nama:
            return 9  # A
        elif 'wavy' in bahan_nama:
            return 7  # B
        elif 'airflow' in bahan_nama:
            return 5  # C
    elif 'rayon' in bahan_nama:
        if 'silky' in bahan_nama or 'twill' in bahan_nama:
            return 9  # A
        elif 'super' in bahan_nama:
            return 7  # B
        elif 'biasa' in bahan_nama:
            return 5  # C
    elif 'poplin' in bahan_nama:
        return 9  # A
    elif 'jaquard silk' in bahan_nama:
        return 9  # A
    elif 'maxmara' in bahan_nama:
        return 9  # A
    elif 'saten' in bahan_nama:
        return 9  # A
    else:
        return 5  # default = C


# ROUTE: Upload dan Proses Excel Data Pesanan

@upload_bp.route('/upload/pesanan', methods=['GET', 'POST'])
def upload_pesanan():
    hasil = []

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            df = pd.read_excel(filepath)
            df.fillna('', inplace=True)

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # ✅ Tambahkan hasil_upload (sesi upload)
            cursor.execute("INSERT INTO hasil_upload () VALUES ()")
            upload_id = cursor.lastrowid

            # Ambil bobot
            cursor.execute("""
                SELECT k.nama_kriteria, b.bobot 
                FROM kriteria k 
                JOIN bobot_kriteria b ON k.id_kriteria = b.id_kriteria
            """)
            bobot_map = {row['nama_kriteria']: row['bobot']
                         for row in cursor.fetchall()}

            # Kelompokkan berdasarkan bahan
            grouped = df.groupby('Bahan')
            for bahan, group in grouped:
                nama = str(bahan).strip()
                total_pcs = group['Jml. Pcs'].sum()
                unique_kode = group['Kode Dsg.'].nunique()
                unique_warna = group['Warna'].nunique()

                kualitas = bahan_to_quality(nama)
                keunikan = min(9, 5 + unique_kode)
                kombinasi = min(9, 5 + unique_warna)
                tren = min(9, int(total_pcs / 10))

                skor = (
                    kualitas * bobot_map.get('Kualitas Bahan', 0) +
                    keunikan * bobot_map.get('Keunikan Motif', 0) +
                    kombinasi * bobot_map.get('Kombinasi Warna', 0) +
                    tren * bobot_map.get('Tren Pasar', 0)
                )

                hasil.append({
                    'nama_motif': nama,
                    'kualitas': kualitas,
                    'keunikan': keunikan,
                    'kombinasi': kombinasi,
                    'tren': tren,
                    'skor': round(skor, 4)
                })

                # ✅ Simpan ke hasil_skoring dengan upload_id
                cursor.execute("""
                    INSERT INTO hasil_skoring (
                        upload_id, nama_motif, kualitas_bahan, keunikan_motif,
                        kombinasi_warna, tren_pasar, skor_total
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    upload_id, nama, kualitas, keunikan, kombinasi, tren, skor
                ))

            hasil.sort(key=lambda x: x['skor'], reverse=True)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('upload_pesanan.html', hasil=hasil)

        flash('File harus berformat .xlsx')
        return render_template('upload_pesanan.html', hasil=[])

    return render_template('upload_pesanan.html', hasil=[])

# ROUTE: Download Template Excel


@upload_bp.route('/template/pesanan/download')
def download_template_pesanan():
    df = pd.DataFrame(columns=['Bahan', 'Kode Dsg.',
                      'Kode Lama', 'Warna', 'Jml. Pcs'])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Template_Pesanan')
    output.seek(0)

    return send_file(
        output,
        download_name="template_pesanan_kain.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
