import gspread
from oauth2client.service_account import ServiceAccountCredentials


class My_API():

    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            'client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = self.client.open("My_sheet").sheet1

    def print_rows(self, row_number):
        print(list(filter(lambda x: x != '',
                          (self.sheet.row_values(row_number)))))

    def give_dimensions(self):
        width = self.sheet.col_count
        heigth = self.sheet.row_count
        print ('Arkusz ma {} kolumn i {} wierszy'.format(width, heigth))

    def resize_sheet(self):
        rows_number = input('Prosze podac liczbe wierszy: ')
        column_number = input('Prosze podac liczbe kolumn: ')
        self.sheet.resize(rows=rows_number, cols=column_number)

    def add_row(self, row, index):
        self.sheet.insert_row(row, index)

    def import_from_csv(self):
        # name_file = input('Podaj nazwe pliku ktory chcesz wrzucic 
        # do sheeta: ')
        with open('Risk report.csv', 'r', encoding="utf-8") as file:
            self.client.import_csv(
                '1mnxUdFBfLMPQko5YFNZhrcHJs4hTWPrzRdiSUknjd8M', file.read())

    def add_data(self):
        empty_row = len(list(filter(None, self.sheet.col_values(1)))) + 1
        columns_to_fill = [1, 5, 9]
        file_name = 'Plus.txt'
        with open(file_name, 'r') as file:
            zapis = file.read().split(',')
            print(zapis)
            index = 0
            for element in zapis:
                self.sheet.update_cell(
                    empty_row, columns_to_fill[index], element)
                index += 1


my_api = My_API()
my_api.resize_sheet()
