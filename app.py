from flask import Flask
from routes.kriteria_route import kriteria_bp
from routes.alternatif_route import alternatif_bp
from routes.perbandingan_route import perbandingan_bp
from routes.perhitungan_route import perhitungan_bp
from routes.upload_route import upload_bp
from routes.riwayat_route import riwayat_bp
from routes.dashboard_route import dashboard_bp

from routes.auth_route import auth_bp

app = Flask(__name__)
app.secret_key = 'rahasia123'

app.register_blueprint(alternatif_bp)

app.register_blueprint(kriteria_bp)
app.register_blueprint(perbandingan_bp)
app.register_blueprint(perhitungan_bp)

app.register_blueprint(upload_bp)
app.register_blueprint(riwayat_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5020", debug=True)
