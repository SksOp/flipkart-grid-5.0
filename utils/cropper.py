from ultralytics import YOLO
import os
import shutil
from PIL import Image


def cropper():
    def rename_and_merge_images(root_folder, target_folder):
        image_number = 1
        
        for folder_name in os.listdir(root_folder):
            folder_path = os.path.join(root_folder, folder_name)
            
            if os.path.isdir(folder_path):
                for image_name in sorted(os.listdir(folder_path)):
                    if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):  # Check for image files
                        image_path = os.path.join(folder_path, image_name)
                        new_image_name = f"{image_number}.jpeg"
                        new_image_path = os.path.join(target_folder, new_image_name)
                        
                        # Copy and rename the image to the target folder
                        shutil.copy(image_path, new_image_path)
                        
                        image_number += 1

    model_path = "data/yolo8_fashion_weights.pt"
    input_folder = "data/temp/scrapped"
    model = YOLO(model_path)
    results = model(input_folder, save_crop=True) 
    print("Cropping and saving complete.")

    root_folder = "runs/detect/predict/crops"       # Replace with your root folder path
    target_folder = "data/temp/cropped"    # Replace with your target folder path
    os.makedirs(target_folder, exist_ok=True)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    rename_and_merge_images(root_folder, target_folder)
    if os.path.exists("data/temp/scrapped"):
        shutil.rmtree("data/temp/scrapped")
    if os.path.exists("runs"):
        shutil.rmtree("runs")
    print("Images cropped successfully.")
cropper()
