import os
import numpy as np
import pandas as pd
import torch
import torchvision.transforms as transforms
from torchvision.models.resnet import ResNet50_Weights
from torchvision.models import resnet50
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import pickle


# Check for CUDA availability and set the device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pre-trained ResNet50 model
model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
model = model.to(device)
model.eval()

# Remove the final classification layer
model = torch.nn.Sequential(*(list(model.children())[:-1]))

# Define a preprocessing pipeline for the images
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# Load and process the image


def process_image(img_path):
    img = Image.open(img_path).convert('RGB')  # Convert image to RGB
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)
    return img_tensor.to(device)

# Extract features from the image


def extract_features(img_path):
    img_tensor = process_image(img_path)
    with torch.no_grad():
        features = model(img_tensor)
    return features.squeeze().cpu().numpy()

# Normalize the feature vector


def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


# Load or create the vector space
vector_space_path = "data/vector_space.pkl"
dataset_folder = "data/temp/dataset_images"
image_paths = [os.path.join(dataset_folder, img)
               for img in os.listdir(dataset_folder)]
if os.path.exists(vector_space_path):
    with open(vector_space_path, 'rb') as f:
        vector_space = pickle.load(f)
else:
    image_vectors = [normalize_vector(extract_features(img_path))
                     for img_path in image_paths]
    vector_space = np.vstack(image_vectors)
    with open(vector_space_path, 'wb') as f:
        pickle.dump(vector_space, f)

# Function to add new vectors to the vector space


def add_new_vector(img_path):
    new_vector = normalize_vector(extract_features(img_path))
    global vector_space
    vector_space = np.vstack((vector_space, new_vector))
    with open(vector_space_path, 'wb') as f:
        pickle.dump(vector_space, f)


# Load and process the query images in the "trending-images" folder
trending_folder = "data/temp/cropped"
trending_image_paths = [os.path.join(trending_folder, img)
                        for img in os.listdir(trending_folder)]
trending_vectors = [normalize_vector(extract_features(img_path))
                    for img_path in trending_image_paths]

# Load the dataset.csv file
df = pd.read_csv("data/dataset.csv")

# Check if the 'trending_score' column already exists
if 'trending_score' not in df.columns:
    df['trending_score'] = 0.0

# Update the trending score for each image in the dataset
for i, img_path in enumerate(image_paths):
    product_id = os.path.basename(img_path).split('.')[0]
    trending_score = 0.0
    # print(f"Processing product ID: {product_id}")
    for j, trending_vector in enumerate(trending_vectors):
        similarity_score = cosine_similarity(
            vector_space[i].reshape(1, -1), trending_vector.reshape(1, -1))[0][0]  # Extract the scalar value
        # print(f"Similarity score with trending image {j}: {similarity_score}")
        if similarity_score >= 0.9:
            print(f"Image {j} crosses the threshold!")
            trending_score += 1
            # Apply a logarithmic scale to the trending score
            trending_score_log = 1 - np.exp(-trending_score)
            if product_id in df['product_id'].values:
                df.loc[df['product_id'] == product_id,
                       'trending_score'] = trending_score_log
                print("Trending score updated", trending_score_log)
                # Save the updated dataset
                df.to_csv("dataset.csv", index=False)
            else:
                print(
                    f"Product ID {product_id} not found in the dataset.csv file.")

# Save the updated dataset
df.to_csv("dataset.csv", index=False)
