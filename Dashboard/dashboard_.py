import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------
# Cargar CSV limpio
df = pd.read_csv("respuestas_limpias.csv")
st.title("Dashboard Compras Compulsivas")
st.write("Datos extraídos de la base de datos de Supabase.")

# ---------------------------
# FILTROS INTERACTIVOS
st.sidebar.header("Filtros")

# Multiselect con valor por defecto
carreras = df['carrera'].dropna().unique()
genero = df['genero'].dropna().unique()

carrera_seleccion = st.sidebar.multiselect("Selecciona carrera(s):", carreras, default=carreras)
genero_seleccion = st.sidebar.multiselect("Selecciona género(s):", genero, default=genero)

# Slider de edad con valor por defecto
edad_min = int(df['edad'].min())
edad_max = int(df['edad'].max())
edad_rango = st.sidebar.slider("Rango de edad:", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max))

# ---------------------------
# Aplicar filtros
df_filtrado = df[
    (df['carrera'].isin(carrera_seleccion)) &
    (df['genero'].isin(genero_seleccion)) &
    (df['edad'] >= edad_rango[0]) &
    (df['edad'] <= edad_rango[1])
]

st.write(f"Registros filtrados: {len(df_filtrado)}")

# ---------------------------
# KPIs generales
col1, col2, col3 = st.columns(3)
col1.metric("Total de encuestados", len(df_filtrado))
col2.metric("Edad promedio", round(df_filtrado['edad'].mean(), 1))
col3.metric("Promedio compras compulsivas", round(df_filtrado['compulsivo_num'].mean(), 2))

# ---------------------------
# Histograma de edades (discreto)
st.subheader("Distribución de edades")
age_count = df_filtrado['edad'].value_counts().sort_index().reset_index()
age_count.columns = ['edad','count']
age_chart = alt.Chart(age_count).mark_bar().encode(
    x='edad:O',
    y='count:Q'
)
st.altair_chart(age_chart, use_container_width=True)

# ---------------------------
# Boxplot de ingresos
st.subheader("Boxplot de ingresos")
fig, ax = plt.subplots()
sns.boxplot(y=df_filtrado['ingresos_num'], ax=ax)
ax.set_ylabel("Ingresos")
st.pyplot(fig)

# ---------------------------
# Pie chart de género
st.subheader("Distribución por género")
pie_data = df_filtrado['genero'].value_counts().reset_index()
pie_data.columns = ['genero','count']
pie_chart = alt.Chart(pie_data).mark_arc().encode(
    theta='count',
    color='genero',
    tooltip=['genero','count']
)
st.altair_chart(pie_chart, use_container_width=True)

# ---------------------------
# Scatter plot: ingresos vs compulsivo con jitter
st.subheader("Relación Ingresos vs Compras Compulsivas")
df_filtrado['compulsivo_jitter'] = df_filtrado['compulsivo_num'] + np.random.uniform(-0.2, 0.2, len(df_filtrado))
scatter = alt.Chart(df_filtrado).mark_circle(size=60).encode(
    x='ingresos_num',
    y='compulsivo_jitter',
    color='genero',
    tooltip=['email','ingresos_num','compulsivo_num','genero']
)
st.altair_chart(scatter, use_container_width=True)

# ---------------------------
# Histograma de compras compulsivas (discreto)
st.subheader("Histograma de compras compulsivas")
comp_count = df_filtrado['compulsivo_num'].value_counts().sort_index().reset_index()
comp_count.columns = ['compulsivo_num','count']
comp_chart = alt.Chart(comp_count).mark_bar().encode(
    x='compulsivo_num:O',
    y='count:Q'
)
st.altair_chart(comp_chart, use_container_width=True)