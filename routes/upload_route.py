import os
import io
import pandas as pd
from flask import Blueprint, request, render_template, flash, send_file
from werkzeug.utils import secure_filename
from db import get_connection

upload_bp = Blueprint('upload_pesanan', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def bahan_to_quality(bahan_nama):
    bahan_nama = (bahan_nama or '').lower()
    if 'stretch' in bahan_nama:
        return 9
    elif 'ceruty' in bahan_nama:
        return 9
    elif 'cringkle' in bahan_nama:
        if 'dobby' in bahan_nama:
            return 9
        elif 'wavy' in bahan_nama:
            return 7
        elif 'airflow' in bahan_nama:
            return 5
    elif 'rayon' in bahan_nama:
        if 'silky' in bahan_nama or 'twill' in bahan_nama:
            return 9
        elif 'super' in bahan_nama:
            return 7
        elif 'biasa' in bahan_nama:
            return 5
    elif 'poplin' in bahan_nama:
        return 9
    elif 'jaquard silk' in bahan_nama:
        return 9
    elif 'maxmara' in bahan_nama:
        return 9
    elif 'saten' in bahan_nama:
        return 9
    else:
        return 5


@upload_bp.route('/upload/pesanan', methods=['GET', 'POST'])
def upload_pesanan():
    hasil = []
    bulan = tahun = None

    if request.method == 'POST':
        # Ambil bulan dan tahun dari form
        bulan = request.form.get('bulan', type=int)
        tahun = request.form.get('tahun', type=int)

        if not bulan or not tahun:
            flash('Bulan dan Tahun wajib diisi.')
            return render_template('upload_pesanan.html', hasil=[], bulan=bulan, tahun=tahun)

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            df = pd.read_excel(filepath)
            df.fillna('', inplace=True)

            # Filter baris tanpa "Kode Dsg."
            df = df[~df['Kode Dsg.'].isin(['', '-', None])]

            if df.empty:
                flash('Data kosong atau semua "Kode Dsg." tidak valid.')
                return render_template('upload_pesanan.html', hasil=[], bulan=bulan, tahun=tahun)

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            # Tambahkan sesi upload dengan bulan dan tahun
            cursor.execute(
                "INSERT INTO hasil_upload (bulan, tahun) VALUES (%s, %s)", (bulan, tahun))
            upload_id = cursor.lastrowid

            # Ambil bobot AHP
            cursor.execute("""
                SELECT k.nama_kriteria, b.bobot 
                FROM kriteria k 
                JOIN bobot_kriteria b ON k.id_kriteria = b.id_kriteria
            """)
            bobot_ahp = {row['nama_kriteria']: row['bobot']
                         for row in cursor.fetchall()}

            # Data untuk normalisasi
            max_warna_variasi = df.groupby(
                'Kode Dsg.')['Warna'].nunique().max()
            max_total_pcs = df.groupby('Kode Dsg.')['Jml. Pcs'].sum().max()
            max_kemunculan = df.groupby('Kode Dsg.').size().max()

            for kode_dsg in df['Kode Dsg.'].dropna().unique():
                subset = df[df['Kode Dsg.'] == kode_dsg]

                kode_desain = str(kode_dsg).strip()
                bahan = str(subset['Bahan'].iloc[0]).strip()
                warna = str(subset['Warna'].iloc[0]).strip(
                ) if not subset['Warna'].empty else ''
                total_pcs = subset['Jml. Pcs'].sum()
                warna_unik = subset['Warna'].nunique()
                jumlah_kemunculan = len(subset)

                kualitas = bahan_to_quality(bahan)
                keunikan = round(
                    (jumlah_kemunculan / max_kemunculan) * 9) if max_kemunculan else 5
                keunikan = min(9, max(1, keunikan))
                kombinasi = round((warna_unik / max_warna_variasi)
                                  * 9) if max_warna_variasi else 5
                tren = round((total_pcs / max_total_pcs)
                             * 9) if max_total_pcs else 5

                skor = (
                    kualitas * bobot_ahp.get('Kualitas Bahan', 0) +
                    keunikan * bobot_ahp.get('Keunikan Motif', 0) +
                    kombinasi * bobot_ahp.get('Kombinasi Warna', 0) +
                    tren * bobot_ahp.get('Tren Pasar', 0)
                )

                hasil.append({
                    'nama_motif': kode_desain,
                    'kualitas': kualitas,
                    'keunikan': keunikan,
                    'kombinasi': kombinasi,
                    'tren': tren,
                    'skor': round(skor, 4)
                })

                cursor.execute("""
                    INSERT INTO hasil_skoring (
                        upload_id, nama_motif, warna, kualitas_bahan, keunikan_motif,
                        kombinasi_warna, tren_pasar, skor_total
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    upload_id, kode_desain, warna, kualitas, keunikan, kombinasi, tren, skor
                ))

            hasil.sort(key=lambda x: x['skor'], reverse=True)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('upload_pesanan.html', hasil=hasil, bulan=bulan, tahun=tahun)

        flash('File harus berformat .xlsx')
        return render_template('upload_pesanan.html', hasil=[], bulan=bulan, tahun=tahun)

    return render_template('upload_pesanan.html', hasil=[])


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
