# Car Damage Detection

Binary classification of car damage: **Severe vs Minor**  
Two models compared: CNN from Scratch vs Transfer Learning (MobileNetV2)

---

## Results

| Model | Val Accuracy | F1 | AUC |
|---|---|---|---|
| CNN from Scratch | 63.6% | ~0.63 | — |
| Transfer Learning (MobileNetV2) | 96.7% | 0.97 | 1.00 |

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Jupyter Notebook
```bash
jupyter notebook notebooks/car_damage_project.ipynb
```

### 3. Run the Flask Web App
```bash
python flask_app.py
```
Then open your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

> **Note:** Update `MODEL_PATH` in `flask_app.py` to point to your local `best_binary_model.keras` before running.

---

## Project Structure

```
car-damage-detection/
├── notebooks/
│   └── car_damage_project.ipynb   # Main training notebook
├── models/
│   └── best_binary_model.keras    # Saved Transfer Learning model
├── results/
│   ├── confusion_matrix.png       # Confusion matrix heatmap
│   ├── roc_curve.png              # ROC curve (AUC = 1.00)
│   ├── training_curves_cnn.png    # CNN training history
│   └── training_curves_tl.png    # Transfer Learning training history
├── templates/
│   └── index.html                 # Flask frontend
├── data/
│   └── ...                        # Dataset (not tracked by Git)
├── flask_app.py                   # Flask web application
├── organize_data.py               # Data organization script
├── training_phase1.csv            # Phase 1 training logs
├── requirements.txt
└── README.md
```

---

## Dataset

- **Source:** [Kaggle — Car Damage Classification](https://www.kaggle.com/)
- **Size:** 1,000+ labeled images
- **Format:** Real images with JSON annotations (VIA tool)
- **Task:** Binary classification — Minor Damage vs Severe Damage
- **Split:** 70% Train / 15% Validation / 15% Test

---

## Models

### Model A — CNN from Scratch
Custom CNN built layer by layer:
- 3× Conv2D + ReLU + MaxPooling + BatchNormalization
- Flatten → Dense(256) → Dropout(0.5) → Sigmoid output
- ~2.1M trainable parameters | ~45 min training

### Model B — Transfer Learning (MobileNetV2)
Manually constructed transfer learning pipeline:
- MobileNetV2 backbone (ImageNet weights, no top)
- Custom head: GlobalAveragePooling2D → Dense(256) → Dropout(0.3) → Sigmoid
- **Phase 1:** Base frozen, only head trained
- **Phase 2:** Last 30 layers unfrozen, fine-tuned at lr = 1e-5
- ~3.4M trainable parameters | ~20 min training

---

## Deployment

Flask web app with a REST API endpoint:

| Component | Details |
|---|---|
| Framework | Flask (Python) |
| Endpoint | `POST /predict` |
| Input | Image file (multipart/form-data) |
| Output | JSON: `label`, `label_ar`, `confidence`, `is_severe` |
| Preprocessing | PIL resize 224×224 + normalize ÷ 255.0 |
