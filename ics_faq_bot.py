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
        "client": "Fis
