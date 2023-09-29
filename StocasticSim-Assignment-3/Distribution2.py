import math
from Distribution import Distribution
from Data_distributions import Data_dist
import scipy.stats as stats


class distribution_fd:
    
    def __init__(self, moreCustomers=False):
        
        
        data = Data_dist()
        if moreCustomers: # 20 % more customers
            for car in data.cars_per_hour.keys():
                rate = data.cars_per_hour.get(car) * 1.2
                data.cars_per_hour[car] = rate
        # needs lists of random nrs for: interarrival at time t, service time at location
        # First the interarrival times
        mean_930 = data.cars_per_hour.get('34200')
        self.arr_930 = Distribution(stats.expon(scale = 3600/mean_930))
        mean_10 = data.cars_per_hour.get('36000')
        self.arr_10 = Distribution(stats.expon(scale = 3600/mean_10))
        mean_11 = data.cars_per_hour.get('39600')
        self.arr_11 = Distribution(stats.expon(scale = 3600/mean_11))
        mean_12 = data.cars_per_hour.get('43200')
        self.arr_12 = Distribution(stats.expon(scale = 3600/mean_12))
        mean_13 = data.cars_per_hour.get('46800')
        self.arr_13 = Distribution(stats.expon(scale = 3600/mean_13))
        mean_14 = data.cars_per_hour.get('50400')
        self.arr_14 = Distribution(stats.expon(scale = 100000))
        
        self.distributions_arr = {930: self.arr_930,
                              10: self.arr_10,
                              11: self.arr_11,
                              12: self.arr_12,
                              13: self.arr_13,
                              14: self.arr_14}
        
        # now the service times
        self.servtime_Entrance = Distribution(stats.gamma(data.mean.get('Entrance')**2/data.stdev.get('Entrance')**2, scale=data.stdev.get('Entrance')**2/data.mean.get('Entrance')))
        self.servtime_FWPM = Distribution(stats.gamma(data.mean.get('FWPM')**2/data.stdev.get('FWPM')**2, scale=data.stdev.get('FWPM')**2/data.mean.get('FWPM')))
        self.servtime_DcDdGpCh = Distribution(stats.gamma(data.mean.get('DcDdGpCh')**2/data.stdev.get('DcDdGpCh')**2, scale=data.stdev.get('DcDdGpCh')**2/data.mean.get('DcDdGpCh')))
        self.servtime_GrWcTEGs = Distribution(stats.gamma(data.mean.get('GrWcTEGs')**2/data.stdev.get('GrWcTEGs')**2, scale=data.stdev.get('GrWcTEGs')**2/data.mean.get('GrWcTEGs')))
        self.servtime_Rest = Distribution(stats.gamma(data.mean.get('Rest')**2/data.stdev.get('Rest')**2, scale=data.stdev.get('Rest')**2/data.mean.get('Rest')))

        self.distributions_serv = {'Entrance': self.servtime_Entrance,
                                   'FWPM': self.servtime_FWPM,
                                   'DcDdGpCh': self.servtime_DcDdGpCh,
                                   'GrWcTEGs': self.servtime_GrWcTEGs,
                                   'Rest': self.servtime_Rest}
        
    def sample_arrival(self, t):
        """ Given the current time in seconds of the day (so 10am is 36000), samples
        an interarrival time at the entrance gate"""
        
        # For now, given time must be between 9:30 and 14:00 for the function to work.
        # Might need to adjust this to just plan no arrivals outside of those times
        assert t >= 34200, "time must be at least 34200 (9:30)"
        assert t < 50400, "time must be less than 50400 (14:00)"
        if math.floor(t/1800)/2 == 9.5: # a time is sampled between 9:30 and 10:00
            inter_arr = self.arr_930.rvs()
            if t + inter_arr >= 36000: # if the car arrives in the next hour, the time needs to be resampled
                time_after = self.arr_10.rvs()
                inter_arr = time_after + (36000 - t)
        else: # a time is sampled between 10:00 and 15:00
            hour = math.floor(t/3600) # the beginning of the hour that we sample in
            inter_arr = self.distributions_arr.get(hour).rvs()
            if t + inter_arr >= hour * 3600 + 3600: # car arrives in the next hour so we need to resample
                time_after = self.distributions_arr.get(hour + 1).rvs()
                inter_arr = time_after + (hour*3600 + 3600 - t)
        return inter_arr
    
    def sample_service(self, location):
        """ Given the location (garbage type or entrance), samples a service
        time at the given location. """
        service_time = -1
        while service_time < 0:
            service_time = self.distributions_serv.get(location).rvs()
        return service_time
        