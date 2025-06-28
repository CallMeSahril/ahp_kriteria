from flask import Blueprint, render_template, request
from db import get_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    selected_bulan = request.args.get('bulan')
    selected_tahun = request.args.get('tahun')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil daftar bulan/tahun upload
    cursor.execute("""
        SELECT DISTINCT MONTH(waktu_upload) AS bulan, YEAR(waktu_upload) AS tahun
        FROM hasil_upload
        ORDER BY tahun DESC, bulan DESC
    """)
    bulan_options = cursor.fetchall()

    # Default ke bulan & tahun terbaru jika belum dipilih
    if not selected_bulan or not selected_tahun:
        if bulan_options:
            selected_bulan = str(bulan_options[0]['bulan'])
            selected_tahun = str(bulan_options[0]['tahun'])

    # Ambil upload_id sesuai filter bulan/tahun
    cursor.execute("""
        SELECT id AS upload_id FROM hasil_upload 
        WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
    """, (selected_bulan, selected_tahun))
    upload_ids = [row['upload_id'] for row in cursor.fetchall()]
    if not upload_ids:
        upload_ids = [0]  # agar query tidak error jika kosong

    placeholders = ','.join(['%s'] * len(upload_ids))

    # Total upload
    cursor.execute("""
        SELECT COUNT(*) AS total FROM hasil_upload 
        WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
    """, (selected_bulan, selected_tahun))
    total_upload = cursor.fetchone()['total']

    # Waktu upload terakhir
    cursor.execute("""
        SELECT MAX(waktu_upload) AS terakhir FROM hasil_upload 
        WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
    """, (selected_bulan, selected_tahun))
    waktu_terakhir = cursor.fetchone()['terakhir']

    # Motif paling banyak
    cursor.execute(f"""
        SELECT nama_motif, COUNT(*) AS jumlah 
        FROM hasil_skoring 
        WHERE upload_id IN ({placeholders}) 
        GROUP BY nama_motif 
        ORDER BY jumlah DESC LIMIT 1
    """, upload_ids)
    motif_terbanyak = cursor.fetchone()

    # Rata-rata skor tertinggi
    cursor.execute(f"""
        SELECT nama_motif, AVG(skor_total) AS rata_rata 
        FROM hasil_skoring 
        WHERE upload_id IN ({placeholders}) 
        GROUP BY nama_motif 
        ORDER BY rata_rata DESC LIMIT 1
    """, upload_ids)
    rata_rata_tertinggi = cursor.fetchone()

    # Data untuk grafik
    cursor.execute(f"""
        SELECT nama_motif, skor_total 
        FROM hasil_skoring 
        WHERE upload_id IN ({placeholders}) 
        ORDER BY created_at DESC LIMIT 5
    """, upload_ids)
    chart_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html',
                           total_upload=total_upload,
                           waktu_terakhir=waktu_terakhir,
                           motif_terbanyak=motif_terbanyak,
                           rata_rata_tertinggi=rata_rata_tertinggi,
                           chart_data=chart_data,
                           bulan_options=bulan_options,
                           selected_bulan=int(selected_bulan),
                           selected_tahun=int(selected_tahun))
