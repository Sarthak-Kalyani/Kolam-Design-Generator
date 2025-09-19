from ultralytics import YOLO
import glob
import os
import cv2

# Paths
model_path = "my_model.pt"
images_path = os.path.join("images", "*.jpg")

# Load model
model = YOLO(model_path)

# Output folder
output_project = os.path.join(os.getcwd(), "runs")
os.makedirs(output_project, exist_ok=True)

# Process each image
for img_path in glob.glob(images_path):
    print(f"Processing: {img_path}")
    
    # Predict (save annotated images and txt)
    results = model.predict(
        source=img_path,
        save=True,
        save_txt=True,
        project=output_project,
        name=os.path.splitext(os.path.basename(img_path))[0],  # unique folder per image
        show=False
    )
    
    # Display the image directly from the prediction
    for r in results:
        annotated_image = r.plot()  # returns image with boxes drawn
        cv2.imshow("Detection", annotated_image)
        cv2.waitKey(0)  # wait until a key is pressed
        cv2.destroyAllWindows()
