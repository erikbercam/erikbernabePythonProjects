import streamlit as st
import requests
import xml.etree.ElementTree as ET

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
NS = '{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}'

@st.cache_data(ttl=3600)
def load_data():
    try:
        response = requests.get(URL_BCE, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        time_node = root.find(f'{NS}Cube/{NS}Cube')

        data_date = time_node.get('time') if time_node is not None else "N/A"

        rates = {'EUR': 1.0}

        for node in root.findall(f'{NS}Cube/{NS}Cube/{NS}Cube'):
            rates[node.get('currency')] = float(node.get('rate'))

        return rates, data_date

    except Exception as e:
        st.error(f"Error al cargar datos: {e.__class__.__name__}. Fallo en conexion/parsing.")
        return None, "N/A"

st.set_page_config(page_title="Conversor BCE", layout="centered")
st.header("Conversor de Divisas BCE Erik Bernabe Camara")

rates, data_date = load_data()

if rates is None:
    st.stop()
else:
    st.success(f"Datos cargados. Fecha oficial: {data_date}")

monedas = sorted(list(rates.keys()))

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    cantidad = st.number_input("Cantidad a convertir", min_value=0.01, value=100.00, format="%.2f")
with col2:
    origen = st.selectbox("Moneda de Origen (DE)", options=monedas, index=monedas.index('EUR'))
with col3:
    destino = st.selectbox("Moneda de Destino (A)", options=monedas, index=monedas.index('USD'))

if st.button("Calcular Conversion", type="secondary"):

    if origen == destino:
        st.warning("Selecciona monedas de origen y destino diferentes.")
    elif cantidad <= 0.01:
        st.error("Introduce una cantidad positiva.")
    else:
        resultado = (cantidad / rates[origen]) * rates[destino]
        tasa_unit = (1.0 / rates[origen]) * rates[destino]

        st.subheader("Resultado Conversion:")

        st.metric(
            label=f"{cantidad:,.2f} {origen} es igual a:",
            value=f"{resultado:,.4f} {destino}"
        )
        st.caption(f"Tasa Usada (1 {origen}): {tasa_unit:,.4f} {destino}")