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

---

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


Frontend:

cd frontend
npm install
npm run dev

Frontend runs at(locally):

http://localhost:5173

Deployment URLs

Frontend (Vercel):

https://ecg-arrhythmia-system-three.vercel.app


Backend (Render):

https://ecg-arrhythmia-system-xe83.onrender.com