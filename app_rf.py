from fastapi import FastAPI
import pickle
from pydantic import BaseModel

# Cargar el modelo
with open('modelo_cafe.pkl', 'rb') as file:
    model = pickle.load(file)

# Crear la aplicación FastAPI
app = FastAPI()

# Crear una clase para los datos de entrada
class InputData(BaseModel):
    feature1: float
    feature2: float

@app.post('/predict')
def predict(data: InputData):
    # Convertir los datos de entrada en un array 2D
    input_data = [[data.feature1, data.feature2]]  

    # Hacer una predicción con el modelo
    prediction = model.predict(input_data)

    # Devolver la predicción
    return {'prediction': prediction[0]}