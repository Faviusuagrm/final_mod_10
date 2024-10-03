import streamlit as st
import os
import string
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

# Título de la aplicación
st.title('Modelo Word2Vec - NLP')

# Subida de archivos de texto
uploaded_files = st.file_uploader("Sube archivos de texto", accept_multiple_files=True, type=['txt'])

if uploaded_files:
    st.write(f"Has subido {len(uploaded_files)} archivo(s)")
    
    # Unir todo el texto de los archivos
    texto = ''
    for file in uploaded_files:
        texto += file.read().decode('utf-8')

    st.write(f"El texto tiene {len(texto)} caracteres")

    # Dividir en oraciones
    oraciones = texto.split('.')
    st.write(f"Número de oraciones: {len(oraciones)}")

    # Mostrar las primeras 10 oraciones
    st.subheader("Primeras 10 oraciones:")
    for i in range(10):
        st.text(oraciones[i])

    # Limpiar el texto y tokenizar las oraciones
    oraciones_limpias = []
    for oracion in oraciones:
        tokens = oracion.translate(str.maketrans('', '', string.punctuation)).split()
        tokens = [word.lower() for word in tokens if word.isalpha()]
        if tokens:
            oraciones_limpias.append(tokens)

    # Entrenar el modelo Word2Vec
    st.subheader("Entrenando modelo Word2Vec...")
    model = Word2Vec(sentences=oraciones_limpias, min_count=1, window=5, vector_size=100, workers=4)

    # Guardar el modelo
    model.save('word2vec_hielo_y_fuego.model')
    st.success("Modelo entrenado y guardado")

    # Mostrar vector de una palabra específica
    word = st.text_input("Ingresa una palabra para ver su vector:", "jon")
    if word in model.wv:
        vector = model.wv[word]
        st.write(f"Vector de la palabra '{word}':")
        st.write(vector)

    # Mostrar palabras más cercanas a una palabra
    similar_word = st.text_input("Ingresa una palabra para ver palabras similares:", "dracarys")
    if similar_word in model.wv:
        palabras_cercanas = model.wv.most_similar(similar_word, topn=5)
        st.write(f"Palabras cercanas a '{similar_word}':")
        for palabra, similitud in palabras_cercanas:
            st.write(f"{palabra}: {similitud}")

    # Mostrar analogía de palabras
    st.subheader("Analogía de palabras")
    a = st.text_input("Palabra A (ej: 'jon'):", "jon")
    b = st.text_input("Palabra B (ej: 'stark'):", "stark")
    c = st.text_input("Palabra C (ej: 'lannister'):", "lannister")

    if st.button("Calcular analogía"):
        try:
            resultado = model.wv.most_similar(positive=[a, c], negative=[b], topn=1)
            st.write(f"La analogía es: {resultado[0][0]}")
        except KeyError as e:
            st.error(f"Palabra no encontrada en el vocabulario: {e}")
