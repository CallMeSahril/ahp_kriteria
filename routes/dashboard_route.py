from io import BytesIO
from weasyprint import HTML
from flask import make_response, Blueprint, render_template, request
from db import get_connection
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/', methods=['GET'])
def dashboard():
    filter_bulan = request.args.get('filter_bulan')
    selected_bulan = request.args.get('bulan')
    selected_tahun = request.args.get('tahun')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil daftar bulan/tahun
    cursor.execute("""
        SELECT DISTINCT MONTH(waktu_upload) AS bulan, YEAR(waktu_upload) AS tahun
        FROM hasil_upload
        ORDER BY tahun DESC, bulan DESC
    """)
    bulan_options = cursor.fetchall()

    try:
        selected_tahun = int(selected_tahun)
    except (TypeError, ValueError):
        selected_tahun = bulan_options[0]['tahun'] if bulan_options else 2023

    if filter_bulan:
        try:
            selected_bulan = int(selected_bulan)
        except (TypeError, ValueError):
            selected_bulan = bulan_options[0]['bulan'] if bulan_options else 1
    else:
        selected_bulan = None

    # Dapatkan upload_ids sesuai filter
    if selected_bulan is not None:
        cursor.execute("""
            SELECT id AS upload_id FROM hasil_upload
            WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
        """, (selected_bulan, selected_tahun))
    else:
        cursor.execute("""
            SELECT id AS upload_id FROM hasil_upload
            WHERE YEAR(waktu_upload) = %s
        """, (selected_tahun,))

    upload_ids = [row['upload_id'] for row in cursor.fetchall()] or [0]
    placeholders = ','.join(['%s'] * len(upload_ids))
    params = tuple(upload_ids)

    # Total upload
    if selected_bulan is not None:
        cursor.execute("""
            SELECT COUNT(*) AS total FROM hasil_upload
            WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
        """, (selected_bulan, selected_tahun))
    else:
        cursor.execute("""
            SELECT COUNT(*) AS total FROM hasil_upload
            WHERE YEAR(waktu_upload) = %s
        """, (selected_tahun,))
    total_upload = cursor.fetchone()['total'] or 0

    # Upload terakhir
    if selected_bulan is not None:
        cursor.execute("""
            SELECT MAX(waktu_upload) AS terakhir FROM hasil_upload
            WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
        """, (selected_bulan, selected_tahun))
    else:
        cursor.execute("""
            SELECT MAX(waktu_upload) AS terakhir FROM hasil_upload
            WHERE YEAR(waktu_upload) = %s
        """, (selected_tahun,))
    waktu_terakhir = cursor.fetchone()['terakhir']

    # Motif terbanyak
    cursor.execute(f"""
        SELECT nama_motif, COUNT(*) AS jumlah
        FROM hasil_skoring
        WHERE upload_id IN ({placeholders})
        GROUP BY nama_motif
        ORDER BY jumlah DESC
        LIMIT 1
    """, params)
    motif_terbanyak = cursor.fetchone() or {'nama_motif': '-', 'jumlah': 0}

    # Rata-rata skor tertinggi
    cursor.execute(f"""
        SELECT nama_motif, AVG(skor_total) AS rata_rata
        FROM hasil_skoring
        WHERE upload_id IN ({placeholders})
        GROUP BY nama_motif
        ORDER BY rata_rata DESC
        LIMIT 1
    """, params)
    rata_rata_tertinggi = cursor.fetchone(
    ) or {'nama_motif': '-', 'rata_rata': 0}

    # Bar chart: top 5 skor tertinggi
    cursor.execute(f"""
        SELECT nama_motif, AVG(skor_total) AS skor_total
        FROM hasil_skoring
        WHERE upload_id IN ({placeholders})
        GROUP BY nama_motif
        ORDER BY skor_total DESC
        LIMIT 5
    """, params)
    chart_data = cursor.fetchall()
    for item in chart_data:
        item['skor_total'] = float(item['skor_total'] or 0)

    # Line chart: rata-rata skor per bulan
    cursor.execute(f"""
        SELECT MONTH(hu.waktu_upload) AS bulan, YEAR(hu.waktu_upload) AS tahun, AVG(hs.skor_total) AS rata_rata_skor
        FROM hasil_skoring hs
        JOIN hasil_upload hu ON hs.upload_id = hu.id
        WHERE hu.id IN ({placeholders})
        GROUP BY YEAR(hu.waktu_upload), MONTH(hu.waktu_upload)
        ORDER BY tahun, bulan
    """, params)
    penjualan_per_bulan = cursor.fetchall()

    # Pie chart: distribusi warna
    cursor.execute(f"""
        SELECT warna, COUNT(*) AS jumlah
        FROM hasil_skoring
        WHERE upload_id IN ({placeholders})
        GROUP BY warna
        ORDER BY jumlah DESC
    """, params)
    distribusi_warna = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html',
                           bulan_options=bulan_options,
                           selected_bulan=selected_bulan,
                           selected_tahun=selected_tahun,
                           total_upload=total_upload,
                           waktu_terakhir=waktu_terakhir,
                           motif_terbanyak=motif_terbanyak,
                           rata_rata_tertinggi=rata_rata_tertinggi,
                           chart_data=chart_data,
                           penjualan_per_bulan=penjualan_per_bulan,
                           distribusi_warna=distribusi_warna)


