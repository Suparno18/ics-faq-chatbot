import streamlit as st
import math
from collections import Counter
import numpy as np
import re

# Full handbook chunks (from pasted OCR, emails, Excel - no truncation)
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
        "content": "30 days time-off balance is applicable to employees
