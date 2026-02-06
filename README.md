# ECG Arrhythmia Detection & Monitoring System

## Project Overview
Cardiac arrhythmias affect millions of people worldwide, and many cases remain undiagnosed due to intermittent symptoms and limitations of traditional ECG monitoring systems. Early detection is critical to prevent severe complications such as stroke and heart failure.

This project implements an **AI-powered ECG Arrhythmia Detection and Continuous Monitoring System** capable of performing **real-time rhythm classification** using deep learning models and scalable web technologies.

The system supports ECG file uploads as well as real-time streaming, performs automated classification using trained neural networks, and displays results via an interactive web interface.

---

## Key Features
- Upload ECG signals for prediction
- Real-time ECG streaming using WebSockets
- AI-based arrhythmia classification
- Live ECG waveform visualization
- REST API-based prediction service
- Full-stack cloud deployment
- Scalable architecture for continuous monitoring

---

## Technology Stack

### Backend
- Python
- FastAPI
- TensorFlow / Keras
- NumPy & Pandas
- WebSockets for streaming
- Render for deployment

### Machine Learning
- 1D CNN + LSTM deep learning architecture
- ECG signal preprocessing and normalization
- Model trained on PTB-XL dataset subset

### Frontend
- React.js
- TypeScript
- Tailwind CSS
- Recharts for ECG visualization

### Deployment
- Backend hosted on Render
- Frontend hosted on Vercel


## Dataset Used
### PTB-XL ECG Dataset
A publicly available clinical ECG dataset containing more than **21,000 labeled ECG recordings**.

For this implementation:
- A subset of ECG recordings was used for faster training
- Binary classification was implemented (Normal vs Arrhythmia)

Dataset Source:
https://physionet.org/content/ptb-xl/

---

## System Architecture


## GET /health

Returns backend status.


## POST /predict

Upload ECG CSV file and receive prediction.





## Backend

cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Backend runs at(locally):

http://127.0.0.1:8000


## Frontend:

cd frontend
npm install
npm run dev

Frontend runs at(locally):

http://localhost:5173

Deployment URLs(Run backend and frontend once, to see the results)

## Frontend (Vercel):

https://ecg-arrhythmia-system-three.vercel.app


## Backend (Render):

https://ecg-arrhythmia-system-xe83.onrender.com


Deliverables and Implementation Details:

This project satisfies all required deliverables as described below.

. FastAPI Backend – ECG Signal Ingestion
The backend accepts ECG data through a REST API endpoint. Users upload ECG signals in CSV format through the frontend, which are then sent to the FastAPI server.

Implementation:
- Endpoint: `POST /predict`
- ECG CSV file is uploaded using `UploadFile`.
- Backend reads signal using Pandas.
- Signal is converted to NumPy array and preprocessed.
- Signals are padded or truncated to fixed model length before inference.

Thus, the system successfully ingests ECG data for processing.

2. Arrhythmia Classification API
The backend provides an API that performs arrhythmia classification using a trained deep learning model.

Implementation:
- TensorFlow/Keras trained model (`ecg_model.h5`) is loaded at server startup.
- Label encoder converts model output into rhythm labels.
- Prediction function processes ECG signal and returns:
  - Predicted rhythm class
  - Confidence score
  - Signal length used.

Example response:
```json
{
  "prediction": "NORM",
  "confidence": 0.92,
  "samples": 5000
}

3. Real-Time Inference Support

The system supports live ECG streaming and prediction using WebSockets.

Implementation:

Backend provides WebSocket endpoint: /ws/ecg.

Frontend streams ECG values in real time.

Backend predicts continuously and sends results back instantly.

Connection tested successfully on deployed backend using secure WebSocket (wss://).

This enables continuous monitoring instead of only static file upload.

4. React Frontend – ECG Upload and Visualization

A React-based frontend allows users to upload ECG files and visualize signals.

Implementation:

Built using React + TypeScript + Tailwind CSS.

CSV ECG files uploaded via file input.

Data sent to backend using FormData API.

ECG waveform displayed using Recharts line graph.

Streaming visualization supported using WebSocket data.

Thus, ECG signals can be both uploaded and visualized.


4. React Frontend – ECG Upload and Visualization

A React-based frontend allows users to upload ECG files and visualize signals.

Implementation:

Built using React + TypeScript + Tailwind CSS.

CSV ECG files uploaded via file input.

Data sent to backend using FormData API.

ECG waveform displayed using Recharts line graph.

Streaming visualization supported using WebSocket data.

Thus, ECG signals can be both uploaded and visualized.


6. Backend Deployment (Render)

Backend API is deployed publicly using Render.

Implementation:

FastAPI service hosted on Render.

REST endpoints and WebSocket accessible publicly.

Swagger API documentation accessible via /docs.

Deployed Backend:
https://ecg-arrhythmia-system-xe83.onrender.com


7. Frontend Deployment (Vercel)

Frontend web application is deployed using Vercel.

Implementation:

React app connected to deployed backend.

Automatic redeployment enabled via GitHub integration.

Public access allows real-time testing.

Deployed Frontend:
https://ecg-arrhythmia-system-three.vercel.app