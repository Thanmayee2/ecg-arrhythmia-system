import gdown

MODEL_URL = "https://drive.google.com/uc?id=1kJtTW1CnUmOeR9i9IyY2MN5XJzGIL5IU"
ENCODER_URL = "https://drive.google.com/uc?id=1wN2dn6iveqxaoEiYjVnsrd6BvRqxoqVR"

print("Downloading model...")
gdown.download(MODEL_URL, "ecg_model.h5", quiet=False)

print("Downloading label encoder...")
gdown.download(ENCODER_URL, "label_encoder.pkl", quiet=False)

print("Download complete.")