@dashboard_bp.route('/print/pdf', methods=['GET'])
def export_pdf():
    selected_bulan = request.args.get('bulan')
    selected_tahun = request.args.get('tahun')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fallback jika tidak ada data
    cursor.execute("""
        SELECT DISTINCT MONTH(waktu_upload) AS bulan, YEAR(waktu_upload) AS tahun
        FROM hasil_upload
        ORDER BY tahun DESC, bulan DESC
    """)
    bulan_options = cursor.fetchall()

    if not selected_bulan or not selected_tahun:
        if bulan_options:
            selected_bulan = str(bulan_options[0]['bulan'])
            selected_tahun = str(bulan_options[0]['tahun'])
        else:
            selected_bulan = '1'
            selected_tahun = '2023'

    # Ambil upload_id
    cursor.execute("""
        SELECT id AS upload_id FROM hasil_upload 
        WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
    """, (selected_bulan, selected_tahun))
    upload_ids = [row['upload_id'] for row in cursor.fetchall()]
    if not upload_ids:
        upload_ids = [0]

    placeholders = ','.join(['%s'] * len(upload_ids))
    params = tuple(upload_ids)

    # Total upload
    cursor.execute("""
        SELECT COUNT(*) AS total FROM hasil_upload 
        WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
    """, (selected_bulan, selected_tahun))
    total_upload = cursor.fetchone()['total'] or 0

    # Waktu upload terakhir
    cursor.execute("""
        SELECT MAX(waktu_upload) AS terakhir FROM hasil_upload 
        WHERE MONTH(waktu_upload) = %s AND YEAR(waktu_upload) = %s
    """, (selected_bulan, selected_tahun))
    waktu_terakhir = cursor.fetchone()['terakhir']

    # Motif terbanyak
    cursor.execute(f"""
        SELECT nama_motif, COUNT(*) AS jumlah 
        FROM hasil_skoring 
        WHERE upload_id IN ({placeholders}) 
        GROUP BY nama_motif 
        ORDER BY jumlah DESC LIMIT 1
    """, params)
    motif_terbanyak = cursor.fetchone() or {'nama_motif': '-', 'jumlah': 0}

    # Skor rata-rata tertinggi
    cursor.execute(f"""
        SELECT nama_motif, AVG(skor_total) AS rata_rata 
        FROM hasil_skoring 
        WHERE upload_id IN ({placeholders}) 
        GROUP BY nama_motif 
        ORDER BY rata_rata DESC LIMIT 1
    """, params)
    rata_rata_tertinggi = cursor.fetchone(
    ) or {'nama_motif': '-', 'rata_rata': 0}

    # Bar Chart (Top 5)
    cursor.execute(f"""
        SELECT nama_motif, AVG(skor_total) AS skor_total 
        FROM hasil_skoring 
        WHERE upload_id IN ({placeholders}) 
        GROUP BY nama_motif 
        ORDER BY skor_total DESC 
        LIMIT 5
    """, params)
    chart_data = cursor.fetchall()
    for item in chart_data:
        item['skor_total'] = float(item['skor_total'] or 0)

    # Line Chart (rata-rata skor per bulan)
    cursor.execute(f"""
        SELECT MONTH(hu.waktu_upload) AS bulan, YEAR(hu.waktu_upload) AS tahun, AVG(hs.skor_total) AS rata_rata_skor
        FROM hasil_skoring hs
        JOIN hasil_upload hu ON hs.upload_id = hu.id
        WHERE hu.id IN ({placeholders})
        GROUP BY YEAR(hu.waktu_upload), MONTH(hu.waktu_upload)
        ORDER BY tahun, bulan
    """, params)
    penjualan_per_bulan = cursor.fetchall()

    # Pie Chart (distribusi warna)
    cursor.execute(f"""
        SELECT warna, COUNT(*) AS jumlah
        FROM hasil_skoring
        WHERE upload_id IN ({placeholders})
        GROUP BY warna
        ORDER BY jumlah DESC
    """, params)
    distribusi_warna = cursor.fetchall()

    cursor.close()
    conn.close()

    html = render_template('dashboard_pdf.html',
                           total_upload=total_upload,
                           waktu_terakhir=waktu_terakhir,
                           motif_terbanyak=motif_terbanyak,
                           rata_rata_tertinggi=rata_rata_tertinggi,
                           chart_data=chart_data,
                           penjualan_per_bulan=penjualan_per_bulan,
                           distribusi_warna=distribusi_warna,
                           selected_bulan=int(selected_bulan),
                           selected_tahun=int(selected_tahun),
                           now=datetime.now())

    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    response = make_response(pdf_io.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=laporan_dashboard.pdf'
    return response
