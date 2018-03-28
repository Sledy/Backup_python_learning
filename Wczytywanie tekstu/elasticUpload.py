from multiprocessing import Process, Lock
import os
import logging
# import shutil
# import matplotlib.pyplot as plt
# import scipy.stats as st
# import numpy as np
import pandas as pd
global target_metrics
global duplisource
global dfiter
global missedreport
global df_sourced
global df


class missedCount():
    def __init__(self):
        global target_metrics
        global df_sourced
        global missedreport
        global df

        with open('data.csv', 'r'):
            df = pd.read_csv('data.csv', sep=';')
        # missedreport = pd.DataFrame(columns=['device_name', 'unix_time'])
        # with open("df.sourced.csv", 'r') as file:
        df_sourced = df.loc[df['source'].str.contains('|'.join(target_metrics))]
        self.preparefiles()
        logging.info('value {0}'.format(df_sourced.head()))
        self.countHandler()

    def preparefiles(self):
        global duplisource
        global dfiter
        duplisource = df_sourced[['source', 'device_id', 'device_name', 'value']].drop_duplicates()
        # duplisource.to_csv("duplicource.csv", sep=";")
        # logging.info('exported duplisource')
        dfiter = df.drop_duplicates(['current_iteration'], keep='first')

    def countHandler(self):
        lock = Lock()
        for index, row in duplisource.iterrows():
            try:
                Process(target=self.count, args=(index, row)).start()
                print("started a child process")
            finally:
                pass


    def count(self, index, row):
        global duplisource
        global dfiter

        s = 'source'
        di = 'device_id'
        dn = 'device_name'
        ci = 'current_iteration'
        valu = 'value'
        newrow = row
        missedreport = pd.DataFrame(columns=['source', 'device_name', 'value', 'unix_time', 'iteration', 'device_id'])
        for i in range(int(max(df_sourced['current_iteration']))):  # test_result.iterations
            current = None
            current = df_sourced[
                (df_sourced[s] == row[s]) & (df_sourced[di] == row[di]) & (df_sourced[valu] == row[valu]) & (df_sourced[dn] == row[dn]) & (
                        df_sourced[ci] == i + 1)]
            if i+1 % 1000 == 0:
                logging.info('passed {0} iterations'.format(i+1))
            if current.empty:
                newrow = row
                missedreport = missedreport.append([{'source': newrow['source'], 'device_name': newrow['device_name'],
                                                     'value':newrow['value'], 'unix_time':
                    dfiter.loc[dfiter['current_iteration'] == i + 1, 'unix_time'].iloc[0], 'iteration':i+1, 'device_id': newrow['device_id'] }], ignore_index=True)
        missedreport.to_csv('missedtemp.csv' , mode='a', header=True, sep=';', )


class missed_upload():
    def __init__(self, data):
        self.data = pd.read_csv('missedtemp.csv', sep=';')
        self.uploadmissed()

    def uploadmissed(self):
        list(self.data.columns.values)
        sc = 'source'
        for index, row in self.data.iterrows():
            MISSEDFLAG = 'missed'
            newrow = row
            # The construction of RESTjson json fails with KeyError if performed with .format() or with direct references to the current row
            # eg. newrow['source'] doesn't work, unless its assigned to a variable and the variable is used for the json construction
            s = newrow['source']
            d = newrow['device_name']
            print(str(index))
            v = newrow['value']
            u = newrow['unix_time']
            dev_id = newrow['device_id']
            print(dev_id)
            RESTjson = "{\"source\":\"" + s + "\", \"device_name\":\"" + d + "\", \"value\":\"" + v + "\", \"unix_time\":\"" + str(u) + "\", \"latency\":\"" + str(0) + "\", \"missedFlag\":\"" +MISSEDFLAG+"\", \"device_id\": \"" + dev_id + "\"}"
            # headers = {"Content-Type": "application/json"}
            url = 'curl http://localhost:9200/scenario/event -H \'Content-Type: application/json\' -d \'{0}\''.format(RESTjson)
            os.system(url)

class latencyCountNUpload():
    def __init__(self):
        #constructs and uploads latency metric for earch device, iteration etc.
        self.data = self.data = pd.read_csv("data.csv", sep=";" , index_col = False)
        self.target_metrics =['CLIENT', 'BOT_CALLBACK']
        self.removes()
        self.sort()

    def removes(self):
        self.data = self.data.loc[self.data['source'].str.contains('|'.join(self.target_metrics))]
        # print(df2.head())

    def sort(self):
        for index, row in self.data.iterrows():
            print(self.data.columns)
            newrow = row
            # The construction of RESTjson json fails with KeyError if performed with .format() or with direct references to the current row
            # eg. newrow['source'] doesn't work, unless its assigned to a variable and the variable is used for the json construction
            s = newrow['source']
            print(s)
            d = newrow['device_name']
            print(d)
            v = newrow['value']
            u = newrow['unix_time']
            lat = newrow['latency']
            dev_id = newrow['device_id']
            MISSEDFLAG = "non-missed"
            a = "{\"source\":\"" + s + "\", \"device_name\":\"" + d + "\", \"value\":\"" + v + "\", \"unix_time\":\"" + str(u)+ "\", \"latency\":\"" + str(lat) + "\", \"missedFlag\":\"" +MISSEDFLAG+ "\", \"device_id\": \""+ dev_id+"\" }"
            # headers = {"Content-Type": "application/json"}
            url = 'curl http://localhost:9200/scenario/event -H \'Content-Type: application/json\' -d \'{0}\''.format(a)
            os.system(url)


if __name__ == '__main__':
    target_metrics = ['CLIENT', 'BOT_CALLBACK']
    logging.basicConfig(level=logging.INFO)
    mc = missedCount()
    mu = missed_upload()
    lc = latencyCountNUpload()
    os.remove('missedtemp.csv')
    os.rename('data.csv', 'data.uploaded.txt')





