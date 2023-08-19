from typing import Dict, Union, Any, List

from langchain.callbacks.base import BaseCallbackHandler

import pandas as pd
import re

csv_dataset_path = "data/dataset.csv"


def replace_product_tags(match):
    """
    This function will be used to replace product tags in the response of assistant
    :param match: match of product id
    :return: replaced markdown text
    """
    product_id = match.group(1)
    df = pd.read_csv(csv_dataset_path)
    df = df[["product_id", "product_url", "image_link", "product_name"]]
    links = df[df["product_id"] == product_id][[
        "image_link", "product_url", "product_name"]]

    replacedText = ''
    for i, row in links.iterrows():
        replacedText += f'[Buy Now]({row["product_url"]}) ![{row["product_name"]}]({row["image_link"]})\n'

    return replacedText.strip()


def add_image_links_to_assistant_response(response: str) -> str:
    """
    Assinstant (in langchain agent) can only show text in streamlit.
    This function will add image links to the response of assistant
    from the string extract product id will be extracted from 
    <product_id> product id </product_id> and image link will be added
    :param response: response of assistant
    :return: response with image links
    """

    pattern = r"<product_id>(.*?)</product_id>"
    result = re.sub(pattern, replace_product_tags, response)
    return result


class on_agent_finish(BaseCallbackHandler):
    def on_agent_finish(self, finish, **kwargs):
        finish.return_values["output"] = add_image_links_to_assistant_response(
            finish.return_values["output"])
