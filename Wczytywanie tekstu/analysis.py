from __future__ import print_function
import os
import sys
import logging
import shutil
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np
import pandas as pd
import time
import re


FILES_NAMES = []
SPLITTING_ON_VALUES = True
#variables directing the flow of execution
#GOOGLEUPLOAD - if the user want the results to bu published on google Sheets
#ISSCENARIO - if the user wants the in[ut data to be cut to within a certain time and the iteration number to be reset
#only if ISSCENARIO is y (yes), will the user be prompted if he/she wants the results to be published (GOOGLEUPLOAD)
GOOGLEUPLOAD = None
ISSCENARIO = None
OUTPUT = None

class TestException(Exception):
    """
    Class intended to differentiate errors that are result of wrong behaviour of System Under Test from
    errors that result in environmental or programmer errors.
    """
    pass

class Helper(object):


    @staticmethod
    def confidence_interval(a, confidence=0.95):
        # TODO This method is not implemented anywhere - delete ?
        #function returns confidence interval value
        ci = st.t.interval(confidence, len(a)-1, loc=np.mean(a), scale=st.sem(a))
        return (ci[0]+ci[1])/2.0-ci[0]

    @staticmethod
    def missed_event_count(a, iteration_events, iterations):
        """calculate missed events for each unique combination of source, device and value"""
        a=a.reset_index()
        b = a.groupby(['current_iteration']).count()
        b.columns = ['counter']

        missed = 0
        for i in range(iterations):
            iteration = i + 1
            if iteration in b.index:
                if b.loc[iteration]['counter'] < iteration_events:
                    # logging.info('Iteration with missed events: \n{0}'.format(iteration))
                    missed += iteration_events - b.loc[iteration]['counter']
            else:
                missed += iteration_events
        return missed

    @staticmethod
    def duplicated_event_count(a, iteration_events, iterations):
        #duplicated events
        a=a.reset_index()
        b = a.groupby(['current_iteration']).count()
        b.columns = ['counter']

        duplicated = 0
        for i in range(iterations):
            iteration = i + 1
            if iteration in b.index:
                if b.loc[iteration]['counter'] > iteration_events:
                    duplicated += b.loc[iteration]['counter'] - iteration_events

        return duplicated


    @staticmethod
    def succeeded_event_count(a, iteration_events, iterations):
        a=a.reset_index()
        b = a.groupby(['current_iteration']).count()
        b.columns = ['counter']

        succeeded = 0
        for i in range(iterations):
            iteration = i + 1
            if iteration in b.index:
                if b.loc[iteration]['counter'] < iteration_events:
                    succeeded += b.loc[iteration]['counter']
                else:
                    succeeded += iteration_events

        return succeeded

    @staticmethod
    def saveToCSV(data, file_name):
        """save data to a file in csv format"""
        data.to_csv(file_name, sep=',', index=True)

    @staticmethod
    def test_assert(condition, message):
        """
        Throws TestException with given message if condition is false.
        """
        if not condition:
            raise TestException(message)

    @staticmethod
    def fetch_csv_names(dirname):
        """gets csv file list from dirname"""
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            logging.error("No {} dir. Creating one. Drag files to analyze there".format(dirname))

        list_of_files=os.listdir(dirname)
        if '.keep' in list_of_files:
            list_of_files.remove('.keep')

        if len(list_of_files) == 0:
            logging.error("'todo' directory is empty and no other directory was specified as an argument")
            quit()

        return list_of_files

    @staticmethod
    def move_to_done():
        """moves csv files to results folders"""
        global OUTPUT

        files_to_move = Helper.fetch_csv_names('todo')
        for element in files_to_move:
            name = element.split('.')[0]
            try:
                shutil.move('todo/'+element,name+'_results/'+name)
                OUTPUT.to_csv(name+'_results/'+name+'_results.txt', sep=';')
            except OSError as e:
                logging.error("Couldn't move file from todo")

    @staticmethod ## //TODO documentation
    def cut_time_delimiters(data_input):
        """
        Cuts the input df to fit the timeframe specified by the user
        Returns: Dataframe populated with logs within the specified timeframe
        """
        fromDelimiter = input("input START day, month, year, hour and minutes in a day/month/year/hour/minute format \n (e.g. 15/12/2017/15/00)\n>")
        fromDelimiter = re.split("/", fromDelimiter)
        fD = fromDelimiter

        # constructs time obj from the input. Hardcoded, but works for now
        fromDelimiterStruct = time.mktime((int(fD[2]), int(fD[1]), int(fD[0]), int(fD[3]) + 1, int(fD[4]), 1, 1, 1, 0))
        fD = str(fromDelimiterStruct)[0:10]
        fD += "000"
        fromtime = int(fD)

        toDelimiter = input("input END day, month, year hour and minutes in day/month/year/hour/minute format \n>")
        tD = re.split("/", toDelimiter)
        toDelimiterStruct = time.mktime((int(tD[2]), int(tD[1]), int(tD[0]), int(tD[3]) + 1, int(tD[4]), 1, 1, 1, 0))
        tD = str(toDelimiterStruct)[0:10]
        tD += "000"
        stoptime = int(tD)

        #cuts the dataframe
        data_df = data_input.query('@fromtime <= unix_time <= @stoptime')
        for index, row in data_df.iterrows():
            if (row['device_id'] == 'UNKN_DEV' and (row['value'] == 'start')):
                # finds the first start of iteration after the specified 'start time' and cuts if there
                data_df = data_df.loc[index:]
                # flips the dataFrame and performs the same operation
                data_df = data_df[::-1]
                for index, row in data_df.iterrows():
                    if (row['device_id'] == 'UNKN_DEV' and  (row['value'] == 'stop')):
                        data_df = data_df.loc[index:]
                        # flips the dataFrame back to the original state
                        data_df = data_df[::-1]
                        break
                break
        return data_df

    @staticmethod
    def cut_iterations(data_input):
        """
        Returns: Dataframe  with iteration starting on 1, as after cutting a scenario log with Helper.cut_time_delimiters(),
        iterations will start not at 1
        """

        start_iteration = min(data_input['current_iteration'])
        data_input['current_iteration'] = data_input.apply(lambda row: int(row['current_iteration']) - (start_iteration- 1),
                                               axis='columns')
        return data_input




