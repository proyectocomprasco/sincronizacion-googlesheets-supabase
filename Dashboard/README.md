**El siguiente documento tiene la finalidad de informar al usuario sobre indicaciones de ejecucion e interpretacion del codigo**
## Dashboard Compras Compulsivas

Este proyecto es un dashboard interactivo creado con Streamlit para visualizar y analizar los datos de encuestas sobre hábitos de compras compulsivas. Los datos provienen de un CSV limpio extraído desde Supabase y mapeado para análisis numérico.

Requisitos

- Python 3.8 o superior

- Paquetes de Python:

- pandas

- streamlit

- altair

- seaborn

- matplotlib

- numpy

Se pueden instalar con:

**pip install pandas streamlit altair seaborn matplotlib numpy**

Cómo correr el dashboard

Coloca el archivo CSV limpio (respuestas_limpias.csv) en la misma carpeta que el script dashboard.py (o el nombre que le hayas dado).

Desde la terminal, navega a la carpeta del proyecto y ejecuta:

**streamlit run dashboard.py**


Esto abrirá automáticamente una ventana en tu navegador mostrando el dashboard interactivo.

Funcionalidades del dashboard
Filtros interactivos (sidebar)

Carrera: Permite seleccionar una o varias carreras para filtrar los datos.

Género: Permite seleccionar uno o varios géneros.

Rango de edad: Permite ajustar el rango de edades de los encuestados.

KPIs principales

Total de encuestados: Número de registros filtrados.

Edad promedio: Edad promedio de los encuestados según filtros.

Promedio compras compulsivas: Valor promedio de la columna compulsivo_num según filtros.

Gráficos

Histograma de edades: Muestra la distribución de edades de los encuestados.

Boxplot de ingresos: Representa la distribución de ingresos (ingresos_num).

Pie chart de género: Distribución de los encuestados por género.

Scatter plot Ingresos vs Compras Compulsivas: Relación entre ingresos y nivel de compras compulsivas, con colores por género.

Histograma de compras compulsivas: Distribución de los valores de la columna compulsivo_num.

Todos los gráficos se actualizan automáticamente al aplicar filtros en la barra lateral.

### Notas

El CSV debe estar limpio y con columnas correctamente nombradas: carrera, genero, edad, compulsivo_num, ingresos_num, entre otras.

Las columnas categóricas han sido mapeadas a valores numéricos para análisis estadístico.

Con pocos registros, algunos gráficos (como histogramas o scatter) pueden mostrar barras o puntos muy juntos debido a la baja variabilidad.
