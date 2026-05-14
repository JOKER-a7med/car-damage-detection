# Car Damage Detection

## Overview
Binary classification: Severe vs Minor car damage
Two models: CNN from scratch vs Transfer Learning (MobileNetV2)

## Results
| Model | Val Accuracy | F1 | AUC |
|---|---|---|---|
| CNN Scratch | 63.6% | ~0.63 | N/A |
| Transfer Learning | 96.7% | 0.97 | 1.00 |

## How to Run
1. Install: pip install -r requirements.txt
2. Open notebooks/car_damage_project.ipynb in Jupyter
3. Web app: py -3.11 -m streamlit run app.py

## Structure
- /models - saved Keras models
- /results - confusion matrix, ROC curve, training curves
- /notebooks - main project notebook
- app.py - Streamlit web application
"Updated README" 
