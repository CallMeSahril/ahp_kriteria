from db import get_connection

def get_all_kriteria():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kriteria")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def simpan_perbandingan(pairs):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM perbandingan_kriteria")  # hapus sebelumnya
    for item in pairs:
        cursor.execute("""
            INSERT INTO perbandingan_kriteria (kriteria_1_id, kriteria_2_id, nilai_perbandingan)
            VALUES (%s, %s, %s)
        """, (item['k1'], item['k2'], item['nilai']))
    conn.commit()
    cursor.close()
    conn.close()
