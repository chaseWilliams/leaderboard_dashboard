from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from lib.analytics import get_leaderboard_data
from lib.sheets import upload_data_to_sheets
import httplib2
import gspread
import time
import json

scope = ['https://www.googleapis.com/auth/analytics.readonly',
            'https://spreadsheets.google.com/feeds',   
            'https://www.googleapis.com/auth/drive']
YEAR = 2018
MONTH = 1
MONTHS_TO_RETURN = 12
VIEW_IDS = 'view_ids.csv'
CREDENTIALS = 'client_secret.json'
SHEET_NAME = 'Web Leaderboard Dashboard'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS, scope)
http = creds.authorize(httplib2.Http())

sheets_manager = gspread.authorize(creds)
analytics_service = build('analytics', 'v4', http=http)

website_data = []
print('Pulling data from Google Analytics')
with open(VIEW_IDS) as f:
    for line in f.readlines():
        view_id, website = line.split(',')
        print(website.strip())
        data = get_leaderboard_data(analytics_service, view_id, YEAR, MONTH, MONTHS_TO_RETURN)
        website_data.append({
            'website': website,
            'data': data
        })
        # have to sleep due to requests quota per 100 seconds
        # interestingly enough, batching requests doesn't affect what is counted 
        # towards quota, as they're interally counted. In other words, there's no way
        # to get all this data without going over the quota
        time.sleep(100)

#print(json.dumps(website_data, sort_keys=True, indent=2))

upload_data_to_sheets(sheets_manager, website_data, SHEET_NAME)