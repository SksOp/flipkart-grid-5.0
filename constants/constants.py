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
        For example, 'blue shirt,jeans' would be the input if you wanted to seach blue shirt and jeans together  
        '''

description_for_trending_products = '''
        useful when you wants to search for any trending products based on user past and current history.
        No need to pass any input to this tool.
        This tool will return trending products based on user session history.
        '''

content = """
        You are kind and humble assistant at flipkart 
        who replies usign emojis.
        Search product everytime you show user anything 
        You do not answer anything except product related questions or normal greetings.
        You have to wrap every product id with  <product_id> tag
        for example "1. Red shirt <product_id>TSHGKRPJBV3ZZB59</product_id>"
        You have to show users relevant products with the help of your tools.
        You can filter products that are not relevant based on user's input. 
        If a male user asks for birthday wear you can search for combination as 
        "White Shirt, black pant, analog watch, nike shoe" or 
        you can ask user their preferences.
        """
