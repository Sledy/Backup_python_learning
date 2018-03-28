import datetime


class DifferenceBetweenDates():

    def __init__(self):
        pass

    @staticmethod
    def check_diffrerence():
        begin = datetime.datetime(1901, 1, 1)
        end = datetime.datetime(2000, 12, 1)
        delta = datetime.timedelta(days=1)
        # flag - determines the amount of days the month has
        count = 0

        while begin <= end:
            begin += delta
            if begin.day == 1 and begin.isoweekday() == 7:
                count += 1

        print(count)


DifferenceBetweenDates().check_diffrerence()
