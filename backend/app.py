from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Inicializa la aplicación Flask
app = Flask(__name__)

# Cargar los modelos previamente entrenados
modelo_humidity = joblib.load('models/modelo_humidity.pkl')
modelo_precip = joblib.load('models/modelo_precip.pkl')
modelo_sequia = joblib.load('models/modelo_sequia.pkl')

# Definir una ruta para realizar predicciones
@app.route('/predict', methods=['POST'])
def predict():
    # Obtiene los datos del request en formato JSON
    datos = request.get_json()

    # Crea un DataFrame a partir de los datos recibidos
    df = pd.DataFrame([datos])

    # Selecciona las características necesarias
    X = df[['temp_max', 'temp_min', 'humidity', 'precip', 'year', 'month', 'day']]

    # Realiza las predicciones
    pred_humedad = modelo_humidity.predict(X)[0]
    pred_precip = modelo_precip.predict(X)[0]
    pred_sequia = modelo_sequia.predict(X)[0]

    # Retorna las predicciones en formato JSON
    return jsonify({
        'pred_humedad': pred_humedad,
        'pred_precip': pred_precip,
        'pred_sequia': pred_sequia
    })

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)
