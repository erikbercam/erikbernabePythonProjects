import streamlit as st
import pandas as pd
import altair as alt

# Configuración de la página
st.set_page_config(layout="wide")

st.title("Dashboard de Libros - Scraping Erik Bernabe")
st.write("Datos de 'books.toscrape.com'")

@st.cache_data
def load_data(csv_file):
    try:
        df = pd.read_csv(csv_file)

        df['Price_Num'] = df['Price'].str.replace('£', '').astype(float)
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        df['Rating_Num'] = df['Rating'].map(rating_map)

        return df
    except FileNotFoundError:
        return None

df = load_data('books.csv')

if df is None:
    st.error("Error: No se encontro el archivo 'books.csv'.")
    st.info("Por favor, ejecuta primero el script 'scrape.py' para generar los datos.")
else:
    st.sidebar.header("Filtros")

    price_range = st.sidebar.slider(
        "Filtrar por rango de precios (£)",
        min_value=float(df['Price_Num'].min()),
        max_value=float(df['Price_Num'].max()),
        value=(float(df['Price_Num'].min()), float(df['Price_Num'].max()))
    )

    rating_options = sorted(df['Rating'].unique())
    selected_ratings = st.sidebar.multiselect(
        "Filtrar por Rating (Estrellas)",
        options=rating_options,
        default=rating_options
    )

    filtered_df = df[
        (df['Price_Num'] >= price_range[0]) &
        (df['Price_Num'] <= price_range[1]) &
        (df['Rating'].isin(selected_ratings))
        ]

    st.header(f"Mostrando {len(filtered_df)} de {len(df)} libros")

    st.dataframe(filtered_df)

    st.header("Visualización de Datos")

    st.subheader("Distribución de Ratings en los libros filtrados")

    chart_data = filtered_df['Rating'].value_counts().reset_index()
    chart_data.columns = ['Rating', 'Count']

    bar_chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Rating', sort=None),
        y=alt.Y('Count', title='Número de Libros'),
        tooltip=['Rating', 'Count']
    ).interactive()

    st.altair_chart(bar_chart, use_container_width=True)