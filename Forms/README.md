#  API Sincronización Google Sheets - Supabase

Sistema de sincronización automática de respuestas de Google Forms hacia una base de datos Supabase.

##  Descripción

Este proyecto conecta Google Sheets (respuestas de Google Forms) con Supabase para almacenar y gestionar datos de encuestas sobre compras compulsivas.

## Características

- Sincronización automática de datos desde Google Sheets
- API REST con Flask
- Almacenamiento en Supabase
- Manejo de errores y validación de datos
- Panel de control web

##  Tecnologías

- Python 3.13
- Flask
- Google Sheets API
- Supabase
- gspread
- oauth2client

##  Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

2. Crear entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Mac/Linux
# .venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install flask supabase gspread oauth2client
```

4. Configurar credenciales:
   - Crear archivo `credenciales.json` con las credenciales de Google Service Account
   - Editar `conexion.py` con tu URL y API Key de Supabase

## Configuración

### Google Sheets API

1. Ve a Google Cloud Console
2. Crea un proyecto y habilita Google Sheets API
3. Crea una cuenta de servicio
4. Descarga el archivo JSON de credenciales
5. Comparte tu Google Sheet con el email de la cuenta de servicio

### Supabase

1. Crea un proyecto en Supabase
2. Crea la tabla `respuestas_googleforms` con las columnas necesarias
3. Copia tu URL y API Key

##  Uso

1. Iniciar el servidor:
```bash
python conexion.py
```

2. Acceder a: `http://127.0.0.1:5001/`

3. Rutas disponibles:
   - `/` - Panel principal
   - `/sync` - Sincronizar datos
   - `/status` - Ver estado del sistema
   - `/test` - Verificar conexión
   - `/ver-datos` - Ver estructura de datos

## Notas de Seguridad

- **NUNCA** subas el archivo `credenciales.json` a GitHub
- Usa variables de entorno para información sensible
- El archivo `.gitignore` protege tus credenciales


## Requerimientos del google shets
Solo lee 17 columnas y son  las siguientes: 
       
        "created_at":
        "email":
        "carrera": 
        "semestre":
        "edad":
        "genero":
        "trabajas": 
        "closet": 
        "conocidos": 
        "vida_compra": 
        "innecesario": 
        "no_planeado": 
        "compulsivo":
        "ofertas": 
        "ingresos": 
        "deudas":
        "tarjeta":
##  Autor

Janine Flores, Yostin Campoy

##  Licencia

Este proyecto es de uso educativo.


# Sincronizador Base44 → Supabase (Flask API)

Este proyecto implementa una API en Python + Flask que sincroniza automáticamente los resultados del test almacenados en Base44 hacia una tabla en Supabase, replicando el mismo mapeo que originalmente se usaba para integrar datos desde Google Forms.
El sistema fue diseñado para:
Leer entidades TestResult desde Base44.
Extraer datos del usuario (personal_info).
Mapear las respuestas del test (answers) a columnas específicas.
Insertar los datos en Supabase en la tabla respuestas_googleforms.
Proporcionar endpoints de prueba, diagnóstico y verificación.

# Características principales
✔ Integración directa con Base44
El sistema se conecta a la API de Base44 usando:
app_id
entity (TestResult)
api_key

✔ Inserción automática en Supabase
Los datos se insertan usando supabase-py, con claves:
SUPABASE_URL
SUPABASE_KEY
Tabla destino: respuestas_googleforms

✔ Mapeo idéntico a Google Forms
Aunque Base44 entrega la información en JSON estructurado, el código traduce todo al mismo formato que llegaba desde Google Sheets:
Base44	Supabase Column

personal_info.carrera	carrera

personal_info.semestre	semestre

personal_info.edad	edad

personal_info.genero	genero

personal_info.trabaja	trabajas

answers[0].answer_text	closet

answers[1].answer_text	conocidos
…	…
answers[9].answer_text	tarjeta

# Estructura del Proyecto
/BASE44.py        → Código principal Flask + Sync

/README.md        → Este archivo

/venv             → Entorno virtual (opcional)
# Requerimientos
Instalar dependencias:

pip install flask supabase requests

También necesitas:

Cuenta de Base44
API Key
APP ID
Nombre de la entidad (TestResult)
Proyecto en Supabase
Tabla respuestas_googleforms creada
 Estructura esperada en Base44

# Cómo ejecutar el servidor
Corre el script:

python BASE44.py

El servidor inicia en:

http://127.0.0.1:5001/
# Rutas disponibles (Endpoints)
GET /
Panel principal con enlaces a todas las rutas.

GET /ver-datos
Obtiene y muestra la estructura real de Base44 (primeros registros).
Sirve para depurar el mapeo.

GET /status
Muestra:
Conexión con Base44
Conexión con Supabase
Número de registros encontrados

GET /test
Verifica que el servidor Flask esté funcionando.

GET /sync
Sincroniza Base44 → Supabase

Acciones:
Consulta todas las entidades TestResult en Base44
Extrae personal_info
Extrae las respuestas answers
Construye el objeto con el mapeo exacto
Inserta cada registro en Supabase
Salida ejemplo:
{
  "mensaje": "Sincronización completada",
  "registros_insertados": 1,
  "registros_con_error": 0
}
# Mapeo completo implementado
"closet"        = answers[0].answer_text

"conocidos"     = answers[1].answer_text

"vida_compra"   = answers[2].answer_text

"innecessario"  = answers[3].answer_text

"no_planeado"   = answers[4].answer_text

"compulsivo"    = answers[5].answer_text

"ofertas"       = answers[6].answer_text

"ingresos"      = answers[7].answer_text

"deudas"        = answers[8].answer_text

"tarjeta"       = answers[9].answer_text


