import streamlit as st
import math
from collections import Counter
import numpy as np
import re

# Excel data from "FIG - Bizx timesheet - Sep 2025-10-1-25.xlsx" (Sheet "Timesheet Report Day Wise (28)")
excel_data = {
    "20113324": {"name": "Sudarsana Sai Meruva", "email": "Sudarsana.Meruva@infinite.com", "doj": 44461, "role": "Project Manager", "manager": "MANAS RANJAN SAHU", "client": "Fiserv Solutions, LLC", "project": "FIG Operations and Implementations", "entries": [
        {"date": 45901, "hours": 8, "category": "Holiday", "status": "Approved", "week_ending": 45905},
        {"date": 45901, "hours": 0, "category": "Worked", "status": "Approved", "week_ending": 45905},
        {"date": 45902, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905},
        {"date": 45902, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905},
        {"date": 45903, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905},
        {"date": 45903, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905},
        {"date": 45904, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905},
        {"date": 45904, "hours": 8, "category": "Worked", "status": "Approved", "week_ending": 45905},
        {"date": 45905, "hours": 0, "category": "Holiday", "status": "Approved", "week_ending": 45905}
        # Truncated for brevity - include all rows (2-42631) in actual code
    ]},
    # Add more employee entries (e.g., 20120551, 20120567) from rows 42623-42631 as needed
    "20120551": {"name": "Victor Njoh Anjeh", "email": "Victor.Anjeh@infinite.com", "doj": 45912, "role": "Program Manager", "manager": "MANAS RANJAN SAHU", "client": "Fiserv Solutions, LLC", "project": "FIG Operations and Implementations", "entries": [
        {"date": 45929, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45930, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933}
    ]},
    "20120567": {"name": "Nicette Garcias", "email": "Nicette.Garcias@infinite.com", "doj": 45917, "role": "Client Tech Support Engineering - Professional II", "manager": "Sudarsana Sai Meruva", "client": "Fiserv Solutions, LLC", "project": "FIG Operations and Implementations", "entries": [
        {"date": 45931, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45932, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45933, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45927, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45928, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45929, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933},
        {"date": 45930, "hours": 0, "category": "", "status": "Not-Submitted", "week_ending": 45933}
    ]}
    # Expand with all 42,631 rows if needed - for now, sample data is sufficient
}

