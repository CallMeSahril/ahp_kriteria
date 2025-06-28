from db import get_connection


def hitung_bobot_kriteria():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil semua kriteria
    cursor.execute("SELECT * FROM kriteria")
    kriteria = cursor.fetchall()
    n = len(kriteria)
    id_map = {k['id_kriteria']: idx for idx, k in enumerate(kriteria)}

    # Inisialisasi matriks perbandingan
    matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    # Isi matriks dari tabel perbandingan_kriteria
    cursor.execute("SELECT * FROM perbandingan_kriteria")
    pairs = cursor.fetchall()
    for pair in pairs:
        i = id_map[pair['kriteria_1_id']]
        j = id_map[pair['kriteria_2_id']]
        nilai = float(pair['nilai_perbandingan'])
        matrix[i][j] = nilai
        matrix[j][i] = 1 / nilai

    # Normalisasi per kolom
    col_sums = [sum(matrix[i][j] for i in range(n)) for j in range(n)]
    norm_matrix = [[matrix[i][j] / col_sums[j]
                    for j in range(n)] for i in range(n)]

    # Hitung bobot: rata-rata tiap baris
    bobot = [round(sum(row) / n, 4) for row in norm_matrix]

    # Simpan bobot
    cursor.execute("DELETE FROM bobot_kriteria")
    for idx, b in enumerate(bobot):
        cursor.execute("INSERT INTO bobot_kriteria (id_kriteria, bobot) VALUES (%s, %s)",
                       (kriteria[idx]['id_kriteria'], b))

    conn.commit()
    cursor.close()
    conn.close()
    return list(zip([k['nama_kriteria'] for k in kriteria], bobot))


def uji_konsistensi():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil semua kriteria
    cursor.execute("SELECT * FROM kriteria")
    kriteria = cursor.fetchall()
    n = len(kriteria)
    id_map = {k['id_kriteria']: idx for idx, k in enumerate(kriteria)}

    # Ambil bobot
    cursor.execute("SELECT * FROM bobot_kriteria")
    bobot_rows = cursor.fetchall()
    bobot = [0] * n
    for row in bobot_rows:
        i = id_map[row['id_kriteria']]
        bobot[i] = float(row['bobot'])

    # Ambil pairwise matrix
    matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    cursor.execute("SELECT * FROM perbandingan_kriteria")
    pairs = cursor.fetchall()
    for pair in pairs:
        i = id_map[pair['kriteria_1_id']]
        j = id_map[pair['kriteria_2_id']]
        nilai = float(pair['nilai_perbandingan'])
        matrix[i][j] = nilai
        matrix[j][i] = 1 / nilai

    # Hitung A * w (perkalian matriks × bobot)
    Aw = [sum(matrix[i][j] * bobot[j] for j in range(n)) for i in range(n)]
    lambda_max = sum(Aw[i] / bobot[i] for i in range(n)) / n
    CI = (lambda_max - n) / (n - 1)

    # RI (Random Index)
    RI_TABLE = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24,
                7: 1.32, 8: 1.41, 9: 1.45}
    RI = RI_TABLE.get(n, 1.49)  # default max

    CR = CI / RI if RI != 0 else 0
    cursor.close()
    conn.close()
    return {
        'n': n,
        'lambda_max': round(lambda_max, 4),
        'CI': round(CI, 4),
        'CR': round(CR, 4),
        'status': 'Konsisten' if CR <= 0.1 else 'Tidak Konsisten'
    }
