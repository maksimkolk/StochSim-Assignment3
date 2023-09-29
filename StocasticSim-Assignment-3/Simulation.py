from Customer import Customer
from FES import FES
from Event import Event
from PriorityQueue import PriorityQueue
from Results import Results
from collections import deque
from Server import Server
from Distribution2 import distribution_fd
import numpy as np
import matplotlib.pyplot as plt

#%%

distr = distribution_fd(moreCustomers=True) #set moreCustomers to False for the current/old situation, where it's not yet 20% more
def ServiceTime(location: str):
    """imported function from Distribution2. Samples a service time based on given location"""
    service_time = distr.sample_service(location)
    return service_time

def arrivaltime(t: float):
    """imported function from Distribution2. Samples next interarrival time based on current time"""
    time_converted = t + 34200 # because the function from Distribution2 has 9.30 am = 34200 sec and in the simulation 9.30 am = 0 sec
    arr_time = distr.sample_arrival(time_converted)
    return arr_time              

class Simulation:

    def __init__(self):
        self.locations = {'FWPM': 3, 'DcDdGpCh': 4, 'GrWcTEGs': 5, 'Rest': 6, 'Exit': 1, 'Entrance': 2}

    def checkServers(self, interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled):
        
        if len(interqueue[3]) >=1 and Rest.isAvailable(interqueue[3][0]) and not alreadyScheduled[4]: # We can serve a new customer at Rest
            c = interqueue[3].popleft()

            if c.location == 'Entrance':     # Remove c from the previous location
                Entrance.remove(c)
                Entrance.isnotHandled()
            elif c.location == 'FWPM':
                FWPM.remove(c)
            elif c.location == 'DcDdGpCh':
                DcDdGpCh.remove(c)
            elif c.location == 'GrWcTEGs':
                GrWcTEGs.remove(c)

            Rest.add(c)   # Add c to the server Rest
            c.updateLoc('Rest')
            location = c.trashtype.pop(0) # select next location
            eventType = self.locations[location] # select next eventtype
            event = Event(eventType, t + ServiceTime('Rest'), c, 'Rest')
            fes.add(event) 
            alreadyScheduled[4] = True

        if len(interqueue[2]) >=1 and GrWcTEGs.isAvailable(interqueue[2][0]) and not alreadyScheduled[3]: # We can serve a new customer at GrWcTEGs
            c = interqueue[2].popleft()

            if c.location == 'Entrance':     # Remove c from the previous location
                Entrance.remove(c)
                Entrance.isnotHandled()
            elif c.location == 'FWPM':
                FWPM.remove(c)
            elif c.location == 'DcDdGpCh':
                DcDdGpCh.remove(c)

            GrWcTEGs.add(c)   # Add c to the server GrWcTEGs
            c.updateLoc('GrWcTEGs')

            location = c.trashtype.pop(0) # select next location
            eventType = self.locations[location] # select next eventtype
            event = Event(eventType, t + ServiceTime('GrWcTEGs'), c, 'GrWcTEGs')
            fes.add(event) 
            alreadyScheduled[3] = True
        
        if len(interqueue[1]) >=1 and DcDdGpCh.isAvailable(interqueue[1][0]) and not alreadyScheduled[2]: # We can serve a new customer at DcDdGpCh
            c = interqueue[1].popleft()

            if c.location == 'Entrance':     # Remove c from the previous location
                Entrance.remove(c)
                Entrance.isnotHandled()
            elif c.location == 'FWPM':
                FWPM.remove(c)

            DcDdGpCh.add(c)   # Add c to the server DcDdGpCh
            c.updateLoc('DcDdGpCh')

            location = c.trashtype.pop(0) # select next location
            eventType = self.locations[location] # select next eventtype
            event = Event(eventType, t + ServiceTime('DcDdGpCh'), c, 'DcDdGpCh')
            fes.add(event) 
            alreadyScheduled[2] = True
        
        if len(interqueue[0]) >=1 and FWPM.isAvailable(interqueue[0][0]) and not alreadyScheduled[1]: # We can serve a new customer at FWPM
            c = interqueue[1].popleft()
            Entrance.remove(c)
            Entrance.isnotHandled()
            
            FWPM.add(c)   # Add c to the server DcDdGpCh
            c.updateLoc('FWPM')

            location = c.trashtype.pop(0) # select next location
            eventType = self.locations[location] # select next eventtype
            event = Event(eventType, t + ServiceTime('FWPM'), c, 'FWPM')
            fes.add(event) 
            alreadyScheduled[1] = True
        
        if not Entrance.isAvailable() and not Entrance.handled: # The entrance is occupied
            customer = Entrance.customer
            canContinue = True       # To determine whether the car can enter
            for location in customer.trashtype: 
                if location == 'FWPM' and not FWPM.isAvailable(customer):
                    canContinue = False
                elif location == 'DcDdGpCh' and not DcDdGpCh.isAvailable(customer):
                    canContinue = False
                elif location == 'GrWcTEGs' and not GrWcTEGs.isAvailable(customer):
                    canContinue = False
                elif location == 'Rest' and not Rest.isAvailable(customer):
                    canContinue = False

            if canContinue:
                location = customer.trashtype.pop(0)  # Select the location we need to go to next
                eventType = self.locations[location]    # Select the next event.
                event = Event(eventType, max(t, customer.arrivaltime + ServiceTime('Entrance')), customer, 'Entrance')  # Function Service time must still be created
                fes.add(event)
                Entrance.isHandled()
       

        if queue.size() >= 1 and Entrance.isAvailable() and not alreadyScheduled[0]: # We can serve a new customer at the Entrance
            c = queue.get(0)
            event = Event(Event.ENTRANCE, t, c, 'queue')
            fes.add(event) 
            alreadyScheduled[0] = True


    def simulate(self):
        Entrance = Server(1, True)  # Initailize servers, that keep track of occupied parking spots.
        FWPM = Server(4)
        DcDdGpCh = Server(4)
        GrWcTEGs = Server(3)
        Rest = Server(2)
        res = Results()
        
        interqueue = [deque() for _ in range(4)]  # [FWPM, DcDdGpCh, GrWcTEGs, Rest] // imaginary queues
        queue = PriorityQueue()     # Queue is empty at opening right now. 
        fes = FES()                 # Future Event Set
        t = 0                       # Current time (this is equivalent to 9.30) 

        lastQLengthChange = 0
        firstArrival= arrivaltime(t)
        #print(firstArrival)

        customer = Customer(firstArrival) # generate a customer
        customer.generateCust() # generate the properties of the customer
        if customer.impatience: # Schedule an impatience event
            impatientEvent = Event(Event.IMPATIENT, firstArrival+customer.impatience, customer)
            fes.add(impatientEvent)
        firstEvent = Event(Event.ARRIVAL, t + firstArrival, customer)
        opening = Event(Event.OPEN, 1800)
        fes.add(firstEvent) # add event to FES
        fes.add(opening)
        # Should not add the customer to the queue here, since we are not handling its event yet.
        
        while not fes.isEmpty():  # We run the simulation for 1 day
            
            e = fes.next()

            if t < e.time: 
                alreadyScheduled = [False, False, False, False, False]
                t = e.time         #queue,FWPM,DcDdGpCh,GrWcTEGs,Rest
            
            if e.type == Event.OPEN:
                #print('We are OPEN!!!')
                self.checkServers(interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled)

            if e.type == Event.ARRIVAL:
                #print(f'{e.customer}: at time {t} there arrives a {e.customer.vehicletype} with trash {e.customer.trashtype} ')
                duration = t - lastQLengthChange
                res.QLength(queue.size(), duration, False) # record queue length each time a customer arrives and save it
                lastQLengthChange = t
                queue.add(e.customer)   # Add the customer to the queue
                if queue.size() <= 1 and Entrance.isAvailable(e.customer):     # The customer is the only one in the queue, and can therefore be served directly if the Entrance is not occupied
                    event = Event(Event.ENTRANCE, t, e.customer, 'queue')  # Schedule event for start of the Entrance
                    fes.add(event)
                    alreadyScheduled[0] = True
                #### adding new arrival to the future event set    
                arrival = arrivaltime(t)
                if t + arrival < 16200: # The arrival is within opening hours.
                    customer = Customer(t + arrival) # generate a customer
                    customer.generateCust() # generate the properties of the customer
                    if customer.impatience: # Schedule an impatience event
                        impatientEvent = Event(Event.IMPATIENT, t + arrival + customer.impatience, customer)
                        fes.add(impatientEvent)
                    newEvent = Event(Event.ARRIVAL, t + arrival, customer)
                    fes.add(newEvent) # add event to FES
            
            elif e.type == Event.IMPATIENT:
                #print(f'time of impatient event = {t}')
                if e.customer.location == 'queue' and t < 16200:
                    queue.remove(e.customer)
                    #print(f'{e.customer}: at time {t}, left the queue because of impatience')
                    duration = t - lastQLengthChange
                    res.QLength(queue.size(), duration, False) # record queue length each time a customer leaves impatiently and save it
                    lastQLengthChange = t
                    
            
            elif e.type == Event.DEPARTURE:
                #print(f'{e.customer}: at time {t} there departs a {e.customer.vehicletype} with trash {e.customer.trashtype} ')

                res.TimeInTotal(e.customer.arrivaltime, t, False, e.customer.vehicletype)
    
                if e.prevLoc == 'Entrance':
                    Entrance.remove(e.customer)
                    Entrance.isnotHandled()
                elif e.prevLoc == 'FWPM':
                    FWPM.remove(e.customer)
                elif e.prevLoc == 'DcDdGpCh':
                    DcDdGpCh.remove(e.customer)
                elif e.prevLoc == 'GrWcTEGs':
                    GrWcTEGs.remove(e.customer)
                else: # e.prevLoc = 'Rest'
                    Rest.remove(e.customer)
                self.checkServers(interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled)

            elif e.type == Event.ENTRANCE:
                #print(f'{e.customer}: at time {t} there arrives at the ENTRANCE a {e.customer.vehicletype} with trash {e.customer.trashtype} ')
                queue.removeFirst() # equal to e.customer
                Entrance.add(e.customer) # Occupy the parking spot of the entrance
                e.customer.updateLoc('Entrance')
                if not e.customer.citypass: # Customer does not have a  city pass
                    e.customer.trashtype = ['Exit']
                    #print(f'{e.customer}: Forgot its citypass')
                    # By simply removing the trash from its list, the customer will be sent to the exit directly

                if 16200 >= t >= 1800: # Waste point is open
                    canContinue = True       # To determine wheter the car can enter
                    for location in e.customer.trashtype: 
                        if location == 'FWPM' and not FWPM.isAvailable(e.customer):
                            canContinue = False
                        elif location == 'DcDdGpCh' and not DcDdGpCh.isAvailable(e.customer):
                            canContinue = False
                        elif location == 'GrWcTEGs' and not GrWcTEGs.isAvailable(e.customer):
                            canContinue = False
                        elif location == 'Rest' and not Rest.isAvailable(e.customer):
                            canContinue = False
                elif t < 1800 and e.customer.citypass:  # The shop is not open 
                    canContinue = False
                elif t >=16200: # We are closed 16200 = 14.00
                    #print("WE ARE CLOSED")
                    canContinue = False
                    Entrance.remove(e.customer)
                    queue = PriorityQueue() # Reset the priority queue // send everybody home
                elif not e.customer.citypass:
                    canContinue = True # e.customer.citypass, such that someone without citypass can go home

                if canContinue:
                    res.EntranceWaitingtime(t, e.customer.arrivaltime, False) # register the waiting time for the entrance
                    location = e.customer.trashtype.pop(0)  # Select the location we need to go to next
                    eventType = self.locations[location]    # Select the next event.
                    event = Event(eventType, t + ServiceTime('Entrance'), e.customer, 'Entrance')  # Function Service time must still be created
                    fes.add(event)
                    Entrance.isHandled()
                else:
                    #print('WE CANT CONTINUE IMMEADITELY')
                    res.NumberOfBlockings(0) # count a blocking


                                    
            elif e.type == Event.FWPM:
                #print(f'{e.customer}: at time {t} there arrives at the FWPM a {e.customer.vehicletype} with trash {e.customer.trashtype} ')
                interqueue[0].append(e.customer) # Add the customer to the imaginary queue

                if FWPM.isAvailable(e.customer) and len(interqueue[0]) <= 1: # Customer can be served immediately
                    interqueue[0].remove(e.customer) # Remove the customer from the queue, since it is being served.
                    Entrance.remove(e.customer)      # Remove the customer from the previous server
                    Entrance.isnotHandled()
                    FWPM.add(e.customer)             # Add the customer to the new server
                    e.customer.updateLoc('FWPM')
                    self.checkServers(interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled) # Check wheter cars can move
                    
                    location = e.customer.trashtype.pop(0) # Select the location we need to go to next
                    eventType = self.locations[location] # Select the next event.
                    event = Event(eventType, t + ServiceTime('FWPM'), e.customer, 'FWPM')  
                    fes.add(event)  
                else:
                    res.NumberOfBlockings(1) # count a blocking
               

            elif e.type == Event.DcDdGpCh:
                #print(f'{e.customer}: at time {t} there arrives at the DcDdGpCh a {e.customer.vehicletype} with trash {e.customer.trashtype} ')
                interqueue[1].append(e.customer) # Add the customer to the imaginary queue
                if DcDdGpCh.isAvailable(e.customer) and len(interqueue[1]) <= 1: # Customer can be served immediately
                    interqueue[1].remove(e.customer) # Remove the customer from the imaginary queue
                    # Remove the customer from its previous location
                    if e.prevLoc == 'Entrance':
                        Entrance.remove(e.customer)
                        Entrance.isnotHandled()
                    else: # e.prevLoc == 'FWPM'
                        FWPM.remove(e.customer)
                    DcDdGpCh.add(e.customer) # add it to the new server
                    e.customer.updateLoc('DcDdGpCh')
                    self.checkServers(interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled) # Check wheter cars can move

                    location = e.customer.trashtype.pop(0) # Select the location we need to go to next
                    eventType = self.locations[location] # Select the next event.
                    event = Event(eventType, t + ServiceTime('DcDdGpCh'), e.customer, 'DcDdGpCh')  # Function Service time must still be created
                    fes.add(event)
                else:
                    res.NumberOfBlockings(2) # count a blocking
                   
            
            elif e.type == Event.GrWcTEGs:
                #print(f'{e.customer}: at time {t} there arrives at the GrWcTEGs a {e.customer.vehicletype} with trash {e.customer.trashtype} ')

                interqueue[2].append(e.customer) # Add the customer to the imaginary queue
                if GrWcTEGs.isAvailable(e.customer) and len(interqueue[2]) <= 1: # Customer can be served immediately
                    interqueue[2].remove(e.customer) # Remove the customer from the imaginary queue
                    # Remove the customer from its previous location
                    if e.prevLoc == 'Entrance': 
                        Entrance.remove(e.customer)
                        Entrance.isnotHandled()
                    elif e.prevLoc == 'FWPM':
                        FWPM.remove(e.customer)
                    else: # e.prevLoc == DcDdGpCh
                        DcDdGpCh.remove(e.customer)                   
                    GrWcTEGs.add(e.customer) # add it to the new server
                    e.customer.updateLoc('GrWcTEGs')
                    self.checkServers(interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled) # Check wheter cars can move

                    location = e.customer.trashtype.pop(0) # Select the location we need to go to next
                    eventType = self.locations[location] # Select the next event.
                    event = Event(eventType, t + ServiceTime('GrWcTEGs'), e.customer, 'GrWcTEGs')  # Function Service time must still be created
                    fes.add(event)
                else:
                    res.NumberOfBlockings(3) # count a blocking
        

            elif e.type == Event.Rest:
                #print(f'{e.customer}: at time {t} there arrives at the REST a {e.customer.vehicletype} with trash {e.customer.trashtype} ')

                interqueue[3].append(e.customer) # Add the customer to the imaginary queue
                if Rest.isAvailable(e.customer) and len(interqueue[3]) <= 1: # Customer can be served immediately
                    interqueue[3].remove(e.customer) # Remove the customer from the imaginary queue
                    # Remove the customer from its previous location
                    if e.prevLoc == 'Entrance':
                        Entrance.remove(e.customer)
                        Entrance.isnotHandled()
                    elif e.prevLoc == 'FWPM':
                        FWPM.remove(e.customer)
                    elif e.prevLoc == 'DcDdGpCh':
                        DcDdGpCh.remove(e.customer)
                    else: # e.prevLoc == GrWcTEGs
                        GrWcTEGs.remove(e.customer)     
                    Rest.add(e.customer) # add it to the new server
                    e.customer.updateLoc('Rest')
                    self.checkServers(interqueue, Entrance, FWPM, DcDdGpCh, GrWcTEGs, Rest, queue, t, fes, alreadyScheduled) # Check wheter cars can move

                    location = e.customer.trashtype.pop(0) # Select the location we need to go to next
                    eventType = self.locations[location] # Select the next event.
                    event = Event(eventType, t + ServiceTime('Rest'), e.customer, 'Rest')  # Function Service time must still be created
                    fes.add(event)
                else:
                    res.NumberOfBlockings(4) # count a blocking

        # simulation finished so we conclude the data
        res.BlockListHistogram() # save number of blockings  
        timeintotal, timeintotal_big, timeintotal_small = res.TimeInTotal(e.customer.arrivaltime, t, True, "big") # save time spent in total
        entrancewaitingtime = res.EntranceWaitingtime(e.customer.arrivaltime, t, True) # save entrance waiting time
        print(f"average time in the wrp was {timeintotal-entrancewaitingtime}")
        res.QLength(queue.size(), 0, True) # save queue lengths
        return res




