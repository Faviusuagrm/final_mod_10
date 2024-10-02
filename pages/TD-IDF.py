import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la app
st.title("Análisis de Datos de Médicos por País")

# Subida de archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV con separador ';'
    df = pd.read_csv(uploaded_file, sep=',')
    
    # Mostrar los primeros registros del dataset
    st.write("Vista previa del archivo subido:")
    st.write(df.head())
    
    # Seleccionar país para análisis
    pais_seleccionado = st.selectbox("Selecciona un país para analizar:", df['Country'].unique())

    # Filtrar los datos por país seleccionado
    df_pais = df[df['Country'] == pais_seleccionado]

    # Mostrar datos del país seleccionado
    st.write(f"Datos de {pais_seleccionado}:")
    st.write(df_pais)

    # Graficar la evolución de médicos en el tiempo
    st.write(f"Evolución del número de médicos en {pais_seleccionado} a lo largo de los años")
    plt.plot(df_pais['Year'], df_pais['Medical doctors (number)'], label="Número de médicos")
    plt.xlabel("Año")
    plt.ylabel("Número de médicos")
    plt.title(f"Evolución de médicos en {pais_seleccionado}")
    plt.legend()
    st.pyplot(plt)

else:
    st.info("Por favor, sube un archivo CSV para continuar.")
