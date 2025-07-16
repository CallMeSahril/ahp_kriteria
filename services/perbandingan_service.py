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


def get_matrix_nilai():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM kriteria")
    kriteria = cursor.fetchall()

    matrix = {}
    for k1 in kriteria:
        matrix[k1['id_kriteria']] = {}
        for k2 in kriteria:
            matrix[k1['id_kriteria']][k2['id_kriteria']
                                      ] = 1.0 if k1['id_kriteria'] == k2['id_kriteria'] else None

    cursor.execute("SELECT * FROM perbandingan_kriteria")
    for row in cursor.fetchall():
        k1 = row['kriteria_1_id']
        k2 = row['kriteria_2_id']
        nilai = row['nilai_perbandingan']
        matrix[k1][k2] = nilai
        matrix[k2][k1] = round(1 / nilai, 4)

    cursor.close()
    conn.close()
    return kriteria, matrix
