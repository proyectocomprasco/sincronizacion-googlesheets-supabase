from flask import Flask, jsonify
from supabase import create_client, Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, UTC
import uuid
import os

app = Flask(__name__)

SUPABASE_URL = "https://epevoikxjbfgnknhybye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwZXZvaWt4amJmZ25rbmh5YnllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA5MzY2ODQsImV4cCI6MjA3NjUxMjY4NH0.gKvE5FgwjFHudmwQYgJOH4aRGPU6H_ptiPLkuhQccXU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

GOOGLE_SHEETS_ID = "1xnEs-HfmHld4CNNoiqyDA1w6nT3G4njqEEtpP82FpRs"
SHEET_NAME = "Test de Compras Compulsivas (respuestas)"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Obtener la ruta absoluta del archivo
ruta_credenciales = os.path.join(os.path.dirname(__file__), "credenciales.json")
credentials = ServiceAccountCredentials.from_json_keyfile_name(ruta_credenciales, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(GOOGLE_SHEETS_ID).sheet1


def insertar_respuesta_supabase(respuesta):
    """
    Mapeo de columnas de Google Sheets a Supabase:
    - respuesta[0] = Marca temporal
    - respuesta[1] = Dirección de correo electrónico → email
    - respuesta[2] = ¿Qué carrera estas estudiando? → carrera
    - respuesta[3] = Semestre en el que estas → semestre
    - respuesta[4] = ¿Cuál es tu edad? → edad
    - respuesta[5] = ¿Cuál es tu genero? → genero
    - respuesta[6] = ¿Trabajas? → trabajas
    - respuesta[7] = Pregunta 1 (clóset) → closet
    - respuesta[8] = Pregunta 2 (conocidos) → conocidos
    - respuesta[9] = Pregunta 3 (vida_compra) → vida_compra
    - respuesta[10] = Pregunta 4 (innecesario) → innecesario
    - respuesta[11] = Pregunta 5 (no_planeado) → no_planeado
    - respuesta[12] = Pregunta 6 (compulsivo) → compulsivo
    - respuesta[13] = Pregunta 7 (ofertas) → ofertas
    - respuesta[14] = Pregunta 8 (ingresos) → ingresos
    - respuesta[15] = Pregunta 9 (deudas) → deudas
    - respuesta[16] = Pregunta 10 (tarjeta) → tarjeta
    """
    data = {
        "created_at": datetime.now(UTC).isoformat(),
        "email": respuesta[1],
        "carrera": respuesta[2],
        "semestre": respuesta[3],
        "edad": respuesta[4],
        "genero": respuesta[5],
        "trabajas": respuesta[6],
        "closet": respuesta[7],
        "conocidos": respuesta[8],
        "vida_compra": respuesta[9],
        "innecesario": respuesta[10],
        "no_planeado": respuesta[11],
        "compulsivo": respuesta[12],
        "ofertas": respuesta[13],
        "ingresos": respuesta[14],
        "deudas": respuesta[15],
        "tarjeta": respuesta[16],
    }
    response = supabase.table("respuestas_googleforms").insert(data).execute()
    return response.data


# ====== RUTAS ======

@app.route("/")
def index():
    return '''
    <html>
    <head>
        <title>API Sync Google Sheets - Supabase</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            h1 { color: #333; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            ul { list-style: none; padding: 0; }
            li { margin: 15px 0; }
            a { 
                display: inline-block;
                padding: 10px 20px;
                background: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }
            a:hover { background: #45a049; }
            .info { background: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔄 API de Sincronización</h1>
            <p>Sistema de sincronización de Google Sheets con Supabase</p>

            <h2>Rutas disponibles:</h2>
            <ul>
                <li><a href="/sync"> /sync</a> - Sincronizar datos de Google Sheets a Supabase</li>
                <li><a href="/test"> /test</a> - Verificar conexión</li>
                <li><a href="/status"> /status</a> - Ver estado del sistema</li>
                <li><a href="/ver-datos"> /ver-datos</a> - Ver estructura de datos de Google Sheets</li>
            </ul>

            <div class="info">
                <strong> Información:</strong><br>
                • Presiona "Sincronizar" para transferir datos de Google Forms a Supabase<br>
                • Los datos se almacenan en la tabla "respuestas_googleforms"<br>
                • Usa "/ver-datos" para verificar la estructura antes de sincronizar
            </div>
        </div>
    </body>
    </html>
    '''


@app.route("/test")
def test():
    return jsonify({
        "status": "ok",
        "mensaje": " Servidor Flask funcionando correctamente",
        "timestamp": datetime.now(UTC).isoformat()
    })


@app.route("/ver-datos")
def ver_datos():
    try:
        registros = sheet.get_all_values()
        encabezados = registros[0]
        primer_registro = registros[1] if len(registros) > 1 else []
        segundo_registro = registros[2] if len(registros) > 2 else []

        return jsonify({
            "encabezados_google_sheets": encabezados,
            "total_columnas": len(encabezados),
            "total_registros": len(registros) - 1,
            "ejemplo_primer_registro": primer_registro,
            "ejemplo_segundo_registro": segundo_registro,
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": str(e)
        }), 500


@app.route("/status")
def status():
    try:
        # Verificar conexión con Google Sheets
        total_rows = len(sheet.get_all_values()) - 1  # -1 para excluir encabezados

        # Verificar conexión con Supabase
        response = supabase.table("respuestas_googleforms").select("id", count="exact").execute()
        total_supabase = response.count if hasattr(response, 'count') else len(response.data)

        return jsonify({
            "status": "ok",
            "google_sheets": {
                "conectado": True,
                "total_respuestas": total_rows
            },
            "supabase": {
                "conectado": True,
                "total_registros": total_supabase
            },
            "timestamp": datetime.now(UTC).isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": str(e)
        }), 500


@app.route("/sync", methods=["GET"])
def sync_data():
    try:
        registros = sheet.get_all_values()
        encabezados = registros.pop(0)  # Quita los encabezados
        resultados = []
        errores = []

        for idx, fila in enumerate(registros, start=2):  # start=2 porque la fila 1 son encabezados
            try:
                # Saltar filas vacías
                if not any(fila):
                    print(f"  Fila {idx} está vacía, saltando...")
                    continue

                res = insertar_respuesta_supabase(fila)
                resultados.append(res)
                print(f" Fila {idx} insertada correctamente")
            except Exception as e:
                print(f" Error al insertar fila {idx}:", e)
                errores.append({"fila": idx, "error": str(e)})

        return jsonify({
            "mensaje": " Sincronización completada" if not errores else "⚠️ Sincronización completada con errores",
            "registros_insertados": len(resultados),
            "registros_con_error": len(errores),
            "detalles_errores": errores if errores else None
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": str(e)
        }), 500


# ====== INICIO DEL SERVIDOR ======

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print("=" * 50)
    print(f" Servidor iniciado en http://127.0.0.1:{port}")
    print(f" Panel principal: http://127.0.0.1:{port}/")
    print("=" * 50)
    app.run(debug=True, port=port, host='0.0.0.0')
