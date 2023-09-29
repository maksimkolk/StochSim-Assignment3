import pandas as pd

class Data_dist:
    """Reads the data from the first sheet of the cleaned excel file. Then contains
    all required info from that, like cars per hour for each hour, opening time."""

    def __init__(self):
        
        # import excel file
        df = pd.read_excel('CleanData.xlsx', header=None, sheet_name="Arrival and service processes")
                
        # import opening time
        opening = df.iloc[6,1]
        t = str(opening)
        (h, m, s) = t.split(':')
        self.opening = int(h) * 3600 + int(m) * 60 + int(s)
        
        # get cars per hour (for fixed hours)
        self.cars_per_hour = dict()
        for i in range(1,7):
            hour = str(df.iloc[9,i])
            (h, m, s) = hour.split(':')
            hour_converted = int(h) * 3600 + int(m) * 60 + int(s)
            self.cars_per_hour[str(hour_converted)] = df.iloc[10,i]
        
        # get mean and stdev of service times for each station
        self.mean = dict()
        self.stdev = dict()
        for i in range(5):
            garbage_type = df.iloc[19+i,0]
            self.mean[str(garbage_type)] = df.iloc[19+i,1]
            self.stdev[str(garbage_type)] = df.iloc[19+i,2]
        