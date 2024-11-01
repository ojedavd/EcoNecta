from flask import Flask, request, jsonify
import pandas as pd
import joblib
from datetime import datetime

# Inicializa la aplicación Flask
app = Flask(__name__)

# Cargar los modelos previamente entrenados
modelo_humidity = joblib.load('models/modelo_humidity.pkl')
modelo_precip = joblib.load('models/modelo_precip.pkl')
modelo_sequia = joblib.load('models/modelo_sequia.pkl')

# Definir una ruta para realizar predicciones
@app.route('/predclim', methods=['POST'])
def predclim():
    try:
        # Obtiene los datos del request en formato JSON
        datos = request.get_json()

        # Extraer y procesar la fecha
        fecha = datos.get('fecha')  # Ejemplo de formato esperado: "2024-11-01"
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
        year = fecha_dt.year
        month = fecha_dt.month
        day = fecha_dt.day

        # Extraer otros datos
        temp_max = datos.get('temp_max')
        temp_min = datos.get('temp_min')
        humidity = datos.get('humidity')
        precip = datos.get('precip', 0)  # Puede que 'precip' no siempre esté presente

        # Crear un DataFrame con los datos
        X = pd.DataFrame([{
            'temp_max': temp_max,
            'temp_min': temp_min,
            'humidity': humidity,
            'precip': precip,
            'year': year,
            'month': month,
            'day': day
        }])

        # Realizar las predicciones
        pred_humedad = modelo_humidity.predict(X)[0]
        pred_precip = modelo_precip.predict(X)[0]
        pred_sequia = modelo_sequia.predict(X)[0]

        # Retorna las predicciones en formato JSON
        return jsonify({
            'pred_humedad': pred_humedad,
            'pred_precip': pred_precip,
            'pred_sequia': pred_sequia
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


modelo_cultivo = joblib.load('models/modelo_cultivo.pkl')

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