from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import MessagesPlaceholder
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.prompts import MessagesPlaceholder
from utils.tools import tools, clean_space
from dotenv import load_dotenv
from constants.constants import content
load_dotenv()


# from utils.callbacks import call_me

system_message = SystemMessage(content=clean_space(content))

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="history")],
}

openAI = OpenAI(temperature=0)

llm = ChatOpenAI(temperature=0, streaming=False, model="gpt-3.5-turbo-0613")

prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message,
                                            extra_prompt_messages=[
                                                MessagesPlaceholder(variable_name="history")]
                                            )

# prompt = ChatPromptTemplate(
#     messages=[
#         SystemMessagePromptTemplate.from_template("""
#                                You are kind and humble assistant at flipkart.
#                                You show users relevant products with the help of your tools.
#                                You can filter products that are not relevant based on user's input as well as
#                                you can recommend user and search them using tools
#                                for eampleif a male user asks for birthday wear you can search
#                                for combination as "White Shirt, black pant, analog watch, nike shoe"
#                                """
#         ),
#         MessagesPlaceholder(variable_name="history"),
#         HumanMessagePromptTemplate.from_template("{question}")
#     ]
# )


agent = OpenAIFunctionsAgent(
    tools=tools,
    llm=llm,
    prompt=prompt,
    agent_kwargs=agent_kwargs,
)
