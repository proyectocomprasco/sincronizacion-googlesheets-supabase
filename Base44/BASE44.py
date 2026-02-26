from flask import Flask, jsonify
from supabase import create_client, Client
from datetime import datetime, UTC
import requests
import os

app = Flask(__name__)

# ========== SUPABASE ==========
SUPABASE_URL = "https://epevoikxjbfgnknhybye.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwZXZvaWt4amJmZ25rbmh5YnllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA5MzY2ODQsImV4cCI6MjA3NjUxMjY4NH0.gKvE5FgwjFHudmwQYgJOH4aRGPU6H_ptiPLkuhQccXU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# MISMA TABLA QUE USABAS CON GOOGLE FORMS
SUPABASE_TABLE = "respuestas_googleforms"

# ========== BASE44 ==========
BASE44_API_KEY = "fa3bd9bb67ef421abf1c9ba3a9875476"
BASE44_APP_ID = "6912cb13501ab401340fed29"
BASE44_ENTITY = "TestResult"
BASE44_BASE_URL = "https://app.base44.com/api"


def make_api_request(api_path, method="GET", data=None, params=None):
    url = f"{BASE44_BASE_URL}/{api_path}"
    headers = {
        "api_key": BASE44_API_KEY,
        "Content-Type": "application/json"
    }
    if method.upper() == "GET":
        response = requests.request(method, url, headers=headers, params=params or data)
    else:
        response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def obtener_respuestas_base44():
    """
    Trae las entidades TestResult desde Base44.
    """
    entities = make_api_request(
        f"apps/{BASE44_APP_ID}/entities/{BASE44_ENTITY}",
        method="GET"
    )

    # Normalizar a lista
    if isinstance(entities, list):
        return entities
    if isinstance(entities, dict):
        for key in ["items", "results", "data"]:
            if key in entities and isinstance(entities[key], list):
                return entities[key]
        # Si no hay una lista obvia, lo envolvemos
        return [entities]
    return []


def _get_answer_text(answers, index):
    """
    Extrae el answer_text de la pregunta en la posición 'index' (0-based).
    P1 = index 0, P2 = index 1, etc.
    """
    try:
        a = answers[index]
    except (IndexError, TypeError):
        return None

    if isinstance(a, dict):
        # Base44 usa 'answer_text' según el JSON que mandaste
        return a.get("answer_text") or str(a.get("answer"))
    return str(a)


def insertar_respuesta_supabase(entidad):
    """
    MISMO MAPEO que con Google Sheets, pero leyendo de Base44.

    personal_info:
        - carrera
        - edad
        - genero
        - semestre
        - trabaja   (¡OJO! esta es la que mapeamos a 'trabajas' en Supabase)

    answers (lista, en orden):
        0 -> closet
        1 -> conocidos
        2 -> vida_compra
        3 -> innecesario
        4 -> no_planeado
        5 -> compulsivo
        6 -> ofertas
        7 -> ingresos
        8 -> deudas
        9 -> tarjeta
    """
    personal_info = entidad.get("personal_info") or {}
    answers = entidad.get("answers") or []

    # Por ahora Base44 no está enviando email del usuario, así que quedará NULL
    email = (
        personal_info.get("email")
        or personal_info.get("correo")
        or personal_info.get("email_address")
    )

    data = {
        "created_at": datetime.now(UTC).isoformat(),
        "email": email,  # probablemente None por ahora
        "carrera": personal_info.get("carrera"),
        "semestre": personal_info.get("semestre"),
        "edad": personal_info.get("edad"),
        "genero": personal_info.get("genero"),
        "trabajas": personal_info.get("trabaja"),  # <- clave 'trabaja' en Base44

        "closet": _get_answer_text(answers, 0),
        "conocidos": _get_answer_text(answers, 1),
        "vida_compra": _get_answer_text(answers, 2),
        "innecesario": _get_answer_text(answers, 3),
        "no_planeado": _get_answer_text(answers, 4),
        "compulsivo": _get_answer_text(answers, 5),
        "ofertas": _get_answer_text(answers, 6),
        "ingresos": _get_answer_text(answers, 7),
        "deudas": _get_answer_text(answers, 8),
        "tarjeta": _get_answer_text(answers, 9),
    }

    print(" Insertando en Supabase:", data)  # DEBUG

    response = supabase.table(SUPABASE_TABLE).insert(data).execute()
    return response.data


# ====== RUTAS ======

@app.route("/")
def index():
    return '''
    <html>
    <head>
        <title>API Sync Base44 - Supabase</title>
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
            <h1>API de Sincronización</h1>
            <p>Sistema de sincronización de Base44 con Supabase</p>

            <h2>Rutas disponibles:</h2>
            <ul>
                <li><a href="/sync">/sync</a> - Sincronizar datos de Base44 a Supabase</li>
                <li><a href="/test">/test</a> - Verificar conexión</li>
                <li><a href="/status">/status</a> - Ver estado del sistema</li>
                <li><a href="/ver-datos">/ver-datos</a> - Ver estructura de datos de Base44</li>
            </ul>

            <div class="info">
                <strong> Información:</strong><br>
                • Presiona "Sincronizar" para transferir datos de Base44 a Supabase<br>
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
        "mensaje": "Servidor Flask funcionando correctamente",
        "timestamp": datetime.now(UTC).isoformat()
    })


@app.route("/ver-datos")
def ver_datos():
    try:
        entidades = obtener_respuestas_base44()
        primer_registro = entidades[0] if len(entidades) > 0 else {}
        segundo_registro = entidades[1] if len(entidades) > 1 else {}

        return jsonify({
            "total_registros_base44": len(entidades),
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
        # Base44
        try:
            entidades = obtener_respuestas_base44()
            total_base44 = len(entidades)
            base44_ok = True
        except Exception:
            base44_ok = False
            total_base44 = 0

        # Supabase
        response = supabase.table(SUPABASE_TABLE).select("id", count="exact").execute()
        total_supabase = response.count if hasattr(response, "count") else len(response.data)

        return jsonify({
            "status": "ok",
            "base44": {
                "conectado": base44_ok,
                "total_registros_base44": total_base44
            },
            "supabase": {
                "conectado": True,
                "total_registros_supabase": total_supabase
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
        entidades = obtener_respuestas_base44()
        resultados = []
        errores = []

        for idx, entidad in enumerate(entidades, start=1):
            try:
                res = insertar_respuesta_supabase(entidad)
                resultados.append(res)
                print(f" Entidad {idx} insertada correctamente")
            except Exception as e:
                print(f" Error al insertar entidad {idx}: {e}")
                errores.append({"entidad": idx, "error": str(e)})

        return jsonify({
            "mensaje": "Sincronización completada" if not errores else "⚠️ Sincronización completada con errores",
            "registros_insertados": len(resultados),
            "registros_con_error": len(errores),
            "detalles_errores": errores if errores else None
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "mensaje": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("=" * 50)
    print(f" Servidor iniciado en http://127.0.0.1:{port}")
    print(f" Panel principal: http://127.0.0.1:{port}/")
    print("=" * 50)
    app.run(debug=True, port=port, host="0.0.0.0")
