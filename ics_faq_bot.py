from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("API key not found in secrets. Please add OPENAI_API_KEY in Streamlit secrets for security.")
    st.stop()  # Halt execution if no key
llm = ChatOpenAI(api_key=api_key)
prompt = PromptTemplate.from_template("Based on this context: {context}\n\nQuestion: {question}\n\nAnswer in a fun, child-friendly way with a premium tone for an elite ICS Team member:")
chain = prompt | llm  # Chain prompt with LLM
