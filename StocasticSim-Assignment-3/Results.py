from collections import deque

from numpy.ma.core import zeros, sqrt

import matplotlib.pyplot as plt

import numpy as np


class Results:
        
    def __init__(self):
        self.EntranceSum = 0
        self.EntranceCounter = 0

        self.BlockCounter = 0
        self.BlockList = zeros(5) # 0:gate 1:FWPM 2:DcDdGpCh 3:GrWcTEGs 4:rest

        self.TotalTimeCounter = 0
        self.TotalTimeSum = 0
        self.big_TotalTimeCounter = 0
        self.big_TotalTimeSum = 0
        self.small_TotalTimeCounter = 0
        self.small_TotalTimeSum = 0
        
        self.nr_impatients = 0

        self.QLengthList = [0]

        self.QLengthWeights = []
        self.QLengthTimestamps = [0]
    
        self.QCounter = 0
        self.QSum = 0

        ### FINAL RESULTS ###
        self.meanQLength = None
        self.averageTotalTime = None
        self.averageTotalTimeBig = None
        self.averageTotalTimeSmall = None
        self.averageWTentrance = None
    
    
    def QLength(self, length, duration, done):
        if done==True:
            self.QLengthWeights.append(0) #since we always record the duration of the previous Q length, the last length needs a duration as well.
            self.meanQLength = np.average(self.QLengthList,weights=self.QLengthWeights) # computes time average of Q length
            print(f"average queue length is {self.meanQLength}")
            ### uncomment the following lines to make a plot of the daily pattern
            # plt.plot(self.QLengthTimestamps,self.QLengthList)
            # plt.title("Daily pattern of the queue length for the WRP")
            # plt.ylabel("Queue length")
            # plt.xlabel("Time")
            # plt.savefig('Daily pattern Q length.pdf')
            # plt.show()
        self.QSum += length
        self.QCounter += 1
        self.QLengthList.append(length)
        self.QLengthWeights.append(duration)
        self.QLengthTimestamps.append(self.QLengthTimestamps[-1]+duration)
        
    def AddImpatient(self):
        """ Records the number of customers that left due to impatience. """
        self.nr_impatients += 1
        
    def NumberOfImpatients(self):
        """ Returns the number of customers that left due to impatience. """
        return self.nr_impatients
        
    def NumberOfBlockings(self, index): 
        self.BlockList[index] += 1

    def BlockListHistogram(self, verbose=False):
        print(self.BlockList)
        index = range(len(self.BlockList))
        categories = ['gate', 'FWPM', 'DcDdGpCh', 'GrWcTEGs', 'rest']
        if verbose:
            plt.bar(index, self.BlockList)
            plt.xlabel('Station')
            plt.ylabel('Number of blockings')
            plt.xticks(index, categories)
            plt.show()

    def TimeInTotal(self, start, end, done, vehtype):
        if done==True:
            self.averageTotalTime = self.TotalTimeSum/self.TotalTimeCounter
            self.averageTotalTimeBig = self.big_TotalTimeSum/self.big_TotalTimeCounter
            self.averageTotalTimeSmall = self.small_TotalTimeSum/self.small_TotalTimeCounter
            print(f"average total time was {self.averageTotalTime} for general, {self.averageTotalTimeBig} for big vehicles, {self.averageTotalTimeSmall} for small vehicles")
            return self.TotalTimeSum/self.TotalTimeCounter, self.big_TotalTimeSum/self.big_TotalTimeCounter, self.small_TotalTimeSum/self.small_TotalTimeCounter

        # general
        totaltime = end - start
        self.TotalTimeSum += totaltime
        self.TotalTimeCounter += 1

        # big
        if vehtype == "big":
            big_totaltime = end - start
            self.big_TotalTimeSum += big_totaltime
            self.big_TotalTimeCounter += 1
            
        # small
        elif vehtype == "small":
            small_totaltime = end - start
            self.small_TotalTimeSum += small_totaltime
            self.small_TotalTimeCounter += 1
        
    def EntranceWaitingtime(self, enter, arrival, done):
        if done==True:
            self.averageWTentrance = self.EntranceSum/self.EntranceCounter
            print(f"average waiting time for the entrance was {self.averageWTentrance}")
            return self.averageWTentrance
        time = enter - arrival
        self.EntranceSum += time     
        self.EntranceCounter += 1   
        

    