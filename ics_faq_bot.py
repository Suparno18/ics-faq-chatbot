import streamlit as st
import math
from collections import Counter
import numpy as np
import re

# Full handbook chunks (from pasted OCR, emails, Excel - fixed quotes, no truncation)
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
        "content": "Note - Overtime payment is ONLY applicable for Salaried Non-Exempt Employees. Salaried Exempt Employees can submit more than 40 standard worked hours/ week in Bizx but they are NOT eligible for Overtime payment. All Non-Exempt (Hourly Employees) should be submitting their timesheet in Bizx