class Test_Result(object):

    def __init__(self, file, data, is_value_splitted):

        logging.info('Created Test_Result object for {0}'.format(file))
        self.file_name = file.split('.')[0] #remove csv extension
        self.results_directory = self._get_results_directory()
        self.data = data
        self.event_count = self._get_event_count()
        self.iterations = self._get_iterations_count()
        # TODO hardcoded - only works if there are two action/values per iteration
        self.values_count = 2 if is_value_splitted else 1
        self.events_per_iteration = self._get_events_per_iteration()
        self.wj_errors_count = self._get_wj_errors_count()
        self.validate()
        self.target_metrics = self._get_target_event_sources()

        self.report = None

    def _get_results_directory(self):
        directory = self.file_name + '_results'
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def _get_event_count(self):
        df_filtered = self.data[(self.data['source'] == 'BOT') & (self.data['value'].str.contains('start '))]
        event_count = len(df_filtered)
        logging.info('Event count for BOT \'start *\' commands: {0}'.format(event_count))
        return event_count

    def _get_iterations_count(self):
        iterations = int(self.data['current_iteration'].max())
        logging.info('Total iterations number: {0}'.format(iterations))
        return iterations

    def _get_wj_errors_count(self):
        errors = self.data.loc[self.data['source'] == 'WJ_ERROR']
        event_count = len(errors)
        logging.info('Total WJ_ERRORs count: {0}'.format(event_count))
        return event_count

    def _get_events_per_iteration(self):
        single_iteration = self.data.loc[(self.data['current_iteration'] == 1) & (self.data['value'].str.contains('start '))]

        events_per_iteration = int(len(single_iteration) / self.values_count)
        logging.info('Events per iteration: {0}'.format(events_per_iteration))
        return events_per_iteration

    def validate(self):
        Helper.test_assert(self.event_count == (self.events_per_iteration * self.iterations * self.values_count),
                'Total event count is not equal to events per iteration * number of iterations \
                Kindly remove partial results from last unfinished iteration!.')

    def _get_target_event_sources(self):
        df_filtered = self.data[self.data['latency'].notnull()]
        df_filtered = df_filtered[df_filtered['latency']!=0]
        df_filtered = df_filtered['source'].unique()
        source_list = df_filtered.tolist()
        source_list.remove('DEVICE')
        if 'COMMAND' in source_list:
            source_list.remove('COMMAND')
        if 'APP_COMMAND' in source_list:
            source_list.remove('APP_COMMAND')
            source_list.remove('APP_COMMAND_CLIENT')
        logging.info('Target event sources for metrics: {0}'.format(source_list))
        return source_list



