import numpy as np
from Customer import Customer

class Server:

    def __init__(self, nrParkinspots, entrance = False) -> None:
        self.nrParkingspots = nrParkinspots
        self.occupied = 0
        self.entrance = entrance
        self.customer = 'no customer'
        self.handled = False


    def isAvailable(self, customer = Customer(None, 'small')):
        if customer.vehicletype == 'small' or self.entrance == True :
            return self.occupied < self.nrParkingspots
        elif customer.vehicletype == 'big':
            return self.nrParkingspots - self.occupied >= 2
        elif customer.vehicletype == 'pedestrian':
            return True
        
    def add(self, customer):
        if customer.vehicletype == 'small' or self.entrance:
            self.occupied += 1
        elif customer.vehicletype == 'big':
            self.occupied += 2

        if self.entrance:
            self.customer = customer 

    def remove(self, customer):
        if customer.vehicletype == 'small' or self.entrance == True:
            self.occupied -= 1
        elif customer.vehicletype == 'big':
            self.occupied -= 2
        
        if self.entrance:
            self.customer = 'no customer'

    def isHandled(self):
        self.handled = True

    def isnotHandled(self):
        self.handled = False