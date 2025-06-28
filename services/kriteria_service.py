from db import get_connection

def get_all_kriteria():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kriteria")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def add_kriteria(nama):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kriteria (nama_kriteria) VALUES (%s)", (nama,))
    conn.commit()
    cursor.close()
    conn.close()

def update_kriteria(id_kriteria, nama):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE kriteria SET nama_kriteria = %s WHERE id_kriteria = %s", (nama, id_kriteria))
    conn.commit()
    cursor.close()
    conn.close()

def delete_kriteria(id_kriteria):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kriteria WHERE id_kriteria = %s", (id_kriteria,))
    conn.commit()
    cursor.close()
    conn.close()