# Handbook content split into granular chunks
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
        "title": "1. Overtime & Special Hours - Process for overtime hours submission",
        "content": "Note - Overtime payment is ONLY applicable for Salaried Non-Exempt Employees. Salaried Exempt Employees can submit more than 40 standard worked hours/ week in Bizx but they are NOT eligible for Overtime payment. All Non-Exempt (Hourly Employees) should be submitting their timesheet in Bizx with their regular 40 hours + OT hours. For OT hours, please ensure that you get the email approval from your Fiserv Manager in advance and then only submit your OT hours in the BizX timesheet. In case your Fiserv manager is on leave / vacation / unable to approve your OT on email for any reason, please wait till your Fiserv manager is back and then only submit your OT hours in Bizx. Please Note - There is no additional category to enter OT hours in BizX, anything entered more than standard 40 worked hrs. are treated as OT hours by payroll team."
    },
    {
        "title": "1. Overtime & Special Hours - Process to claim OT/Shift Differential Bug Bash/On call hours",
        "content": "Please find the below table on the agreed process, as of now. This table will be updated as soon as we have an answer from Fiserv Management on few of the points below – | Category | OT Hours | Shift Differential | Bug Bash Hours | On Call Waiting Hours | On Call Received Hours | Salaried Non-Exempt Employees | Employee will enter the timesheet in BizX after getting approval from your Fiserv Manager on the OT Hours. USPayroll team process it. Please reach out to US Payroll <uspayroll@infinite.com> for any questions on this. | Employee will enter the timesheet in BizX. USPayroll team process it. Please reach out to US Payroll <uspayroll@infinite.com> for any questions on this. | Not Applicable | Not Applicable | Not Applicable | Salaried Employees (Exempt) | Fiserv/Infinite managers are working on the process to finalize this claim process. Until then please support the project as needed. Get an approval from your Fiserv Manager and notify your infinite manger on the approval. | Employee will enter the timesheet in BizX. USPayroll team process it. Please reach out to US Payroll <uspayroll@infinite.com> for any questions on this. | Fiserv/Infinite managers are working on the process to finalize this claim process. Until then please support the project as needed. Get an approval from your Fiserv Manager and notify your infinite manger on the approval. | Fiserv/Infinite managers are working on the process to finalize this claim process. Until then please support the project as needed. Get an approval from your Fiserv Manager and notify your infinite manger on the approval. | Fiserv/Infinite managers are working on the process to finalize this claim process. Until then please support the project as needed. Get an approval from your Fiserv Manager and notify your infinite manger on the approval."
    },
    {
        "title": "2. Timesheet / Payroll - How to access Infinite timesheet",
        "content": "‘BizX’ is available over the internet. Employees have to login to the portal to access the Timesheet to log their work hours, leave hours. Note: We recommend users to access the Portal using Google Chrome, Edge and IE browsers for the best view. Type https://bizx.infinite.com/ in the browser, navigate to the Timesheet -> My Timesheet as shown below."
    },
    {
        "title": "2. Timesheet / Payroll - To add Non work hours",
        "content": "To add Non work hours (vacation/sick/personal/Jury Duty/Bereavement/Break Time/Holiday), please add a row and select the corresponding non work time as shown below."
    },
    {
        "title": "2. Timesheet / Payroll - When do I need to submit my Timesheet?",
        "content": "Mandatory Activity - Timesheets need to be submitted by Monday 11 Eastern time for the previous week. (If Bizx is down or, having an outage, please keep checking ITSG emails and immediately update when Bizx is available)"
    },
    {
        "title": "2. Timesheet / Payroll - My Timesheet is locked or grayed out",
        "content": "Timesheets will be locked on the Monday following at 11 EST after each payroll cut-off date (biweekly). Once a payroll is locked, the user will not be able to submit their time sheet. In such cases, reach out to uspayroll@infinite.com to unlock the timesheet OR submit the manual timesheet to uspayroll@infinite.com and request your infinite manager approval for the same (Avoid manual timesheet submission for accountability purposes, always submit your timesheet in Bizx)."
    },
    {
        "title": "2. Timesheet / Payroll - What if I have missed filling my timesheet for the pay period on time and now my timesheet is locked?",
        "content": "Employee can send an email to US Payroll uspayroll@infinite.com to unlock the timesheet for the missing period. Once unlocked, employee can fill in the timesheet and submit. Payroll team will process your timesheet in the next pay cycle, through retro process."
    },
    {
        "title": "2. Timesheet / Payroll - I don’t have a time-off balance available and would like to avail a time-off. What is the process for this?",
        "content": "Any time-off request needs to be approved by your Fiserv Manager and same needs to be notified to your Infinite Manager. Leave Payment is subject to the accruals and available leave balance. If there is no available balance and you have taken leave, then it will be leave without pay."
    },
    {
        "title": "2. Timesheet / Payroll - Does BizX allow you to enter the timesheets for future dates?",
        "content": "No, you can only fill the current week’s timesheet for worked hours, not future hours. If you are going on vacation, please ensure to submit your timesheet in Bizx, from any device, anywhere across the world."
    },
    {
        "title": "2. Timesheet / Payroll - What is the policy for Jury Duty?",
        "content": "Please inform your Fiserv & infinite manager about your Jury Duty and get an approval to attend the same. Send a copy of the summons to USHR@infinite.com. Salaried employees will be paid their base pay for up to two weeks of jury or subpoenaed witness duty served. Hourly employees do not receive pay for jury or subpoenaed witness duty unless mandated. Jury duty/Witness Leave is recorded as such on time records, and a copy of the summons and of the paid-time statements provided by the jurisdiction must be attached."
    },
    {
        "title": "2. Timesheet / Payroll - How to access Paystubs and W-2s?",
        "content": "Paystubs and W-2s can be accessed via URL, https://workforcenow.adp.com. If you have any questions and/or issues regarding ADP iPay, please contact Infinite Payroll at USPayroll@infinite.com."
    },
    {
        "title": "2. Timesheet / Payroll - Where can I see my time-off balance?",
        "content": "Time-off balance can only be seen on your most recent pay statement."
    },
    {
        "title": "2. Timesheet / Payroll - I see an option to request time-off balance in ADP, can I request here?",
        "content": "No, you do not have to request in ADP, this is not applicable for you."
    },
    {
        "title": "3. Leave & Time-Off - What is the process to request time-off?",
        "content": "Send an email to Fiserv Manager copying your infinite Manager. Once approved by Fiserv Manager, you are good to the take time-off."
    },
    {
        "title": "3. Leave & Time-Off - What is pre-approve time off? How do I enter the timesheet for this?",
        "content": "Time-Off Approved by your Fiserv Manager before joining infinite is called as pre-approve time-off. This is applicable to Salaried employees only. For all the pre-approved time-off, you will enter the hours as worked hours in BizX and submit."
    },
    {
        "title": "3. Leave & Time-Off - How do I enter time for the time-off approved after joining Infinite in BizX?",
        "content": "You will enter this time as non-worked hours in BizX and submit."
    },
    {
        "title": "3. Leave & Time-Off - I was part of unlimited PTO with Fiserv. How is my one-time 30 days time-off balance distributed?",
        "content": "30 days time-off balance is applicable to employees who were part of unlimited PTO with Fiserv. It is distributed as 25(200 Hours) vacation days and 5(40 hours) sick days. These time-off balance – 240 hours will get rolled over to year 2026. During the year 2025, you will not accumulate any more time-off balance. Accrual of time-off balance will be seen from the first paycheck in the year 2026."
    },
    {
        "title": "3. Leave & Time-Off - I was not part of unlimited PTO with Fiserv, but I am a salaried employee. Do I get one time-off balance added?",
        "content": "No, you will get the time-off accrual from the first paycheck with infinite as per process."
    },
    {
        "title": "3. Leave & Time-Off - Does vacation carry over from year to year?",
        "content": "Yes, maximum of 80 vacation hours will get carried over from year to year and sick hours will elapse. (Please don’t get confused with your 30 days one-time leave, as I have explained 240 hours will get rolled over to year 2026)"
    },
    {
        "title": "3. Leave & Time-Off - Which Holidays are applicable for us?",
        "content": "We follow Fiserv Holiday only."
    },
    {
        "title": "3. Leave & Time-Off - How many hours of vacation/sick added to me for every paycheck?",
        "content": "Please find the information below, same can be seen in Employee handbook as well."
    },
    {
        "title": "4. Benefits - I have questions about my Benefits.",
        "content": "Please refer to the Benefits provided as a part of onboarding documentation."
    },
    {
        "title": "5. Miscellaneous / IT Support - How can I access infinite email?",
        "content": "Web URL to access infinite mailbox is https://outlook.office.com. Use same credentials as BizX to login to infinite mailbox. Please clear browser cache OR use incognito mode while trying to access infinite email."
    },
    {
        "title": "5. Miscellaneous / IT Support - What are the support groups we have and how do we contact them?",
        "content": "For any questions/issues with BizX, please contact BizX-Support BizX-Support@infinite.com, copy your infinite manager for the visibility. For any questions/issues with Payroll, please contact US Payroll uspayroll@infinite.com, copy your infinite manager for the visibility. For any questions/issues with Employee Benefits (Medical/Dental/Vision Insurance, 401K, HSA, e.t.c.,), please contact USHR <USHR@infinite.com>, copy your infinite manager for the visibility. For any questions/issues with IT (infinite Email access, password reset, e.t.c.,), please contact ITSG-US ITSG-US@infinite.com, copy me for visibility."
    },
    {
        "title": "5. Miscellaneous / IT Support - How can I reset my password?",
        "content": "Outlook will require you to change your password every 90 days. Go to https://passwordreset.microsoftonline.com."
    },
    {
        "title": "5. Miscellaneous / IT Support - Can I work from a location different than my current location?",
        "content": "No, even if you are working remotely, for any change of work location, please contact Infinite USHR."
    },
    {
        "title": "5. Miscellaneous / IT Support - My infinite account (BizX/Email) is locked. How to get my account unlocked?",
        "content": "Employee can send an email to IT team with the details of Employee name, Employee number and email address from the personal email address. IT team will send instructions on how to reset/unlock the password."
    },
    # Fieldglass-specific chunks from emails
    {
        "title": "Fieldglass - Hour Types and Submission",
        "content": "Fieldglass tracks actual worked time for compliance and capacity. Use ST/HR for standard hours (up to 40/week), OT/HR for overtime (>40/week), DT/HR for shift differential (nights/weekends), and 0 hours for non-worked (holidays, sick, leave). Submit weekly by Saturday EOD (Sunday-Saturday). Align with BizX Total Worked Hours, mandatory for payroll (Monday 11 AM EST, Saturday-Friday)."
    },
    {
        "title": "Fieldglass - Pre-approved Time Off",
        "content": "Pre-approved time-off (Fiserv before Infinite) is logged as worked hours in BizX and Fieldglass (ST/HR, e.g., 8 hours/day). Standard post-joining leave (sick/vacation) is 0 hours in Fieldglass, non-worked in BizX. Requires Fiserv Manager approval, notify Infinite Manager."
    },
    {
        "title": "Fieldglass - Technical Support",
        "content": "For login issues (e.g., locked accounts), @Swati Das is our FG Champion. Request her to assist via email. Access Fieldglass at https://www.fieldglass.net/ or regional URL, navigate to My Timesheet."
    },
    {
        "title": "Fieldglass - On-Call/Outside Hours",
        "content": "Time called in outside normal hours (e.g., on-call) is worked time in Fieldglass—use OT/HR if >40/week, or Other/HR for on-call waiting/received (non-exempt not paid yet, log for tracking). Align with BizX worked totals, exclude from 0-hour non-worked entries."
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
    return retrieved if retrieved else "No matching section found. Please provide more details."

def lookup_excel_data(query):
    for emp_id, data in excel_data.items():
        if data["name"].lower() in query.lower() or emp_id in query:
            latest_entry = data["entries"][-1]  # Latest week ending
            return f"### Employee Lookup: {data['name']}\n- Employee ID: {emp_id}\n- Role: {data['role']}\n- Manager: {data['manager']}\n- Latest Entry (Week Ending {latest_entry['week_ending']}): {latest_entry['hours']} hours, {latest_entry['category']} on {latest_entry['date']}, Status: {latest_entry['status']}"
    return ""

# Streamlit UI with awesome user experience
st.title("ICS Team FAQs Chatbot - Your Friendly Policy Guide")
st.markdown("Ask about policies, timesheets, leave, benefits, IT support, or check your status! Chat history saved per session. Current time: 1:02 PM EDT, October 1, 2025.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question here (e.g., 'What is Sudarsana Sai Meruva's status?')"):
    # Extract user name from email if available
    user_name = prompt.split('@')[1].split('>')[0] if '@' in prompt else "User"
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Excel lookup first, then handbook retrieval
    excel_response = lookup_excel_data(prompt)
    retrieved = retrieve_sections(prompt)
    response = f"Hi @{user_name},\n\nThank you for your question. Here's the relevant information:\n\n"
    if excel_response:
        response += excel_response + "\n\n"
    if retrieved:
        response += retrieved + "\n\n"
    else:
        response += "No handbook match found. Please refine your question.\n\n"
    response += f"To recap the process:\n- Please follow the guidelines above (e.g., log hours as ST/HR, OT/HR, or DT/HR in Fieldglass, submit by Saturday EOD, October 4, 2025).\n- If unsure, please provide more details or contact support (e.g., @Swati Das for Fieldglass, USPayroll@infinite.com for payroll).\n\nIf this doesn't answer your question, please feel free to share more details, and I'll be happy to guide you further.\n\nThanks, and Regards,\nSuparno Chowdhury | Project Manager\nInfinite | The PlatformizationTM Company\nExciting times...infinite possibilities…\nEmail: suparno.chowdhury@infinite.com | Cell: +1-470-404-0740"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Add flair for user experience
st.sidebar.title("Quick Links")
st.sidebar.markdown("- [Fieldglass Login](https://www.fieldglass.net/)\n- [BizX Portal](https://bizx.infinite.com/)\n- [Paystubs](https://workforcenow.adp.com)\n- [Support Email](mailto:suparno.chowdhury@infinite.com)")
st.sidebar.button("Clear Chat", on_click=lambda: st.session_state.update(messages=[]))
