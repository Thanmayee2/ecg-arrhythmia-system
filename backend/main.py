from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import os

app = FastAPI(title="ECG Arrhythmia Detection API")

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model and label encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "ecg_model.h5")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

model = tf.keras.models.load_model(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

SIGNAL_LEN = 5000


# Real model prediction function
def predict_arrhythmia(ecg_signal: np.ndarray):
    # Fix ECG length (pad or truncate)
    if len(ecg_signal) > SIGNAL_LEN:
        ecg_signal = ecg_signal[:SIGNAL_LEN]
    else:
        ecg_signal = np.pad(ecg_signal, (0, SIGNAL_LEN - len(ecg_signal)))

    # Reshape for model (1, 1000, 1)
    ecg_signal = ecg_signal.reshape(1, SIGNAL_LEN, 1)

    # Predict
    pred = model.predict(ecg_signal, verbose=0)
    class_index = int(np.argmax(pred))
    confidence = float(np.max(pred))

    # Decode label
    prediction_label = label_encoder.inverse_transform([class_index])[0]

    return prediction_label, confidence


@app.get("/health")
def health_check():
    return {"status": "Backend running successfully"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    df = pd.read_csv(file.file, header=None)
    ecg_signal = df.iloc[:, 0].values

    prediction, confidence = predict_arrhythmia(ecg_signal)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "samples": SIGNAL_LEN
    }


@app.websocket("/ws/ecg")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        ecg_values = np.array(list(map(float, data.split(","))))

        prediction, confidence = predict_arrhythmia(ecg_values)

        await websocket.send_json({
            "prediction": prediction,
            "confidence": confidence,
            "samples": SIGNAL_LEN
        })
