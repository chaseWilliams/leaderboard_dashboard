import gspread


def upload_data_to_sheets(sh, website_data, sh_name):
    ## TODO
    # create header on row 2
    worksheet = sh.open(sh_name).get_worksheet(0)
    row = 3
    for website in website_data:
        worksheet.update_cell(row, 1, website['website'])
        col = 3
        worksheet.update_cell(row, 2, 'Monthly Users')
        worksheet.update_cell(row + 1, 2, 'Monthly Pageviews')
        worksheet.update_cell(row + 2, 2, 'Top Pages')
        for month in website['data']:
            worksheet.update_cell(row, col, month['users'])
            worksheet.update_cell(row + 1, col, month['unique_pageviews'])
            worksheet.update_cell(row + 2, col, '\n'.join(month['top_pages']))
            col = col + 1
        row = row + 4
