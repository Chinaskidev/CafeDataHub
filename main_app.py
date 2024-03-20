import streamlit as st
import pandas as pd
import pickle



with open('modelo_cafe.pkl', 'rb') as file:
    model = pickle.load(file)

coffe_export = pd.read_csv('data_cafe/Coffee_export.csv')

st.image('img/cafe.jpg', caption='Cortadora de café', use_column_width=True)

st.title('Predicción de exportación de café')

country = st.text_input('Introduce el nombre del país')

if st.button('Predecir'):
    country_data = coffe_export[coffe_export['Country'] == country]
    country_data = country_data.drop(['Country', 'Total_export'], axis=1)
    prediction = model.predict(country_data)
    st.write(f'La predicción de exportación de café para {country} es {format(prediction[0], ",.2f")}')