sim = Simulation()

# We determine confidence intervals for:
meanQLength = []
averageTotalTime = []
averageTotalTimeBig = []
averageTotalTimeSmall = []
averageWTentrance = []
averagenrOfBlockings = []
blockingsEntrance = []
blockingsFWPM = []
blockingsDcDdGpCh = []
blockingsGrWcTEGs = []
blockingsRest = []

n =10000
for i in range(n): # Number of runs to determine confidence interval
    print('i',i)
    res = sim.simulate()
    meanQLength.append(res.meanQLength)
    averageTotalTime.append(res.averageTotalTime)
    averageTotalTimeBig.append(res.averageTotalTimeBig)
    averageTotalTimeSmall.append(res.averageTotalTimeSmall)
    averageWTentrance.append(res.averageWTentrance)
    averagenrOfBlockings.append(sum(res.BlockList))
    blockingsEntrance.append(res.BlockList[0])
    blockingsFWPM.append(res.BlockList[1])
    blockingsDcDdGpCh.append(res.BlockList[2])
    blockingsGrWcTEGs.append(res.BlockList[3])
    blockingsRest.append(res.BlockList[4])


# Printing confidence intervals
print(f'mean queue length: {np.mean(meanQLength)} +- {np.std(meanQLength)/ np.sqrt(n)}')
print(f'mean TotalTime: {np.mean(averageTotalTime)} +- {np.std(averageTotalTime)/ np.sqrt(n)}')
print(f'mean TotalTimeBig: {np.mean(averageTotalTimeBig)} +- {np.std(averageTotalTimeBig)/ np.sqrt(n)}')
print(f'mean TotalTimeSmall: {np.mean(averageTotalTimeSmall)} +- {np.std(averageTotalTimeSmall)/ np.sqrt(n)}')
print(f'mean Waiting time entrance: {np.mean(averageWTentrance)} +- {np.std(averageWTentrance)/ np.sqrt(n)}')
print(f'mean nr of total blockings: {np.mean(averagenrOfBlockings)} +- {np.std(averagenrOfBlockings)/ np.sqrt(n)}')
print(f'mean nr of entrance blockings: {np.mean(blockingsEntrance)} +- {np.std(blockingsEntrance)/ np.sqrt(n)}')
print(f'mean nr of FWPM blockings: {np.mean(blockingsFWPM)} +- {np.std(blockingsFWPM)/ np.sqrt(n)}')
print(f'mean nr of DcDdGpCh blockings: {np.mean(blockingsDcDdGpCh)} +- {np.std(blockingsDcDdGpCh)/ np.sqrt(n)}')
print(f'mean nr of GrWcTEGs blockings: {np.mean(blockingsGrWcTEGs)} +- {np.std(blockingsGrWcTEGs)/ np.sqrt(n)}')
print(f'mean nr of Rest blockings: {np.mean(blockingsRest)} +- {np.std(blockingsRest)/ np.sqrt(n)}')


