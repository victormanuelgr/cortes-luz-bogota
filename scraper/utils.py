import os

def ensure_data_folder():
    os.makedirs("data", exist_ok=True)