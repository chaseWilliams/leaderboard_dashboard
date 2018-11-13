import gspread
from gspread_formatting import *
import datetime
import string
import time

def upload_data_to_sheets(sh, website_data, sh_name):
    ## TODO
    # create header on row 2
    worksheet = sh.open(sh_name).get_worksheet(0)
    # create header
    worksheet.update_cell(2, 1, 'Website')
    worksheet.update_cell(2, 2, 'Metrics')
    for i, month in enumerate(website_data[0]['data']):
        month_name = datetime.date.fromisoformat(month['month']).strftime("%B")
        worksheet.update_cell(2, i + 3, month_name)
    row = 3
    print('Uploading data to Google Sheets')
    for website in website_data:
        print(website['website'].strip())
        worksheet.update_cell(row + 1, 1, website['website'].strip())
        col = 3
        worksheet.update_cell(row, 2, 'Monthly Users')
        worksheet.update_cell(row + 1, 2, 'Monthly Pageviews')
        worksheet.update_cell(row + 2, 2, 'Top Pages')
        
        for i, month in enumerate(website['data']):
            worksheet.update_cell(row, col, month['users'])
            # APPLY COLOR FORMATTING
            if i is not 0:
                good_color = month['users'] > website['data'][i - 1]['users']
                apply_color_formatting(worksheet, good_color, row, col)
            worksheet.update_cell(row + 1, col, month['unique_pageviews'])
            if i is not 0:
                good_color = month['unique_pageviews'] > website['data'][i - 1]['unique_pageviews']
                apply_color_formatting(worksheet, good_color, row + 1, col)
            worksheet.update_cell(row + 2, col, '\n'.join(month['top_pages']))
            col = col + 1
        row = row + 4
        time.sleep(100)

def apply_color_formatting(worksheet, good_color, row, col):
    color = Color(56 / 255, 118 / 255, 29 / 255)
    if not good_color:
        color = Color(204 / 255, 0, 0)
    fmt = CellFormat(textFormat=TextFormat(foregroundColor=color))
    cell_range = string.ascii_uppercase[col - 1] + str(row)
    cell_range = cell_range + ':' + cell_range
    format_cell_range(worksheet, cell_range, fmt)