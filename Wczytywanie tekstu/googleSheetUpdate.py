from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#residual code from google API, commented out, but left just in case
"""
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
"""
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'
CELLDEVICELOCATION= { 'SYLVANIA Smart A19 Tunable White' : 'U1',
                          'Hue A60 White':'AO1',
                          'GE Plug-In Switch': 'BF1',
                          'SYLVANIA Smart A19 Tunable White 2': 'A1',
                          'Yale Touchscreen Deadbolt Door Lock': 'BX1',
                          'Leviton Z-Wave Switch': 'CP1',
                          'Multipurpose Sensor': 'DH1',
                          }
V2DEVICELOCATION = {'SYLVANIA Smart A19 Tunable White' : 'V1',
                          'Hue A60 White':'BW1',
                          'GE Plug-In Switch': 'CR1',
                          'SYLVANIA Smart A19 Tunable White 2': 'A1',
                          'Yale Touchscreen Deadbolt Door Lock': 'DM1',
                          'Leviton Z-wave switch': 'BB1',
                          'Multipurpose Sensor V2': 'AQ1',}
temp = ''
def get_credentials():
    #Gets valid user credentials from storage.

    # residual code from google API, commented out, but left just in case

    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')
    """
    store = Storage('secret_client.json')
    credentials = store.get()
    
    return credentials

def updateGoogleSheet(device, valuesParameter):
    """Sheets API.

    Creates a Sheets API service object and updates the spreadsheet at botpilogs@gmail.com
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1ZbXeSFn8hBy-bPPW0zBB0sxUttNFAQuhwpiHYP4ycoo'

    if temp == '1':
        range_Name = 'cell!' + CELLDEVICELOCATION[device]
        print(range_Name)
    elif temp == '2':
        range_Name = 'v2!' + V2DEVICELOCATION[device]
    else:
        print("wrong input")
        exit(1)
    if (len(valuesParameter)) >5:
        valuesParameter[3:5], valuesParameter[5:7] = valuesParameter[5:7], valuesParameter[3:5]
    values = []
    values.append(valuesParameter)
    body = {
        'values': values
    }
    print("writing {} to {}".format(values, range_Name ))
    value_input_option = 'USER_ENTERED'
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_Name,
        valueInputOption=value_input_option, body=body).execute()



class importFile():
    file = 'ss'
    valuesBOT = []
    valuesCLIENT = []
    source = {}
    title = []
    devices = {}
    date = '2013/12/3'
    output = []
    temp=''
    def __init__(self):
        self.setDate()
        self.openFile()
        self.setupLabels()
        self.valueMaster()
        self.clean()


    def setDate(self):
        print(self.output)
        self.date = input("input date you would like to tag for today (e.g. 22/11/17)")

    def openFile(self):
       temp = open('temp.csv', 'r')
       temp = temp.read().splitlines()
       self.file = temp
       for i in range(len(temp)):
           self.file[i]= temp[i].split(';')

    def setupLabels(self):
        for i in range(len(self.file)-1):
            if self.file[i+1][1] not in self.devices.keys():
                self.devices[(self.file[i+1][1])] = self.file[i+1][2]
        self.source = {'BOT': 'BOT_CALLBACK', 'CLIENT':'CLIENT'}

    def valueMaster(self):
       for i in self.devices.keys():
           deviceValues = []
           for z in range(len(self.file) - 1):
               if self.file[z][1] == i and self.file[z][3] not in deviceValues:
                   deviceValues.append(self.file[z][3])
           print(deviceValues)
           self.output.append(self.date)
           for y in deviceValues:
               self.setupValues(i, y)
           print(self.output)

           updateGoogleSheet(self.temp,self.output )
           self.output = []

    def setupValues(self, device_id, deviceValue):
       for i in range(len(self.file)):
           latencyBOT = ''
           if self.file[i][0] == 'BOT_CALLBACK' and self.file[i][1] == device_id and self.file[i][3] == deviceValue:
               latencyBOT =  str(self.file[i][4])
               missedBOT = str(self.file[i][11])
               self.temp= self.devices[device_id]
               print(self.devices[device_id])
               self.output.append( latencyBOT )
               self.output.append(missedBOT)
       for i in range(len(self.file)):
           rowCLIENT = ''
           if self.file[i][0] == 'CLIENT' and self.file[i][1] == device_id and self.file[i][3] == deviceValue:
               latencyCLIENT = str(self.file[i][4])
               missedCLIENT = str(self.file[i][11])
               self.temp = self.devices[device_id]
               self.output.append(latencyCLIENT)
               self.output.append(missedCLIENT )

    def clean(self):
        os.remove('temp.csv')


if __name__ == "__main__":
    temp = input("Are You updating cell or v2 results ? enter 1 for cell and 2 for v2\n ")

    im = importFile()