# Make plot of mean nr of blockings
hist_data = {'Entrance': np.mean(blockingsEntrance), 'FWPM': np.mean(blockingsFWPM), 'DcDdGpCh': np.mean(blockingsDcDdGpCh), 'GrWcTEGs': np.mean(blockingsGrWcTEGs), 'Rest': np.mean(blockingsRest)}
plt.figure()
plt.bar(hist_data.keys(), hist_data.values())
# plt.savefig('Hist of mean blockings.pdf') ### uncomment to save the plot
plt.show()


# Make another plot yay
# I know this is not the proper way to get data but I forgot to save them before and doing 10000 runs takes too long. I did copy paste the results into a txt document so I'm using those values now.
x_old = [51.8139, 0, 1.8194, 4.4566, 2.3862]
x_new = [64.3688, 0, 2.2827, 5.2585, 2.8232]
stations = ['Entrance', 'FWPM', 'DcDdGpCh', 'GrWcTEGs', 'Rest']

X_axis = np.arange(len(stations))

plt.bar(X_axis - 0.2, x_old, 0.4, label = "Current situation")
plt.bar(X_axis + 0.2, x_new, 0.4, label = "More customers")

plt.xticks(X_axis, stations)
plt.ylabel("Average number of blockings")
plt.legend(["Current situation", "More customers"])
#plt.savefig('Comparison.pdf')
plt.show()

x_gr = [65.9762, 0, 2.6174, 1.5047, 3.6366]
x_all = [49.666, 0, 1.7585, 4.0843, 1.6505]

plt.bar(X_axis - 0.3, x_old, 0.2, label = "Old situation")
plt.bar(X_axis - 0.1, x_new, 0.2, label = "No changes")
plt.bar(X_axis + 0.1, x_all, 0.2, label = "One more spot at each station")
plt.bar(X_axis + 0.3, x_gr, 0.2, label = "Two more spots at GrWcTEGs")
plt.xticks(X_axis, stations)
plt.ylabel("Average number of blockings")
plt.legend(["Old situation", "No changes", "One more spot at each station", "Two more spots at GrWcTEGs"])
plt.savefig('Comparison2.pdf')
plt.show()

