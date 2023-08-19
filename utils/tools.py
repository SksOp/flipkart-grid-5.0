from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from utils.data import load_matrix_from_local, convert_to_matrix, load_csv
import json
from langchain.tools import StructuredTool
import pandas as pd


def search_products(product_names: str) -> str:
    """
    Method to get the products as per user query
    a tool for
    :param product_names: comma(,) seperated names of products for ex shirt, pant
    :return: json response of products
    """

    product_names = product_names.split(",")
    no_of_product_response = 5
    final_result = []
    df = load_csv()
    tfidf_matrix, tfidf_vectorizer = load_matrix_from_local()

    for product in product_names:
        print(f'searching for {product}')
        query_vec = tfidf_vectorizer.transform([product.lower()])
        cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
        relevant_indices = cosine_similarities.argsort(
        )[-no_of_product_response:][::-1]

        results = df.iloc[relevant_indices].copy()
        results['similarity_score'] = cosine_similarities[relevant_indices]
        results = results[["product_name", "product_url", "image_link"]]
        results = results.to_dict(orient="records")
        final_result.append({product: results})

    return json.dumps(final_result)

# ayush -> write a tool to get trending products based on user preference


# def get_trending_products(user_preference: str) -> str:
#     """
#     Method to get the trending products as per user preference, give a trending product related to each product in user_preference,
#     assuming there is a trending score with respect to each product from 0 to 1 and we will rank the products found by crossing threshold of cosine similarity based on this score.
#     :param user_preference: e.g. '[{"product_name": "red shirt", "price": 500}, {"product_name": "blue jeans", "price": 5000}]'
#     :return: json response of product ids
#     """

#     user_preference = json.loads(f"[{user_preference}]")
#     cosine_similarity_threshold = 0.5
#     no_of_product_response = 5
#     final_result = []
#     df = load_csv()
#     tfidf_matrix, tfidf_vectorizer = load_matrix_from_local()

#     # Remove the ₹ symbol and convert the 'price' column to numeric
#     df['price'] = pd.to_numeric(
#         df['price'].str.replace('₹', ''), errors='coerce')

#     for product in user_preference:
#         print(f'searching for {product}')
#         query_vec = tfidf_vectorizer.transform(
#             [product["product_name"].lower()])
#         cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()

#         # Filter products based on cosine similarity threshold
#         relevant_indices = [i for i, score in enumerate(
#             cosine_similarities) if score >= cosine_similarity_threshold]

#         # Sort the filtered products based on their trending score (assuming the column name is 'trending_score')
#         results = df.iloc[relevant_indices].copy()
#         results['similarity_score'] = cosine_similarities[relevant_indices]

#         # Filter products based on price range
#         min_price = 0.25 * product["price"]
#         max_price = 3 * product["price"]
#         results = results[(results['price'] >= min_price) &
#                           (results['price'] <= max_price)]

#         results = results.sort_values(
#             by='trending_score', ascending=False).head(no_of_product_response)
#         results = results[["product_name", "product_url", "image_link"]]
#         results = results.to_dict(orient="records")
#         final_result.append({str(product): results})

#     return json.dumps(final_result)

def get_trending_products(user_preference: str) -> str:
    """
    Method to get the trending products as per user preference, give a trending product related to each product in user_preference,
    assuming there is a trending score with respect to each product from 0 to 1 and we will rank the products found by crossing threshold of cosine similarity based on this score.
    :param user_preference: e.g. '[{"product_name": "red shirt", "price": 500}, {"product_name": "blue jeans", "price": 5000}]'
    :return: json response of product ids
    """

    user_preference = json.loads(f"[{user_preference}]")
    no_of_product_response = 5
    final_result = []
    df = load_csv()
    tfidf_matrix, tfidf_vectorizer = load_matrix_from_local()

    # Remove the ₹ symbol and convert the 'price' column to numeric
    df['price'] = pd.to_numeric(
        df['price'].str.replace('₹', ''), errors='coerce')

    for product in user_preference:
        print(f'searching for {product}')
        query_vec = tfidf_vectorizer.transform(
            [product["product_name"].lower()])
        cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()

        # Get the top 30 most similar products based on cosine similarity
        relevant_indices = cosine_similarities.argsort()[-30:][::-1]

        # Sort the filtered products based on their trending score (assuming the column name is 'trending_score')
        results = df.iloc[relevant_indices].copy()
        results['similarity_score'] = cosine_similarities[relevant_indices]

        # Filter products based on price range
        min_price = 0.25 * product["price"]
        max_price = 3 * product["price"]
        results = results[(results['price'] >= min_price) &
                          (results['price'] <= max_price)]

        # Filter products based on the exact product type specified by the user
        product_type = product["product_name"].split()[-1].lower()
        results = results[results['product_name'].str.lower(
        ).str.contains(product_type)]

        results = results.sort_values(
            by='trending_score', ascending=False).head(no_of_product_response)
        results = results[["product_name", "product_url", "image_link"]]
        results = results.to_dict(orient="records")
        final_result.append({str(product): results})

    return json.dumps(final_result)


tools = [
    StructuredTool.from_function(search_products,
                                 description='''
        useful when you wants to search for any products based on user past and current history. 
        The input of this tool should be a  should be a comma separated list of product_names. 
        make sure to give full product name based on user past and current message do not just pass color or style name
        For example, 'blue shirt,jeans' would be the input if you wanted to seach blue shirt and jeans together  
        
        '''
                                 ),
    StructuredTool.from_function(get_trending_products,
                                 description='''
        Useful when you want to get trending products based on a user's preferences. 
        The input of this tool should be a JSON string representing a list of dictionaries, where each dictionary contains a product name and its price. 
        For example, '{"product_name": "red shirt", "price": 500}, {"product_name": "blue jeans", "price": 5000}' would be the input if you wanted to get trending products related to a red shirt and blue jeans. 
        This tool will return a list of products that have a cosine similarity score above a certain threshold (0.8) with the given products, and then it will rank the filtered products based on their trending score.
        
        '''
                                 )
]
