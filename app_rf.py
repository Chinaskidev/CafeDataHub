# He creado esta API para predecir la exportación de café de un país en particular.
# La API toma el nombre del país como entrada y devuelve la predicción de exportación de café para ese país.
# La API utiliza un modelo de regresión aleatoria (Random Forest) , para hacer la predicción.
# El modelo y el conjunto de datos se cargan en la API y se utilizan para hacer la predicción.


from fastapi import FastAPI
import pickle
from pydantic import BaseModel
import pandas as pd

coffe_export = pd.read_csv('data_cafe/Coffee_export.csv')

with open('modelo_cafe.pkl', 'rb') as file:
    model = pickle.load(file)

app = FastAPI()

class InputData(BaseModel):
    country: str

@app.post('/predict')
def predict(input_data: InputData):
    country_data = coffe_export[coffe_export['Country'] == input_data.country]

    country_data = country_data.drop(['Country', 'Total_export'], axis=1)

    prediction = model.predict(country_data)

    # Convertir la predicción a una cadena con comas como separadores de miles
    prediction_str = format(prediction[0], ",.2f")

    return {'prediction': prediction_str}