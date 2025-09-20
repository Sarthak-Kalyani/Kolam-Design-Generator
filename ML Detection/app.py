from flask import Flask, request, jsonify
from ultralytics import YOLO
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO model
model = YOLO('my_model/my_model.pt')

# Define class names in the same order as your training
class_names = ["Kolam", "Rangoli"]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save uploaded image
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Run prediction and save annotated image
        results = model.predict(source=filepath, save=True)

        predictions = []
        for r in results:
            if hasattr(r, "boxes") and r.boxes is not None and len(r.boxes) > 0:
                xyxy_list = r.boxes.xyxy.tolist()
                conf_list = r.boxes.conf.tolist()
                cls_list = r.boxes.cls.tolist()
                for box, conf, cls in zip(xyxy_list, conf_list, cls_list):
                    predictions.append({
                        'bbox': [float(x) for x in box],
                        'confidence': float(conf),
                        'label': class_names[int(cls)]
                    })

        return jsonify({'predictions': predictions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
