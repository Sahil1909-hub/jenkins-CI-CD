from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print('Model loading failed', e)
    raise

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try: 
        data = request.get_json()

        if not data or 'features' not in data:
            return jsonify({"error": "Invalid input"}), 400

        features = data['features']

        if len(features) != 30:
            return jsonify({"error": "Expected 30 features"}), 400

        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()

        return jsonify({
            "prediction": int(prediction),
            "probability": probability
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })
    

if __name__ == "__main__":
    print('App starting')
    app.run(host='0.0.0.0', port=5000)
