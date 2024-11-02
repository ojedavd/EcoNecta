from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# Inicializa la aplicación Flask
app = Flask(__name__)

# Cargar los modelos previamente entrenados
modelo_humidity = joblib.load('models/modelo_humidity_V2.pkl')
modelo_precip = joblib.load('models/modelo_precip_V2.pkl')
modelo_sequia = joblib.load('models/modelo_drought_V2.pkl')
modelo_cultivo = joblib.load('models/modelo_cultivo.pkl')
model_N = joblib.load('models/model_N.joblib')
model_P = joblib.load('models/model_P.joblib')
model_K = joblib.load('models/model_K.joblib')
model_pH = joblib.load('models/model_pH.joblib')


# Definir una ruta para realizar predicciones
@app.route('/predclim', methods=['POST'])
def predclim():
    try:
        # Obtiene los datos del request en formato JSON
        datos = request.get_json()

        # Extraer y procesar la fecha
        fecha = datos.get('fecha')  # Ejemplo de formato esperado: "2024-11-01"
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')

        # Extraer otros datos
        temp_max = datos.get('temp_max')
        temp_min = datos.get('temp_min')
        humidity = datos.get('humidity')
        precip = datos.get('precip', 0)  # Puede que 'precip' no siempre esté presente

        # Calcular temperatura promedio para el modelo
        temp = (temp_max + temp_min) / 2  # Promedio de temperatura máxima y mínima

        # Crear un DataFrame con los datos
        X = pd.DataFrame([{
            'temp': temp,
            'humidity': humidity,
            'precip': precip
        }])

        # Realizar las predicciones
        pred_humedad = modelo_humidity.predict(X)[0]
        pred_precip = modelo_precip.predict(X)[0]
        pred_sequia = modelo_sequia.predict(X)[0]  # Si decides predecir sequía

        # Retorna las predicciones en formato JSON
        return jsonify({
            'pred_humedad': pred_humedad,
            'pred_precip': pred_precip,
            'pred_sequia': pred_sequia
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


label_encoder = LabelEncoder()
label_encoder.classes_ = np.array(['Fresno', 'Los Angeles', 'Sacramento','San Diego','San Francisco'], dtype=object)  # Usar un array de NumPy explícitamente

# Ruta para hacer predicciones
@app.route('/predsuelo', methods=['POST'])
def predsuelo():
    try:
        # Obtener los datos enviados en el cuerpo de la solicitud
        data = request.get_json()
        ciudad = data['ciudad']
        fecha = data['fecha']

        # Validar que los datos de entrada no sean None
        if not ciudad or not fecha:
            return jsonify({"error": "Faltan datos: ciudad o fecha no proporcionados"}), 400

        # Codificar la ciudad
        ciudad_codificada = label_encoder.transform([ciudad])[0]  # Aquí no se necesita dtype

        # Convertir la fecha a día, mes y año
        fecha = pd.to_datetime(fecha)
        dia, mes, año = fecha.day, fecha.month, fecha.year

        # Preparar los datos de entrada para el modelo
        X_nueva = [[dia, mes, año, ciudad_codificada]]

        # Hacer las predicciones
        pred_N = model_N.predict(X_nueva)[0]
        pred_P = model_P.predict(X_nueva)[0]
        pred_K = model_K.predict(X_nueva)[0]
        pred_pH = model_pH.predict(X_nueva)[0]

        # Devolver las predicciones como JSON
        response = {
            "Nitrogen (N)": pred_N,
            "Phosphorus (P)": pred_P,
            "Potassium (K)": pred_K,
            "pH": pred_pH
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predcult', methods=['POST'])
def predcult():
    # Obtener los datos JSON del cuerpo de la solicitud
    data = request.get_json()

    # Verificar que los datos sean una lista de diccionarios
    if not isinstance(data, list):
        return jsonify({"error": "Los datos de entrada deben ser una lista de diccionarios."}), 400

    # Crear un DataFrame a partir de los datos de entrada
    df_prueba = pd.DataFrame(data)

    # Asegurarse de que el DataFrame tenga las columnas correctas
    required_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    if not all(col in df_prueba.columns for col in required_columns):
        return jsonify({"error": f"Faltan columnas necesarias: {required_columns}"}), 400

    # Realizar las predicciones
    simulacion_predicciones = modelo_cultivo.predict(df_prueba)
    probs = modelo_cultivo.predict_proba(df_prueba)

    # Crear un DataFrame para las probabilidades y los cultivos
    df_probs = pd.DataFrame(probs, columns=modelo_cultivo.classes_)

    # Preparar los resultados en formato adecuado para el frontend
    resultados = []
    for index, row in df_prueba.iterrows():
        # Obtener las probabilidades y cultivos para la fila actual
        prob_row = df_probs.iloc[index]
        top_n = prob_row.nlargest(10)  # Obtener las 10 mayores probabilidades

        for crop, prob in top_n.items():
            resultados.append({
                'Recommended Crop': crop,
                'N': row['N'],
                'P': row['P'],
                'K': row['K'],
                'Temperature': row['temperature'],
                'Humidity': row['humidity'],
                'pH': row['ph'],
                'Rainfall': row['rainfall'],
                'Probability': round(prob, 4)
            })

    # Devolver los resultados como respuesta JSON
    return jsonify(resultados)


# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)