class Event:

    ARRIVAL = 0
    DEPARTURE = 1
    ENTRANCE = 2
    FWPM = 3
    DcDdGpCh = 4
    GrWcTEGs = 5
    Rest = 6
    OPEN = 7
    IMPATIENT = 8
    
    def __init__(self, typ, time, cust = None, prevLoc = None):  # type is a reserved word
        self.type = typ
        self.time = time
        self.customer = cust
        self.prevLoc = prevLoc
        
    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        for self.type in range(0,7):
            s = ('queue', 'exit', 'Entrance', 'FWPM', 'DcDdGpCh', 'GrWcTEGs', 'Rest')
            return 'Arrival at ' + s[self.type] + " of customer " + str(self.customer) + ' at t = ' + str(self.time)
        else:
            return 'OPENING'
    
