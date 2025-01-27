from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from transformers import BertTokenizer

# Charger le modèle
model_path = "model_final2.h5"  # Assurez-vous que le modèle est dans le même répertoire
try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    raise HTTPException(status_code=500, detail="Model loading failed: " + str(e))

# Charger le tokenizer BERT
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

# Définir le schéma pour la requête d'API
class TextRequest(BaseModel):
    text: str

# Initialiser l'application FastAPI
app = FastAPI()

# Route de prédiction
@app.post("/predict/")
async def predict(request: TextRequest):
    try:
        # Prétraiter le texte (tokenisation avec BERT)
        inputs = bert_tokenizer(request.text, return_tensors="tf", padding='max_length', truncation=True, max_length=256)
        
        # Exécuter le modèle sur les données prétraitées
        predictions = model.predict(inputs['input_ids'])  # Utilisez les bonnes clés pour vos données d'entrée
        
        # Vérifiez la forme de la sortie
        if predictions.shape == (1, 1):  # Si la sortie est de forme (1, 1) (classification binaire)
            predicted_class = (predictions[0][0] > 0.5).astype(int)  # Si la probabilité est > 0.5, on prédit 1, sinon 0
            predicted_score = predictions[0][0]  # Score de la prédiction pour la classe 1 (probabilité)
        elif predictions.shape[1] > 1:  # Si c'est un modèle de classification multi-classes
            predicted_class = np.argmax(predictions, axis=1)[0]  # Obtenez la classe avec la plus grande probabilité
            predicted_score = np.max(predictions)  # La probabilité associée à la classe prédite
        else:
            raise HTTPException(status_code=500, detail="Unsupported output shape")
        
        # Retourner les prédictions
        return {"prediction": int(predicted_class), "score": float(predicted_score)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))