from app import db


class Kriteria(db.Model):
    id_kriteria = db.Column(db.Integer, primary_key=True)
    nama_kriteria = db.Column(db.String(100), nullable=False)
