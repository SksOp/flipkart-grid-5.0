
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentExecutor
from utils.model import agent,tools,memory,msgs


st_callback = StreamlitCallbackHandler(st.container())



agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    memory=memory,
    )

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.run(prompt, callbacks=[st_callback])
        st.write(response)

st.write(memory.load_memory_variables({}))

# if __name__ == "__main__":
#     main()