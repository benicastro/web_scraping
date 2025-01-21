# Importing libraries
import requests
import xlwt
from xlwt import Workbook
import smtplib
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

def get_job_postings():
    res = requests.get(url=BASE_URL, headers=REQUEST_HEADERS)
    return res.json()

if __name__ == "__main__":
    job_posting_sample = get_job_postings()[1]
    print(job_posting_sample)


# # Creating a workbook
# wb = Workbook()

# # Adding a sheet to the workbook
# sheet1 = wb.add_sheet('Sheet 1')

# # Writing data to the sheet
# sheet1.write(0, 0, 'Hello')

# # Saving the workbook
# wb.save('example.xls')