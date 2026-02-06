from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import os

app = FastAPI(title="ECG Arrhythmia Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for production you can set your Vercel domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ecg_model.h5")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

model = tf.keras.models.load_model(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

SIGNAL_LEN = 5000

def predict_arrhythmia(ecg_signal: np.ndarray):
    ecg_signal = np.asarray(ecg_signal, dtype=np.float32)

    if len(ecg_signal) > SIGNAL_LEN:
        ecg_signal = ecg_signal[:SIGNAL_LEN]
    else:
        ecg_signal = np.pad(ecg_signal, (0, SIGNAL_LEN - len(ecg_signal)))

    ecg_signal = ecg_signal.reshape(1, SIGNAL_LEN, 1)

    pred = model.predict(ecg_signal, verbose=0)
    class_index = int(np.argmax(pred))
    confidence = float(np.max(pred))
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

    return {"prediction": prediction, "confidence": confidence, "samples": SIGNAL_LEN}


@app.websocket("/ws/ecg")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            # allow ping messages from frontend
            if data.strip().lower() in ["ping", ""]:
                await websocket.send_json({"type": "pong"})
                continue

            # parse comma-separated floats
            try:
                ecg_values = np.array([float(x) for x in data.split(",") if x.strip() != ""], dtype=np.float32)
                if ecg_values.size == 0:
                    await websocket.send_json({"error": "No ECG values received"})
                    continue
            except Exception:
                await websocket.send_json({"error": "Invalid ECG data format. Send comma-separated numbers."})
                continue

            prediction, confidence = predict_arrhythmia(ecg_values)

            await websocket.send_json({
                "prediction": prediction,
                "confidence": confidence,
                "samples": SIGNAL_LEN
            })

    except WebSocketDisconnect:
        # client disconnected normally
        return
    except Exception as e:
        # avoid crashing server if something unexpected happens
        try:
            await websocket.send_json({"error": f"Server error: {str(e)}"})
        except:
            pass
        return
