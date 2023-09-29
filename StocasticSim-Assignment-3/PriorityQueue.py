import heapq

class PriorityQueue:
    
    def __init__(self):
        ''' 
        Creates an instance of a priority queue.
        Initially, the queue contains no customers.
        '''
        self.customers = []  # internally we use a heapq, which is the most efficient data structure for this purpose
        
    def add(self, customer):
        ''' 
        Adds a customer to this queue, inserting it at the correct location based on their ordering/priority level.
        
        Parameters:
            customer: a customer object
        '''
        heapq.heappush(self.customers, customer)
        
    def removeFirst(self):
        ''' 
        Removes (and returns) the customer at the front of the queue.
        
        Returns:
            the customer object at position 0
        '''
        return heapq.heappop(self.customers)
    
    def remove(self, customer):
        ''' 
        Removes the specified customer from the queue.
        
        Parameters:
            customer: a customer object
        '''
        self.customers.remove(customer)          # you can use it like any other list,
        heapq.heapify(self.customers)            # but then you need to re-heapify.
        
    def removeAt(self, index):
        ''' 
        Removes the customer at the specified index/position from the queue.
        Position 0 corresponds to the front of the queue.
        
        Parameters:
            index: the index/position where to remove a customer
        '''
        self.customers = sorted(self.customers)
        self.customers[index] = self.customers[-1]
        self.customers.pop()
        heapq.heapify(self.customers)            # but then you need to re-heapify.
        
    def position(self, customer):
        ''' 
        Returns the position of the specified customer in the queue.
        
        Returns:
            the index/position of the specified customer
        '''
        return sorted(self.customers).index(customer)
    
    def get(self, index):
        ''' 
        Returns the customer at the specified index in the queue.
        
        Returns:
            the customer object at the specified position 
        '''
        
        return heapq.nsmallest(index + 1, self.customers)[-1] 
        
    def size(self):
        ''' 
        Returns the number of customers in the queue (i.e., the queue length)
        
        Returns:
            the queue length
        '''
        return len(self.customers)
    
    def __str__(self):
        s = ''
        for c in sorted(self.customers):
            s += str(c) + '\n'
        return s
