import streamlit as st
import math
from collections import Counter
import numpy as np
import re
from datetime import datetime

# Excel data from "FIG - Bizx timesheet - Sep 2025-10-1-25.xlsx" and "FIG400_Issue and Query Log - 9-30-25.xlsx"
excel_data = {
    "20113324": {
        "name": "Sudarsana Sai Meruva",
        "email": "Sudarsana.Meruva@infinite.com",
        "doj": 44461,  # Jan 1, 2021
        "role": "Project Manager",
        "manager": "MANAS RANJAN SAHU",
        "client": "Fiserv Solutions, LLC",
        "project": "FIG Operations and Implementations",
        "entries": [
            {"date": 45901, "hours": 8, "category": "Holiday", "status": "Approved", "week_ending": 45905},
            {"date": 45901, "hours": 0, "category": "Worked", "status": "Approved", "week_ending": 45905},
            {"date": 45902, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905},
            {"date": 45902, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905},
            {"date": 45903, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905},
            {"date": 45903, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905},
            {"date": 45904, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905},
            {"date": 45904, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905},
            {"date": 45905, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905}
        ]
    },
    "20120551": {
        "name": "Victor Njoh Anjeh",
        "email": "Victor.Anjeh@infinite.com",
        "doj": 45912,  # Oct 10, 2025
        "role": "Program Manager",
        "manager": "MANAS RANJAN SAHU",
        "client": "Fiserv Solutions, LLC",
        "project": "FIG Operations and Implementations",
        "entries": [
            {"date": 45929, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45930, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933}
        ]
    },
    "20120567": {
        "name": "Nicette Garcias",
        "email": "Nicette.Garcias@infinite.com",
        "doj": 45917,  # Oct 15, 2025
        "role": "Client Tech Support Engineering - Professional II",
        "manager": "Sudarsana Sai Meruva",
        "client": "Fiserv Solutions, LLC",
        "project": "FIG Operations and Implementations",
        "entries": [
            {"date": 45931, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45932, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45933, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45927, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45928, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45929, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
            {"date": 45930, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933}
        ]
    },
    "10009236": {
        "name": "Matthew Wilcox",
        "email": "matthew.wilcox@fiserv.com",
        "doj": 38475,  # Jan 1, 2005
        "role": "Computer Operations",
        "manager": "Catherine Dombroski",
        "client": "Fiserv Solutions, LLC",
        "project": "SOW Roster",
        "entries": [{"date": 45901, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905}]
    },
    "10184692": {
        "name": "Justin Jackson",
        "email": "justin.jackson@fiserv.com",
        "doj": 39569,  # Jan 1, 2008
        "role": "Computer Operations",
        "manager": "Catherine Dombroski",
        "client": "Fiserv Solutions, LLC",
        "project": "SOW Roster",
        "entries": [{"date": 45902, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905}]
    },
    "10001321": {
        "name": "Raellen Rivard",
        "email": "raellen.rivard@fiserv.com",
        "doj": 40178,  # Jan 1, 2010
        "role": "Computer Operations",
        "manager": "Catherine Dombroski",
        "client": "Fiserv Solutions, LLC",
        "project": "SOW Roster",
        "entries": [{"date": 45903, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905}]
    },
    "10001322": {
        "name": "Ashka Zaveri",
        "email": "ashka.zaveri@fiserv.com",
        "doj": 40792,  # Jan 1, 2012
        "role": "Computer Operations",
        "manager": "Catherine Dombroski",
        "client": "Fiserv Solutions, LLC",
        "project": "SOW Roster",
        "entries": [{"date": 45904, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905}]
    }
    # Expand with all IDs as needed
}

# Handbook and email content split into granular chunks
chunks = [
    {
        "title": "ICS Team – FAQs Handbook 2025 Cover",
        "content": "Your colourful, engaging guide to Policies, Payroll, Timesheets, Benefits & More"
    },
    {
        "title": "Table of Contents",
        "content": "- 1. Overtime & Special Hours\n- 2. Timesheet / Payroll\n- 3. Leave & Time-Off\n- 4. Benefits\n- 5. Miscellaneous / IT Support"
    },
    {
        "title": "1. Overtime & Special Hours - Process for Overtime Hours Submission",
        "content": "Overtime payment is only for Salaried Non-Exempt Employees. Salaried Exempt Employees can submit >40 hours in BizX but aren’t eligible. Non-Exempt (Hourly) submit 40 hours + OT in BizX with Fiserv Manager email approval. Wait if manager is unavailable. OT >40 hours is auto-detected by payroll."
    },
    {
        "title": "1. Overtime & Special Hours - Process to Claim OT/Shift Differential/Bug Bash/On-Call Hours",
        "content": "Table: OT Hours (Non-Exempt: BizX with approval, USPayroll processes), Shift Differential (BizX, USPayroll processes), Bug Bash/On-Call (Not Applicable for Non-Exempt, Exempt in progress—get approval, notify Infinite Manager)."
    },
    {
        "title": "2. Timesheet / Payroll - How to Access Infinite Timesheet",
        "content": "Use BizX[](https://bizx.infinite.com) with Chrome/Edge/IE. Navigate to Timesheet > My Timesheet."
    },
    {
        "title": "2. Timesheet / Payroll - To Add Non-Work Hours",
        "content": "Add rows in BizX for vacation, sick, personal, jury duty, bereavement, break time, or holiday."
    },
    {
        "title": "2. Timesheet / Payroll - Submission Deadline",
        "content": "Submit by Monday 11 AM ET. Check ITSG emails if BizX is down."
    },
    {
        "title": "2. Timesheet / Payroll - Locked Timesheet",
        "content": "Locked post-Monday 11 AM ET after payroll cutoff. Unlock via uspayroll@infinite.com or submit manual (avoid if possible)."
    },
    {
        "title": "2. Timesheet / Payroll - Missed Timesheet",
        "content": "Email uspayroll@infinite.com to unlock, submit retroactively next cycle."
    },
    {
        "title": "2. Timesheet / Payroll - Time-Off Without Balance",
        "content": "Request Fiserv Manager approval, notify Infinite Manager. Unpaid if no balance."
    },
    {
        "title": "2. Timesheet / Payroll - Future Dates",
        "content": "No future entries. Submit current week’s worked hours; vacation from anywhere."
    },
    {
        "title": "2. Timesheet / Payroll - Jury Duty Policy",
        "content": "Inform Fiserv & Infinite Managers, get approval, send summons to USHR@infinite.com. Salaried get 2 weeks base pay; hourly unpaid unless mandated."
    },
    {
        "title": "2. Timesheet / Payroll - Paystubs and W-2s",
        "content": "Access at https://workforcenow.adp.com. Issues to USPayroll@infinite.com."
    },
    {
        "title": "2. Timesheet / Payroll - Time-Off Balance",
        "content": "View on latest pay statement."
    },
    {
        "title": "2. Timesheet / Payroll - ADP Time-Off Request",
        "content": "Not applicable; use email approval."
    },
    {
        "title": "3. Leave & Time-Off - Request Process",
        "content": "Email Fiserv Manager (copy Infinite Manager) for approval."
    },
    {
        "title": "3. Leave & Time-Off - Pre-Approved Time-Off",
        "content": "Pre-join approval (Salaried only) logged as worked hours in BizX."
    },
    {
        "title": "3. Leave & Time-Off - Post-Join Time-Off",
        "content": "Log as non-worked hours in BizX."
    },
    {
        "title": "3. Leave & Time-Off - Unlimited PTO Distribution",
        "content": "30 days (200 vacay + 40 sick hours) for ex-Fiserv unlimited PTO, rolls to 2026; no 2025 accruals."
    },
    {
        "title": "3. Leave & Time-Off - Non-Unlimited PTO",
        "content": "Accruals start with Infinite’s first paycheck."
    },
    {
        "title": "3. Leave & Time-Off - Vacation Carry-Over",
        "content": "80 hours max carry over; sick hours lapse (except 240-hour 2026 roll)."
    },
    {
        "title": "3. Leave & Time-Off - Applicable Holidays",
        "content": "Follow Fiserv holidays."
    },
    {
        "title": "3. Leave & Time-Off - Accrual Rates",
        "content": "Salaried: 6.15 hrs vacay, 2.31 hrs sick; Hourly: 3.08 hrs vacay, 1.15 hrs sick per paycheck."
    },
    {
        "title": "4. Benefits - Questions",
        "content": "Refer to onboarding documentation; contact USHR@infinite.com."
    },
    {
        "title": "5. Miscellaneous / IT Support - Email Access",
        "content": "Use https://outlook.office.com with BizX credentials; clear cache or use incognito."
    },
    {
        "title": "5. Miscellaneous / IT Support - Support Groups",
        "content": "BizX: BizX-Support@infinite.com, Payroll: USPayroll@infinite.com, Benefits: USHR@infinite.com, IT: ITSG-US@infinite.com (copy manager)."
    },
    {
        "title": "5. Miscellaneous / IT Support - Password Reset",
        "content": "Reset every 90 days at https://passwordreset.microsoftonline.com."
    },
    {
        "title": "5. Miscellaneous / IT Support - Location Change",
        "content": "No remote location changes without USHR approval."
    },
    {
        "title": "5. Miscellaneous / IT Support - Account Unlock",
        "content": "Email IT team from personal email with name, ID, and email."
    },
    # Fieldglass from emails
    {
        "title": "Fieldglass - Hour Types and Submission",
        "content": "Use ST/HR (≤40/week), OT/HR (>40/week), DT/HR (shift diff), 0 hours (non-work). Submit by Saturday EOD (Sunday-Saturday), match BizX. Deadline Oct 11 for past."
    },
    {
        "title": "Fieldglass - Pre-Approved Time-Off",
        "content": "Pre-approved (pre-Infinite) as worked (ST/HR); post-join leave as 0 hours (non-worked). Requires Fiserv approval, notify Infinite."
    },
    {
        "title": "Fieldglass - Technical Support",
        "content": "Contact @Swati Das for login issues. Access at https://www.fieldglass.net/ or regional URL."
    },
    {
        "title": "Fieldglass - On-Call/Outside Hours",
        "content": "Log on-call as OT/HR (>40) or Other/HR (waiting/received, non-exempt unpaid). Align with BizX worked totals."
    },
    # Emails (e.g., Suparno's Fieldglass emails)
    {
        "title": "Fieldglass Timesheet Requirement - Sep 28, 2025",
        "content": "Capture all work hours in Fieldglass for compliance. Register at earliest. Use ST/HR (≤40), OT/HR (>40). Submit by Saturday EOD. Match BizX. Past timesheets due Oct 11."
    },
    {
        "title": "Business Travel Process - General",
        "content": "Get Fiserv Manager approval (copy Manas & Naagamuthu), raise in BizX, select air/hotel options. Pay hotel/car with personal card, reimburse via Concur."
    }
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
st.markdown("Welcome, distinguished ICS Team member! Your exclusive guide to Policies, Payroll, Timesheets, Benefits, and more awaits. Current time: 04:32 PM EDT, October 1, 2025. 🌟")
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
