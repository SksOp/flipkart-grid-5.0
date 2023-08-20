from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from utils.data import load_matrix_from_local, convert_to_matrix, load_csv
import json
from langchain.tools import StructuredTool
import pandas as pd
import streamlit as st
from constants.constants import description_for_search_products, description_for_trending_products, description_for_occasion_based_search
from utils.helper_model import get_dress_based_on_occasion


def clean_space(string: str):
    """
    Remove extra spaces from a string to reduce size
    """
    cleaned_string = ' '.join(string.split())
    return cleaned_string


def search_products(product_names: str) -> str:
    """
    Method to get the products as per user query
    a tool for
    :param product_names: comma(,) seperated names of products for ex shirt, pant
    :return: json response of products
    """
    print(product_names)
    product_names = product_names.split(",")
    no_of_product_response = 5
    final_result = []
    df = load_csv()
    tfidf_matrix, tfidf_vectorizer = convert_to_matrix()

    for product in product_names:
        print(f'searching for {product}')
        query_vec = tfidf_vectorizer.transform([product.lower()])
        cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
        relevant_indices = cosine_similarities.argsort(
        )[-no_of_product_response:][::-1]

        results = df.iloc[relevant_indices].copy()
        results['similarity_score'] = cosine_similarities[relevant_indices]
        results = results[["product_name", "product_id", "price"]]
        results = results.to_dict(orient="records")
        final_result.append({product: results})

    return json.dumps(final_result)


def get_trending_products() -> str:
    """
    Method to get the trending products as per user preference, 
    give a trending product related to each product in user_preference,
    assuming there is a trending score with respect to each product from 0 to 1 and 
    we will rank the products found by crossing threshold of cosine similarity based on this score.
    :param user_preference: e.g. '[{"product_name": "red shirt", "price": 500}, {"product_name": "blue jeans", "price": 5000}]'
    :return: json response of product ids
    """

    user_preference = st.session_state.entries
    print(user_preference)
    for item in user_preference:
        item['price'] = int(item['price'])

    no_of_product_response = 5
    final_result = []
    df = load_csv()
    tfidf_matrix, tfidf_vectorizer = convert_to_matrix()

    df['price'] = pd.to_numeric(
        df['price'].str.replace('₹', ''), errors='coerce')

    for product in user_preference:
        print(f'searching for {product}')
        query_vec = tfidf_vectorizer.transform(
            [product["product_name"].lower()])
        cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()

        # top 30 most similar products
        relevant_indices = cosine_similarities.argsort()[-10:][::-1]
        results = df.iloc[relevant_indices].copy()
        results['similarity_score'] = cosine_similarities[relevant_indices]

        min_price = 0.25 * product["price"]
        max_price = 3 * product["price"]
        results = results[(results['price'] >= min_price) &
                          (results['price'] <= max_price)]

        product_type = product["product_name"].split()[-1].lower()
        results = results[results['product_name'].str.lower(
        ).str.contains(product_type)]

        results = results.sort_values(
            by='trending_score', ascending=False).head(no_of_product_response)
        results = results[["product_name", "product_id", "price"]]
        results = results.to_dict(orient="records")
        final_result.append({product["product_name"]: results})
    print(final_result)
    return json.dumps(final_result)


tools = [
    StructuredTool.from_function(get_trending_products,
                                 name="trending_products",
                                 description=clean_space(
                                     description_for_trending_products)
                                 ),
    StructuredTool.from_function(search_products,
                                 name="search_product_tool",
                                 description=clean_space(
                                     description_for_search_products)
                                 ),
    StructuredTool.from_function(get_dress_based_on_occasion,
                                 name="occasion_based_search_tool",
                                 description=clean_space(
                                     description_for_occasion_based_search)
                                 ),

]
