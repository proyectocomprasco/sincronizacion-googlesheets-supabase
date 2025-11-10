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

##  Autor

Janine Flores, Yostin Campoy

##  Licencia

Este proyecto es de uso educativo.