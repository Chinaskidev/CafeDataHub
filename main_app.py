import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objs as go
import plotly.express as px

# Cargar el modelo y los datos
with open('modelo_cafe.pkl', 'rb') as file:
    model = pickle.load(file)

coffe_export = pd.read_csv('data_cafe/Coffee_export.csv')
coffe_import = pd.read_csv('data_cafe/Coffee_import.csv')

# Los paises que mas exportan cafe: 
mayor_exportador = coffe_export[['Country', 'Total_export']].sort_values(by=['Total_export'], ascending=False).head(10)

# Los paises que mas importan cafe:  
mayor_importador = coffe_import[['Country', 'Total_import']].sort_values(by=['Total_import'], ascending=False).head(10)

# 15 mayores exportadores e importadores
top_exportadores = mayor_exportador.nlargest(15, 'Total_export').sort_values('Total_export', ascending=True)
top_importadores = mayor_importador.nlargest(15, 'Total_import').sort_values('Total_import', ascending=True)

# Función para crear el gráfico
def create_graph(value, n_clicks):
    # Alternar entre gráfico de barras y gráfico geográfico
    graph_type = 'bar' if n_clicks % 2 == 0 else 'geo'
    
    if value == 'export':
        df = top_exportadores
        title = 'Main exporters'
    else:
        df = top_importadores
        title = 'Main importers'
    
    if graph_type == 'bar':
        # Crear un gráfico de barras
        data = go.Bar(x=df['Total_export' if value == 'export' else 'Total_import'], 
                      y=df['Country'], orientation='h', marker_color='#5d2417')
        figure = go.Figure(data=data)
        figure.update_layout(title=title, xaxis_title='Total', yaxis_title='Country',
                             plot_bgcolor='#a77844')
    else:
        # Crear un gráfico geográfico (choropleth)
        figure = px.choropleth(df, locations='Country',
                       locationmode='country names',
                       color='Total_export' if value == 'export' else 'Total_import',
                       color_continuous_scale='Picnic',
                       title=title)
        figure.update_geos(projection_type="natural earth")
        figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                             plot_bgcolor='#a77844')

    return figure

# Selector de páginas
page = st.sidebar.selectbox('Elige una página', ['Predicciones', 'Gráficos'])

if page == 'Predicciones':
    # Página de predicciones
    st.image('img/cafe.jpg', caption='Cortadora de café', use_column_width=True)
    st.title('Predicción de exportación de café (En miles de sacos de 60 kg)')

    country = st.text_input('Introduce el nombre del país')

    if st.button('Predecir'):
        country_data = coffe_export[coffe_export['Country'] == country]
        country_data = country_data.drop(['Country', 'Total_export'], axis=1)
        prediction = model.predict(country_data)
        st.write(f'La predicción de exportación de café para {country} es {format(prediction[0], ",.2f")}')
    
elif page == 'Gráficos':
    # Página de gráficos
    st.title('Gráficos de exportadores e importadores de café')

    # Selector de opciones para elegir entre exportadores e importadores
    option = st.selectbox('Elige entre exportadores e importadores', ('export', 'import'))

    # Botón para cambiar entre gráfico de barras y gráfico geográfico
    if st.button('Cambiar visualización'):
        n_clicks = 1
    else:
        n_clicks = 0

    # Crear y mostrar el gráfico
    figure = create_graph(option, n_clicks)
    st.plotly_chart(figure)