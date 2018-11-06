import gspread


def upload_data_to_sheets(sh, website_data):
    worksheet = sh.get_worksheet(0)
    for website in website_data:
        