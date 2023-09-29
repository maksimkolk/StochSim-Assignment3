from numpy import random
from Data import Data
import numpy as np
rng = random.default_rng()


class Customer:
    #Customer classes and corresponding matrices (Not all matrices are written down / can probably be imported more easily)
    data = Data()   # Class containing all needed matrices
    FPC = 0     # Flammable, Paper, Clothes
    FWM = 1     # Flammable, Wood, Metal
    F = 2       # Flammable
    FP = 3      # FLammable, Paper
    FCPE = 4    # Flammable, Chemical, Paper, Electronis
    G = 5       # Green
    FWCP = 6    # Flammable, Wood, Chemical, Paper
    W = 7       # Wood
    WC = 8      # Wood, Carpet
    D = 9       # Debris
    FWMMPE = 10 # Flammable, Wood, Metal, Mattress, Paper, Electronics

    def __init__(self, arrivaltime, vehicletype = 'small', impatience = None, pcitypass = 0.9, location = 'queue'):
        self.vehicletype = vehicletype  # Possible types are big, small, pedestrian
        self.arrivaltime = arrivaltime
        self.trashtype = []      # List of trash types, can contain FWPM, DcDdGpCh, GrWcTEGs and Rest
        self.impatience = impatience
        self.customerClass = None
        self.location = location
        if rng.uniform(0,1) < pcitypass:
            self.citypass = True
        else:
            self.citypass = False



    def __str__(self):
        return f'Customer {self.arrivaltime}'  #"Customer at " + str(self.arrivaltime)  + " in " + str(self.vehicletype) + " disposing of " + str(self.trashtype) + " of class " + str(self.customerClass)

    def __lt__(self, other):
        if self.vehicletype == "pedestrian" and other.vehicletype != "pedestrian":
            return True
        elif self.vehicletype != "pedestrian" and other.vehicletype == "pedestrian":
            return False
        else: # self.vehicletype == other.vehicletype
            return self.arrivaltime < other.arrivaltime

    def generateCust(self):
        """Generate the vehicletype, the trashtype and the impatience of the customer."""
        prob = rng.uniform(0,1)
        if prob < 0.5: # 50% small, 48% big, 2% pedestrian.
            self.vehicletype = 'small'
        elif 0.5 <= prob < 0.98:
            self.vehicletype =  'big'
        else:
            self.vehicletype = 'pedestrian'

        self.customerClass = rng.choice(range(11),1,p=[2/152,23/152,27/152,24/152,5/152,18/152,4/152,27/152,4/152,16/152,2/152]) # Weights are determined from datasheet
        self.customerClass = self.customerClass[0]
        matrix = Customer.data.getMatrix(self.customerClass)
        location = 'Gate'

        while location != 'Exit':
            #Determining the next stop, based on the probability matrix
            location = rng.choice(['FWPM', 'DcDdGpCh', 'GrWcTEGs', 'Rest', 'Exit'], 1, p=np.asarray(matrix[Customer.data.getLocation(location)][1:], dtype='float64'))
            location = location[0]
            self.trashtype.append(location)

        # generating impatience
        # 10% of customers are impatient
        if rng.uniform(0,1) < 0.1:   
            self.impatience = rng.uniform(30,300) # impatience between half minute and 5 minutes
        else:                         
            self.impatience = False

    def updateLoc(self,location):
        """Update the location of the customer"""
        self.location = location

c = Customer(6)
c.generateCust()
c.trashtype

data = Data()
data.getLocation('DcDdGpCh')
