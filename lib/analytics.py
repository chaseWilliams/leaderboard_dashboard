from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2
import calendar

def get_leaderboard_data(analytics, view_id, year, month, months):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
    view_id: Google Analytics websites' identifier
    year: the year (int)
    month: the month (int)
    months: number of months to get data for
  Returns:
    The website's monthly data for the specified time span
  """
  data = []
  for i in range(months):
    curr_year = (year * 12 + month + i - 1) // 12
    curr_month = (month + i - 1) % 12 + 1
    month_start_date = str(curr_year) + '-' + make_two_digits(curr_month) + '-01'
    month_end_date = month_start_date[:8] + make_two_digits(calendar.monthrange(curr_year, curr_month)[1])

    row = {}
    row['month'] = month_start_date
    response = analytics.reports().batchGet(
        body={
          'reportRequests': [{
            'viewId': view_id,
            'dateRanges': [{'startDate': month_start_date, 'endDate': month_end_date}],
            'metrics': [{'expression': 'ga:users'}, {'expression': 'ga:uniquePageviews'}]
          }]
        }
    ).execute()
    row['users'] = response['reports'][0]['data']['totals'][0]['values'][0]
    row['unique_pageviews'] = response['reports'][0]['data']['totals'][0]['values'][1]
    response = analytics.reports().batchGet(
        body={
          'reportRequests': [{
            'viewId': view_id,
            'dateRanges': [{'startDate': month_start_date, 'endDate': month_end_date}],
            'metrics': [{'expression': 'ga:pageviews'}],
            'dimensions': [{'name': 'ga:pagepath'}],
            'orderBys': [{'fieldName': 'ga:pageviews', 'sortOrder': 'DESCENDING'}]
          }]
        }
    ).execute()
    try:
      row['top_pages'] = [
        response['reports'][0]['data']['rows'][0]['dimensions'][0],
        response['reports'][0]['data']['rows'][1]['dimensions'][0],
        response['reports'][0]['data']['rows'][2]['dimensions'][0]
      ]
    except KeyError:
      row['top_pages'] = ['', '', '']
    
    data.append(row)
  return data
  
def make_two_digits(num):
  result = str(num)
  if len(result) is 1:
    result = '0' + result
  return result