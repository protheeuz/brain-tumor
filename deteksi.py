import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from flask import jsonify
import pickle
import os

model_folder = 'models'

# Muat model yang udh dilatih
model = load_model(os.path.join(model_folder, 'model_tumor_otak.keras'))

with open(os.path.join(model_folder, 'class_labels.pkl'), 'rb') as f:
    class_labels = pickle.load(f)

def detect_image(img_path):
    try:
        img = load_img(img_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        pred = model.predict(img_array)
        predicted_class = np.argmax(pred, axis=1)[0]
        predicted_label = class_labels[predicted_class]
        confidence = float(pred[0][predicted_class])

        if predicted_label == 'notumor':
            result = {
                'prediction': "Normal",
                'tumor_type': "Tidak Tumor",
                'confidence': confidence
            }
        else:
            result = {
                'prediction': "Tumor",
                'tumor_type': predicted_label,
                'confidence': confidence
            }

        return result
    except Exception as e:
        return {'error': str(e)}, None