class Data_Analyser(object):

    def __init__(self, files, is_value_splitted = True,path='todo/'):
        self.files_names = files
        self.test_result_list = []
        self.path = path
        self.aggregation_cols = ['source', 'device_id', 'device_name']
        if is_value_splitted:
            self.aggregation_cols.append('value')
        self.is_value_splitted = is_value_splitted
        logging.info(
            'Calculating metrics based on value: {0}'.format(self.is_value_splitted))
        self.import_csv_files_data()

    def import_csv_files_data(self):
        global ISSCENARIO
        global GOOGLEUPLOAD
        global OUTPUT
        for f in self.files_names:
            with open(self.path+f, "r") as file:

                '''
                determine if the current file is a scenario logfile or test logfile, and
                based on that, call Helper.cut_time_delimiters and Helper.cut_iterations.
                Determine if the user wants the results to be uploaded to BOT team googleSheets
                '''
                ISSCENARIO = input(
                    "################################\n Analyze in scenario mode - cut iterations, log selection by time ? \n (y/n)\n>")

                if ISSCENARIO =='y':
                    GOOGLEUPLOAD = input("upload the report to googleSheets ? \n (y/n)\n>")

                # Create pandas dataframe from csv
                try:
                    test_result_data = pd.read_csv(file, delimiter=';')
                except Exception as e:
                    raise Exception('Failed to read data from cvs-format file. Cause: {0}'.format(e))
                # drop last line as it contains test description json
                test_result_data = test_result_data[:-1]


                ## Cuts the report file - from and to - specified timepoints, cuts the iterations to start from 1
                if ISSCENARIO == 'y':
                    test_result_data = Helper.cut_time_delimiters(test_result_data)
                    test_result_data = Helper.cut_iterations(test_result_data)
                    OUTPUT = test_result_data
                test_result = Test_Result(f,test_result_data, self.is_value_splitted)
                self.test_result_list.append(test_result)

    def demo(self):
        for i, test_result in enumerate(self.test_result_list):
            df = test_result.data
            logging.info('{0}Display some demo for {1} file.{2}'.format('*'*7,self.files_names[i],'*'*7))
            # Display first rows
            logging.info('First 3 rows: \n{0}'.format(df.head(3)))

            df2 = df.loc[df['source'].str.contains('|'.join(test_result.target_metrics))]
            logging.info('First 3 rows with DEVICE_LATENCY as s source: \n{0}'.format(df2.head(3)))

    def analyze(self):
        global GOOGLEUPLOAD
        global ISSCENARIO
        for i, test_result in enumerate(self.test_result_list):
            df = test_result.data
            # Exports data.csv for elasticUpload.py, calculating and uploading missed events and latency to elasticsearch
            df.to_csv('data.csv', sep=';')
            report = test_result.report

            df_sourced = df.loc[df['source'].str.contains('|'.join(test_result.target_metrics))]
            logging.info('First 5 rows with metrics source: \n{0}'.format(df_sourced.head(5)))

            logging.info('Total event count: {0}'.format(test_result.event_count))
            report = pd.pivot_table(df_sourced, index=self.aggregation_cols, values=['latency'],
                                        aggfunc=[np.average,
                                                 np.std,
                                                 # np.median,
                                                 np.max,
                                                 np.size
                                                 #Helper.confidence_interval
                                                 ],
                                           margins=False)

            # logging.info('Latencies per device: \n{0}'.format(test_result.metrics))
            report.columns = [' '.join(col) for col in report.columns]
            report['average latency'] = np.round(report['average latency'],2)
            report['std latency'] = np.round(report['std latency'], 2)
            # report['median latency'] = report['median latency'].astype(int)
            report['amax latency'] = report['amax latency'].astype(int)
            report['size latency'] = report['size latency'].astype(int)

            report.rename(columns={'average latency': 'Avarege latency (ms)',
                                   'std latency': 'Std Dev (ms)',
                                   #'median latency': 'Median (ms)',
                                   'amax latency': 'Slowest Response (ms)',
                                   'size latency': 'All Events'
                                   }, inplace=True)

            report['Test Iterations'] = test_result.iterations
            columnsTitles = ['Avarege latency (ms)', 'Std Dev (ms)',
                             'Slowest Response (ms)', 'Test Iterations',
                             'All Events']
            report = report.reindex(columns=columnsTitles)


            report['Expected Events'] = int(test_result.event_count / test_result.values_count)

            succeeded_metrics = pd.pivot_table(df_sourced,
                                               index=self.aggregation_cols,
                                               values=['current_iteration'],
                                               aggfunc=[lambda x: Helper.succeeded_event_count(x,test_result.events_per_iteration,test_result.iterations)])
            report['Observed Events w/o duplicates'] = succeeded_metrics['<lambda>']
            report['Observed Events w/o duplicates'] = report['Observed Events w/o duplicates'].fillna(0).astype(int)

            missed_metrics = pd.pivot_table(df_sourced, index=self.aggregation_cols, values=['current_iteration'],
                                           aggfunc=[lambda x: Helper.missed_event_count(x,test_result.events_per_iteration,test_result.iterations)])
            report['Missed Events'] = missed_metrics['<lambda>']
            report['Missed Events'] = report['Missed Events'].fillna(0).astype(int)


            duplicated_metrics = pd.pivot_table(df_sourced, index=self.aggregation_cols, values=['current_iteration'],
                                           aggfunc=[lambda x: Helper.duplicated_event_count(x,test_result.events_per_iteration,test_result.iterations)])
            report['Duplicated Events'] = duplicated_metrics['<lambda>']
            report['Duplicated Events'] = report['Duplicated Events'].fillna(0).astype(int)

            report = report.rename(columns={'size': 'simple count'})

            report['Reliability'] = ((report['Observed Events w/o duplicates'] * test_result.values_count/ test_result.event_count) * 100).round(2)

            report['Wheeljack errors'] = test_result.wj_errors_count

            logging.info('\nEvent count per device: \n{0}'.format(report))
            logging.info('\nEvent count per device: \n{0}'.format(list(report)))
            logging.info('\nReport indexes: \n{0}'.format(list(report.index)))

            file_with_path = '{0}/{1}_table_stats.csv'.format(test_result.results_directory,
                                              test_result.file_name)



            logging.info('\ngoogleupload is : {0}'.format(GOOGLEUPLOAD))
            if GOOGLEUPLOAD =='y':
                report.to_csv('temp.csv', sep = ';')
                if (os.name == 'nt'):
                    os.system('python googleSheetUpdate.py')
                elif (os.name == 'posix' ):
                    os.system('python3 googleSheetUpdate.py')

            logging.info("######################################\nUPLOAD DONE\n###################################### ")

            #Helper.saveToCSV(OUTPUT, '{0}/{1}_time_cut.csv'.format(test_result.results_directory,
            #                                  test_result.file_name) )
            Helper.saveToCSV(report,
                             file_with_path)
            logging.info("######################################\nREPORT DONE\n###################################### ")


    def makePlots(self):
        for i, test_result in enumerate(self.test_result_list):
            df = test_result.data
            self.make_Bar_Plot(test_result = test_result, vals = 'latency')


    def make_Bar_Plot(self, test_result, vals):
        # table_avgs pivot table contains df data set average value of 'vals' calculated on 'index' column (1 column allowed)
        df = test_result.data
        target_metrics = test_result.target_metrics
        results_directory = test_result.results_directory
        logging.info('Making graphs for following metrics: {0}'.format(target_metrics))

        device_ids = df['device_id'].unique().tolist()
        device_ids.remove('UNKN_DEV')

        for device_id in device_ids:
            df2 = df.loc[df['device_id'] == device_id]
            file = self.get_png_file_name(df2, device_id)

            fig = plt.figure(figsize=(12, 9), facecolor='w', edgecolor='k')
            #fig.subplots_adjust(top=0.88)
            for metric in target_metrics:
                df3 = df2.loc[df2['source'].str.contains(metric)]
                if len(df3):
                    if self.is_value_splitted:

                        values = df3['value'].unique().tolist()
                        for i,value in enumerate(values):
                            subplot_id = 211 if i == 0 else 212
                            ax = fig.add_subplot(subplot_id)
                            df4 = df3.loc[df3['value'] == value]
                            # logging.info('Values: {0}'.format(values))
                            label = '{0},{1}'.format(metric,value)
                            ax.text(.5, .9, file.replace('_', ' '),
                                    horizontalalignment='center',
                                    transform=ax.transAxes)
                            ax.set_xlabel('Latency (ms)')
                            ax.set_ylabel('Count')
                            #ax.set_xlim((0, 500))
                            plt.hist(df4[vals], bins=1000, label=label, alpha = 0.7)

                            plt.legend()
                    else:
                        ax = fig.add_subplot(111)
                        plt.hist(df3[vals], bins=1000, label=metric, alpha = 0.7)
                        ax.text(.5, .9, file.replace('_', ' '),
                                horizontalalignment='center',
                                transform=ax.transAxes)
                        ax.set_xlabel('Latency (ms)')
                        ax.set_ylabel('Count')
                        plt.legend()


            #plt.grid()


            file_with_path = '{0}/{1}.png'.format(results_directory, file)
            #save or display
            plt.savefig(file_with_path)
            #plt.show()
            plt.close()

    def get_png_file_name(self, df, device_id):
        logging.info(device_id)
        df = df.loc[df['source'] == 'CLIENT']
        df2 = df.reset_index()
        device_name = df2.iloc[0]['device_name']
        device_id_part = device_id.split('-')[0]
        plot_file_name = '{0}_{1}'.format(device_name, device_id_part)
        plot_file_name = ''.join(c for c in plot_file_name if c not in '\/:*?"<>|')
        plot_file_name = plot_file_name.replace(' ', '_')
        logging.info('Device name: {0}'.format(plot_file_name))
        return plot_file_name


