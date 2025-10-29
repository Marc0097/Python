import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Dashboard de Scraping: 'Books to Scrape'")


@st.cache_data
def cargar_datos():
    df = pd.read_csv("libros.csv")
    df['precio'] = df['precio'].str.replace('£', '').astype(float)
    return df

df = cargar_datos()


st.sidebar.header("Filtros")

ratings_unicos = df['rating'].unique()
rating_seleccionado = st.sidebar.multiselect(
    "Filtrar por Rating (Estrellas):",
    options=ratings_unicos,
    default=ratings_unicos
)

precio_min = float(df['precio'].min())
precio_max = float(df['precio'].max())

rango_precio = st.sidebar.slider(
    "Filtrar por Rango de Precio (£):",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)

# ---  filtros ---
df_filtrado = df[
    (df['rating'].isin(rating_seleccionado)) &
    (df['precio'] >= rango_precio[0]) &
    (df['precio'] <= rango_precio[1])
]


st.subheader("Visualización de Datos")

col1, col2 = st.columns(2)
col1.metric("Libros Encontrados", df_filtrado.shape[0])
col2.metric("Precio Promedio", f"£{df_filtrado['precio'].mean():.2f}")

st.subheader("Distribución de Libros por Rating")
conteo_ratings = df_filtrado['rating'].value_counts()
st.bar_chart(conteo_ratings)

st.subheader("Datos Filtrados")
st.dataframe(df_filtrado)
