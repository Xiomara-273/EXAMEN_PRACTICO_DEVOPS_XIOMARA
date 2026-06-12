from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# REQUERIMIENTO: Configuración estricta mediante variables de entorno
APP_NAME = os.getenv("APP_NAME", "Mi Aplicacion DevOps")
VERSION = os.getenv("APP_VERSION", "1.0.0")
DB_HOST = os.getenv("DB_HOST", "postgresdb-mendez")
DB_NAME = os.getenv("DB_NAME", "empresa")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")

def obtener_conexion():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def inicio():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        estado_conexion = f"✅ Conexión exitosa a PostgreSQL"
        detalle_db = f"Versión del motor: {db_version}"
        color_estado = "#00e676"  # Verde brillante
    except Exception as e:
        estado_conexion = f"❌ Error de conexión con la Base de Datos"
        detalle_db = f"Detalle: {str(e)}"
        color_estado = "#ff1744"  # Rojo brillante

    return f"""
    <html>
    <head>
        <title>{APP_NAME}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #1e1e24; /* Gris oscuro profesional */
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background-color: #2a2a35;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.3);
                border-left: 5px solid #00d2ff; /* Acento Azul Neón */
                max-width: 600px;
                width: 100%;
            }}
            h1 {{ color: #00d2ff; margin-top: 0; font-size: 2.2em; }}
            h2 {{ color: #aaaaaa; font-size: 1.2em; font-weight: 400; }}
            .version {{ color: #00d2ff; font-weight: bold; }}
            .status {{
                background-color: #202029;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #3a3a4a;
                margin-top: 20px;
            }}
            .badge {{ color: {color_estado}; font-size: 1.1em; font-weight: bold; }}
            .detalle {{ color: #888888; font-size: 0.9em; margin-top: 5px; }}
            a {{ color: #00d2ff; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 {APP_NAME}</h1>
            <h2>Versión del Sistema: <span class="version">{VERSION}</span></h2>
            <div class="status">
                <div class="badge">{estado_conexion}</div>
                <div class="detalle">{detalle_db}</div>
            </div>
            <p style="margin-top: 25px; font-size: 0.95em;">
                📂 Ver datos almacenados: <a href="/productos">/productos</a>
            </p>
        </div>
    </body>
    </html>
    """

@app.route("/productos")
def listar_productos():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, precio, stock FROM productos;")
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()

        lista_productos = []
        for f in filas:
            lista_productos.append({
                "id": f[0],
                "nombre": f[1],
                "precio": float(f[2]),
                "stock": f[3]
            })
        return jsonify({"status": "success", "productos": lista_productos})
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Asegúrate de haber creado la tabla 'productos' e insertado los 5 registros en la base de datos 'empresa' mediante pgAdmin.",
            "detalle_tecnico": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)