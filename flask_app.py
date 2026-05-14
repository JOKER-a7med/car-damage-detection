from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import traceback

app = Flask(__name__)

# ─── المسار الصحيح ──────────────────────────────────────────
MODEL_PATH = r'D:\car_damage_project\models\best_binary_model.keras'

print(f"🔄 جاري تحميل الموديل: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ الموديل تحمّل بنجاح!")

CLASS_NAMES = ['Minor Damage', 'Severe Damage']
CLASS_AR = ['ضرر بسيط (Minor)', 'ضرر جسيم (Severe)']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((224, 224))
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)

        prob = model.predict(arr, verbose=0)[0][0]   # احتمال Severe
        confidence = float(prob) * 100

        if prob > 0.5:
            label_idx = 1
        else:
            label_idx = 0

        return jsonify({
            'label': CLASS_NAMES[label_idx],
            'label_ar': CLASS_AR[label_idx],
            'confidence': round(confidence, 1),
            'is_severe': bool(prob > 0.5),
            'severity_prob': round(confidence, 1)
        })

    except Exception as e:
        print("❌ Error in predict:")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)