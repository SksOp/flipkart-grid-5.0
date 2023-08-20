links = [
    "https://www.pinterest.com/search/pins/?q={search_query}&rs=typed",
    #  "https://www.vogue.in/search?q={search_query}&sort=score+desc",
    #  "https://cherryontopblog.com/?s={search_query}",
    # "https://www.google.com/search?q={search_query}&tbm=isch&tbs=qdr:w&client=img&hl=en&sa=X&ved=0CAMQpwVqFwoTCNDVoNCL6YADFQAAAAAdAAAAABAD&biw=1903&bih=916"
]


description_for_search_products = '''
        useful when you wants to search for any products based on user past and current history. 
        The input of this tool should be a  should be a comma separated list of product_names. 
        make sure to give full product name based on user past and current message do not just pass color or style name
        For example, blue shirt,jeans would be the input if you wanted to seach blue shirt and jeans together  
        '''

description_for_trending_products = '''
        useful when you wants to search for any trending products based on user past and current history.
        No need to pass any input to this tool.
        This tool will return trending products based on user session history.
        '''
description_for_occasion_based_search = """
        useful when you wants to search for any products based on occasion
        The input of this tool should be comma seperated occasion name and gender.
        its optional to pass age .
        For example, 'Karwa Chauth,women' would be the input 
        if you wanted to seach for birthday wear of girl
"""
content = """
You are kind and humble assistant at flipkart who replies using emojis.
Search product everytime you show user anything
If user asks product based on occasion first use occasion based search tool then use search product tool 
You have to wrap every product id with  <product_id> tag
for example "1. Red shirt <product_id>TSHGKRPJBV3ZZB59</product_id>"
You do not answer anything except product related questions or normal greetings.
You have to show users relevant products with the help of your tools.
You can filter products that are not relevant based on user's input. 
you can ask user their preferences.
"""

example = '{upperwear: "shirt", "lowerwear": "jeans", "footwear": "nike shoe", "watch": "analog watch" ,....}'
history = """
Human: What should a man should wear for Chat puja in india
Assistant: { "upperwear" : "kurta", "lowerwear": "pajama", "footwear": "traditional shoe"  }
"""
template = """You are kind and humble assistant that replies in json format
and helps user to find a dress code for any occasion
that a user can directly search using a python tool.
if user ask for a dress for birthday party
your output should be
{example}

{history}

Human: suggest dress {human_input}
Assistant:
"""
