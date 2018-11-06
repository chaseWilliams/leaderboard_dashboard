from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from lib.analytics import get_leaderboard_data
import httplib2
import gspread
import json

scope = ['https://www.googleapis.com/auth/analytics.readonly',
            'https://spreadsheets.google.com/feeds',   
            'https://www.googleapis.com/auth/drive']
YEAR = 2018
MONTH = 1
MONTHS_TO_RETURN = 12

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
http = creds.authorize(httplib2.Http())

sheets_manager = gspread.authorize(creds)
analytics_service = build('analytics', 'v4', http=http)

website_data = []
with open('view_ids.csv') as f:
    for line in f.readlines():
        view_id, website = line.split(',')
        data = get_leaderboard_data(analytics_service, view_id, YEAR, MONTH, MONTHS_TO_RETURN)
        website_data.append({
            'website': website,
            'data': data
        })
        
print(json.dumps(website_data, sort_keys=True, indent=2))