if __name__ == '__main__':


    logging.basicConfig(level=logging.INFO)

    no_of_args = len(sys.argv)-1

    if no_of_args > 1:
        """if there is more than 1 extra argument given, quit program"""
        logging.debug("{} Arguments given. Please provide just one argument"
                    .format(sys.argv))
        quit()

    elif no_of_args == 1:
        """if there is exactly one argument given, try to get csvs from there"""
        USER_PATH = sys.argv[1]

        if os.path.isdir(USER_PATH):
            analyzer = Data_Analyser(files=Helper.fetch_csv_names(USER_PATH),
                                    is_value_splitted=SPLITTING_ON_VALUES,
                                    path= USER_PATH+'/')
            logging.info("running on files from user-provided directory: {}"
                        .format(USER_PATH))
            analyzer.analyze()
            analyzer.makePlots()

        else:
            logging.error("Provided path is not a directory!")

    elif no_of_args == 0:
        """if there are no extra arguments, try to get files from todo"""

        logging.info("running analysis on the 'todo' directory")
        analyzer = Data_Analyser(files=Helper.fetch_csv_names('todo'),
                                is_value_splitted=SPLITTING_ON_VALUES)
        analyzer.analyze()
        analyzer.makePlots()
        Helper.move_to_done()


    else:
        logging.error("Cmd argument error")
