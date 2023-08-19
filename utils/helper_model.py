
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from constants.constants import template, example, history
from dotenv import dotenv_values

config = dotenv_values(".env")
api_key = config["OPENAI_API_KEY"]


def clean_space(string: str):
    """
    Remove extra spaces from a string to reduce size
    """
    cleaned_string = ' '.join(string.split())
    return cleaned_string


def get_dress_based_on_occasion(ocassion: str) -> str:
    helper_prompt = PromptTemplate(
        input_variables=["example", "history", "human_input"], template=clean_space(template))

    chat = ChatOpenAI(temperature=0,
                      openai_api_key=api_key,
                      streaming=True)
    helper_chain = LLMChain(
        llm=chat,
        prompt=helper_prompt,
        verbose=True,
        # memory=ConversationBufferWindowMemory(k=2),
    )

    output = helper_chain.predict(
        example=example,
        history=history,
        human_input=ocassion
    )
    return f"You should search for these dresses {output}"


get_dress_based_on_occasion("Goa trip dress")
