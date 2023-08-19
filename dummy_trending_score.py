# delete pkl file everytiem chainging csv
# add random trending score in dataset

import pandas as pd
import os
import random
from utils.tools import get_trending_products

csv_dataset_path = "data/dataset.csv"
pkl_file_path = "data/serialised_matrix_text.pkl"


def delete_serialised_matrix(pkl_file_path=pkl_file_path):
    if os.path.exists(pkl_file_path):
        os.remove(pkl_file_path)
        print(f"{pkl_file_path} has been deleted.")
    else:
        print(f"{pkl_file_path} does not exist.")


def add_trending_scores(path=csv_dataset_path):
    # Delete the serialised_matrix_text.pkl file
    delete_serialised_matrix()

    df = pd.read_csv(path)

    # Check if the 'trending_score' column already exists
    if 'trending_score' not in df.columns:
        df['trending_score'] = 0.0

    # Set random scores for each product
    df['trending_score'] = df['trending_score'].apply(
        lambda x: round(random.uniform(0, 1), 2))

    # Save the updated dataset
    df.to_csv(path, index=False)


x = get_trending_products(
    '{"product_name": "shirt", "price": 400}, {"product_name": "jeans", "price": 800}')

print(x)
