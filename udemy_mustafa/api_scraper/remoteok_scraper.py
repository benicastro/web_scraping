# Importing libraries
import requests
import xlwt
from xlwt import Workbook
import smtplib
import os
import creds
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

# Constants
BASE_URL = "https://remoteok.com/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    'Accept-Language': 'en-US,en;q=0.9',
}

# Function to get job postings
def get_job_postings():
    try:
        res = requests.get(url=BASE_URL, headers=REQUEST_HEADERS)
        res.raise_for_status()  # Raise an error for bad responses
        return res.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return []

# Function to output jobs to excel
def output_jobs_to_excel(jobs):
    if not jobs:
        print("No jobs to write to Excel.")
        return
    try:
        wb = Workbook()
        job_sheet = wb.add_sheet('Jobs')
        header_rows = list(jobs[0].keys())
        for i in range(len(header_rows)):
            job_sheet.write(0, i, header_rows[i])
        for i in range(len(jobs)):
            job = jobs[i]
            values = list(job.values())
            for x in range(len(values)):
                job_sheet.write(i+1, x, values[x])
        wb.save('remoteok_jobs.xls')
    except Exception as e:
        print(f"Error writing jobs to Excel: {e}")

# Function to send email
def send_email(subject, body, to_emails, attachment_paths=[]):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    gmail_user = creds.GMAIL_USER
    gmail_password = creds.GMAIL_PASSWORD

    if not gmail_user or not gmail_password:
        print("Environment variables for Gmail credentials are not set.")
        exit(1)

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = COMMASPACE.join(to_emails)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    # Attach multiple files
    for attachment_path in attachment_paths or []:
        try:
            with open(attachment_path, "rb") as file:
                part = MIMEApplication(file.read(), Name=basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{basename(attachment_path)}"'
            msg.attach(part)
        except FileNotFoundError:
            print(f"Attachment file not found: {attachment_path}")
            continue
        except Exception as e:
            print(f"Error attaching file {attachment_path}: {e}")
            continue

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_emails, msg.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check your email and password.")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    job_posting_sample = get_job_postings()[1:]
    output_jobs_to_excel(job_posting_sample)
    send_email(
        subject="RemoteOK Job Postings",
        body="Please find attached the latest job postings from RemoteOK.",
        to_emails=["contact_astroc@gmail.com"],
        attachment_paths=["remoteok_jobs.xls"]
    )
