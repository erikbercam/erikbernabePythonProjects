import streamlit as st
import pandas as pd
import altair as alt  # Para los gráficos

# Configuración de la página
st.set_page_config(layout="wide")

st.title("Dashboard de Libros - Práctica de Scraping  scraping 📚")
st.write("Datos extraídos de 'books.toscrape.com'")


# 1. Cargar los datos con Pandas
# Usamos @st.cache_data para que Streamlit no recargue el CSV cada vez
@st.cache_data
def load_data(csv_file):
    try:
        df = pd.read_csv(csv_file)

        # --- Limpieza de Datos (esencial para los filtros) ---

        # Convertir precio (ej: '£51.77') a número (51.77)
        df['Price_Num'] = df['Price'].str.replace('£', '').astype(float)

        # Convertir rating (ej: 'Three') a número (3)
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        df['Rating_Num'] = df['Rating'].map(rating_map)

        return df
    except FileNotFoundError:
        return None


df = load_data('books.csv')

if df is None:
    st.error("Error: No se encontró el archivo 'books.csv'.")
    st.info("Por favor, ejecuta primero el script 'scrape.py' para generar los datos.")
else:
    # 2. Implementar filtros interactivos en la barra lateral

    st.sidebar.header("Filtros")

    # Filtro por Rango de Precios
    price_range = st.sidebar.slider(
        "Filtrar por rango de precios (£)",
        min_value=float(df['Price_Num'].min()),
        max_value=float(df['Price_Num'].max()),
        value=(float(df['Price_Num'].min()), float(df['Price_Num'].max()))  # Valor por defecto (todo)
    )

    # Filtro por categorías (Rating)
    rating_options = sorted(df['Rating'].unique())
    selected_ratings = st.sidebar.multiselect(
        "Filtrar por Rating (Estrellas)",
        options=rating_options,
        default=rating_options  # Valor por defecto (todos)
    )

    # Aplicar los filtros al DataFrame
    filtered_df = df[
        (df['Price_Num'] >= price_range[0]) &
        (df['Price_Num'] <= price_range[1]) &
        (df['Rating'].isin(selected_ratings))
        ]

    # 3. Visualizar los datos filtrados

    st.header(f"Mostrando {len(filtered_df)} de {len(df)} libros")

    # Tabla interactiva
    st.dataframe(filtered_df)

    # 4. Representación gráfica [cite: 53]

    st.header("Visualización de Datos")

    # Gráfico de barras para mostrar distribución de ratings [cite: 50]
    st.subheader("Distribución de Ratings en los libros filtrados")

    chart_data = filtered_df['Rating'].value_counts().reset_index()
    chart_data.columns = ['Rating', 'Count']

    bar_chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Rating', sort=None),  # 'sort=None' para respetar el orden de las estrellas
        y=alt.Y('Count', title='Número de Libros'),
        tooltip=['Rating', 'Count']
    ).interactive()

    st.altair_chart(bar_chart, use_container_width=True)