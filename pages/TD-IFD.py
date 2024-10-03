import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# importar las librerias para el PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler


#metodo para cargar los datos
@st.cache_data

def cargar_datos(archivo):
    if archivo:
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith('.xlsx'):
            df = pd.read_excel(archivo)
        else:
            raise ValueError('Formato no soportado. Solo se aceptan archivos .csv o .xlsx')
        return df
    else:
        return None

# agregar configuracion de cabezera
st.set_page_config(page_title='Trabajo Practico'
                   ,page_icon=':shark:'
                   ,layout='wide')

st.sidebar.subheader('Carga de datos')
archivo = st.sidebar.file_uploader('Seleccione un archivo', type=['csv', 'xlsx'])

# Solo cargar el carchivo si aun no existe df en st.session_state
if archivo and 'df' not in st.session_state:
    df = cargar_datos(archivo)
    st.session_state.df = df
    st.info('El archivo se ha cargado correctamente')
    st.write('El dataset tiene', df.shape[0], 'filas y', df.shape[1], 'columnas')
elif 'df' in st.session_state:
    df = st.session_state.df
else:
    st.warning('No se ha cargado ningun archivo')


opciones = ['Analisis Exploratorio',
            'TD-IDF']

# Seleccionar opcion
opcion = st.sidebar.radio('Selecciona una Opcion',opciones)

if opcion == 'Analisis Exploratorio':
    st.title('Analisis Exploratorio')

    #verificar si el archivo ya fue cargado
    if 'df' in st.session_state:
        df = st.session_state.df #Usamos el Datagrame almacenado en la sesion

        st.subheader('Dataframe cargado:')
        st.write(df)
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