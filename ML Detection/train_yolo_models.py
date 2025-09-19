# -*- coding: utf-8 -*-
"""
Train_YOLO_Models.py
Clean version for training a YOLO model in Google Colab
"""

# --- Mount Google Drive (optional, if dataset stored in Drive) ---
from google.colab import drive
drive.mount('/content/gdrive')

# --- Copy dataset from Drive (replace with your path) ---
!cp /content/gdrive/MyDrive/path/to/data.zip /content

# --- Or download pre-made dataset (example candy dataset) ---
!wget -O /content/data.zip https://s3.us-west-1.amazonaws.com/evanjuras.com/resources/candy_data_06JAN25.zip

# --- Unzip dataset ---
!unzip -q /content/data.zip -d /content/custom_data

# --- Split dataset into train/validation ---
!wget -O /content/train_val_split.py https://raw.githubusercontent.com/EdjeElectronics/Train-and-Deploy-YOLO-Models/refs/heads/main/utils/train_val_split.py
!python train_val_split.py --datapath="/content/custom_data" --train_pct=0.9

# --- Install Ultralytics YOLO library ---
!pip install ultralytics

# --- Create data.yaml for YOLO training ---
import yaml
import os

def create_data_yaml(path_to_classes_txt, path_to_data_yaml):
    if not os.path.exists(path_to_classes_txt):
        print(f'classes.txt not found at {path_to_classes_txt}')
        return
    with open(path_to_classes_txt, 'r') as f:
        classes = [line.strip() for line in f if line.strip()]
    data = {
        'path': '/content/data',
        'train': 'train/images',
        'val': 'validation/images',
        'nc': len(classes),
        'names': classes
    }
    with open(path_to_data_yaml, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    print(f'Created config file at {path_to_data_yaml}')

path_to_classes_txt = '/content/custom_data/classes.txt'
path_to_data_yaml = '/content/data.yaml'
create_data_yaml(path_to_classes_txt, path_to_data_yaml)

# --- Train YOLO model ---
!yolo detect train data=/content/data.yaml model=yolo11s.pt epochs=60 imgsz=640

# --- Test model on validation images ---
!yolo detect predict model=runs/detect/train/weights/best.pt source=data/validation/images save=True

# --- Display first 10 prediction images ---
import glob
from IPython.display import Image, display

for image_path in glob.glob('/content/runs/detect/predict/*.jpg')[:10]:
    display(Image(filename=image_path, height=400))

# --- Save and zip trained model ---
!mkdir /content/my_model
!cp /content/runs/detect/train/weights/best.pt /content/my_model/my_model.pt
!cp -r /content/runs/detect/train /content/my_model
!zip -r /content/my_model.zip my_model

from google.colab import files
files.download('/content/my_model.zip')
