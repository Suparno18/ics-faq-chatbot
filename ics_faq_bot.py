import streamlit as st
import math
from collections import Counter
import numpy as np
import re
from datetime import datetime

# Excel data
excel_data = {
    # ... (same as previous, unchanged for brevity)
    # Insert full dictionary from prior message
}

# Handbook chunks
chunks = [
    # ... (same as previous, unchanged for brevity)
    # Insert full list from prior message
]

# Precompute TF-IDF
all_terms = set()
for chunk in chunks:
    terms = set(re.findall(r'\w+', (chunk['title'] + ' ' + chunk['content']).lower()))
    all_terms.update(terms)
term_to_id = {term: i for i, term in enumerate(all_terms)}
N = len(chunks)
idf = {term: math.log(N / sum(1 for chunk in chunks if term in Counter(re.findall(r'\w+', (chunk['title'] + ' ' + chunk['content']).lower())))) for term in all_terms}

def tfidf_vector(text):
    bow = Counter(re.findall(r'\w+', text.lower()))
    vec = np.zeros(len(all_terms))
    for term, count in bow.items():
        if term in term_to_id:
            tf = count / len(bow) if len(bow) > 0 else 0
            vec[term_to_id[term]] = tf * idf.get(term, 0)
    return vec

chunk_vectors = [tfidf_vector(chunk['title'] + ' ' + chunk['content']) for chunk in chunks]

def cosine_similarity(v1, v2):
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot / (norm1 * norm2) if norm1 and norm2 else 0.0

def retrieve_sections(query, top_k=3):
    query_vec = tfidf_vector(query)
    scores = [cosine_similarity(query_vec, chunk_vec) for chunk_vec in chunk_vectors]
    top_indices = np.argsort(scores)[::-1][:top_k]
    retrieved = ""
    for idx in top_indices:
        if scores[idx] > 0.1:
            retrieved += f"### {chunks[idx]['title']}\n{chunks[idx]['content']}\n\n"
    return retrieved if retrieved else "No matching handbook section found. Please refine your query or contact USHR@infinite.com."

def lookup_excel_data(query):
    for emp_id, data in excel_data.items():
        if (data["name"].lower() in query.lower() or 
            emp_id in query or 
            data["email"].lower() in query.lower()):
            latest_entry = max(data["entries"], key=lambda x: x["week_ending"])
            return (f"### Employee Profile: {data['name']}\n"
                    f"- Employee ID: {emp_id}\n"
                    f"- Role: {data['role']}\n"
                    f"- Manager: {data['manager']}\n"
                    f"- DOJ: {data['doj']} (Excel Date: {datetime.fromordinal(data['doj'] - 693594)})\n"
                    f"- Latest Entry (Week Ending {latest_entry['week_ending']}): "
                    f"{latest_entry['hours']} hours, {latest_entry['category']} on {datetime.fromordinal(latest_entry['date'] - 693594)}, "
                    f"Status: {latest_entry['status']}\n"
                    f"- Project: {data['project']}")
    return ""

# Streamlit UI with LangChain integration
st.title("ICS Team FAQs Elite Chatbot")
st.markdown("Welcome, distinguished ICS Team member! Your exclusive guide to Policies, Payroll, Timesheets, Benefits, and more awaits. Current time: 04:29 PM EDT, October 1, 2025. 🌟")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# LangChain Setup
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("API key not found in secrets. Please add OPENAI_API_KEY in Streamlit secrets for security.")
    st.stop()  # Halt execution if no key
llm = ChatOpenAI(api_key=api_key)
chain = RunnableSequence.from([
    PromptTemplate.from_template("Based on this context: {context}\n\nQuestion: {question}\n\nAnswer in a fun, child-friendly way with a premium tone for an elite ICS Team member:"),
    llm,
])

if prompt := st.chat_input("Pose your elite question (e.g., 'What is overtime?' or 'Sudarsana Sai Meruva status')"):
    user_name = prompt.split('@')[0] if '@' in prompt else "Valued Champion"
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enhanced retrieval with LangChain
    excel_response = lookup_excel_data(prompt)
    retrieved = retrieve_sections(prompt)
    context = (excel_response + "\n\n" + retrieved) if excel_response or retrieved else "No context available."
    response = chain.invoke({"context": context, "question": prompt}).content if context else "No response generated due to missing context."

    if not response:  # Fallback if LangChain fails
        response = f"Dear @{user_name},\n\nThank you for your prestigious inquiry. Here’s your tailored response:\n\n"
        if excel_response:
            response += excel_response + "\n\n"
        if retrieved:
            response += retrieved + "\n\n"
        else:
            response += "No direct match found in our elite archives. Please refine your question or consult USHR@infinite.com.\n\n"
        response += (f"Key Guidelines:\n"
                     f"- Submit timesheets by Monday 11 AM ET or Saturday EOD for Fieldglass (Oct 11 deadline).\n"
                     f"- Approval needed for OT, leave, or travel (Fiserv Manager, copy Infinite Manager).\n"
                     f"- Contact: USPayroll@infinite.com (payroll), USHR@infinite.com (benefits), ITSG-US@infinite.com (IT).\n\n"
                     f"Should this not suffice, share more details, and I’ll guide you further with care.\n\n"
                     f"Best Regards,\nSuparno Chowdhury | Project Manager\nInfinite | The PlatformizationTM Company\n"
                     f"Email: suparno.chowdhury@infinite.com | Cell: +1-470-404-0740")

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Premium Sidebar
st.sidebar.title("Elite Resources")
st.sidebar.markdown("- [Fieldglass](https://www.fieldglass.net/)\n- [BizX](https://bizx.infinite.com/)\n- [ADP Paystubs](https://workforcenow.adp.com)\n- [Support](mailto:suparno.chowdhury@infinite.com)")
st.sidebar.button("Reset Chat", on_click=lambda: st.session_state.update(messages=[]))

# Add flair
st.markdown("---")
st.markdown("**Your Journey Continues** - Explore, learn, and excel with Infinite! 🌈")
