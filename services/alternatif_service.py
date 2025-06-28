from db import get_connection

def get_all_alternatif():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alternatif")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def add_alternatif(nama):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alternatif (nama_alternatif) VALUES (%s)", (nama,))
    conn.commit()
    cursor.close()
    conn.close()

def update_alternatif(id_alternatif, nama):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alternatif SET nama_alternatif = %s WHERE id_alternatif = %s", (nama, id_alternatif))
    conn.commit()
    cursor.close()
    conn.close()

def delete_alternatif(id_alternatif):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alternatif WHERE id_alternatif = %s", (id_alternatif,))
    conn.commit()
    cursor.close()
    conn.close()
def hitung_skoring_alternatif():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data alternatif & kriteria
    cursor.execute("SELECT * FROM alternatif")
    alternatif = cursor.fetchall()
    cursor.execute("SELECT * FROM kriteria")
    kriteria = cursor.fetchall()

    # Ambil bobot
    cursor.execute("SELECT * FROM bobot_kriteria")
    bobot_rows = cursor.fetchall()
    bobot_map = {row['id_kriteria']: float(row['bobot']) for row in bobot_rows}

    # Ambil nilai alternatif
    cursor.execute("SELECT * FROM nilai_alternatif")
    nilai_rows = cursor.fetchall()

    # Buat mapping nilai alternatif per kriteria
    nilai_map = {}
    for row in nilai_rows:
        alt_id = row['id_alternatif']
        kri_id = row['id_kriteria']
        nilai = float(row['nilai'])
        if alt_id not in nilai_map:
            nilai_map[alt_id] = {}
        nilai_map[alt_id][kri_id] = nilai

    # Hitung skor
    hasil = []
    for alt in alternatif:
        skor = 0
        for kri in kriteria:
            nilai = nilai_map.get(alt['id_alternatif'], {}).get(kri['id_kriteria'], 0)
            bobot = bobot_map.get(kri['id_kriteria'], 0)
            skor += nilai * bobot
        hasil.append({
            'nama_alternatif': alt['nama_alternatif'],
            'skor': round(skor, 4)
        })

    # Urutkan
    hasil.sort(key=lambda x: x['skor'], reverse=True)
    cursor.close()
    conn.close()
    return hasil
