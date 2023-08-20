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
    print(match.group(1))
    df = pd.read_csv(csv_dataset_path)
    df = df[["product_id", "product_url", "image_link", "product_name"]]
    links = df[df["product_id"] == product_id][[
        "image_link", "product_url", "product_name"]]
    try:
        links = links.iloc[0].to_dict()  # as they are available in list
    except Exception as e:
        print(product_id, e)
    # print(links)
    replacedText = ''

    replacedText += f'''
    <div style="margin-bottom: 10px;">
        <div style="margin-top: 5px;display:flex;flex-direction:column;align-items: flex-start;width:fit-content;gap:5px">
            <img src="{links["image_link"]}" alt="{links["product_name"]}" style="max-width: 100px;">
            <a href="{links["product_url"]}" style="color: white; text-decoration: none; background-color: blue; padding: 5px 20px; border-radius: 4px;">Buy Now</a>
        </div>
    </div>
    '''

    return replacedText


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

# we are not using this call back for now


class on_agent_finish(BaseCallbackHandler):
    def on_agent_finish(self, finish, **kwargs):
        finish.return_values["output"] = add_image_links_to_assistant_response(
            finish.return_values["output"])
