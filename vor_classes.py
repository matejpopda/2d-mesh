import heapq
import itertools

class Point:
   x = 0.0
   y = 0.0
   
   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.edges = list()

class Edge:
    start = None
    end = None
    done = False
    
    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False
        self.start.edges.append(self) 

    def finish(self, p):
        if self.done: return
        self.end = p
        self.done = True 
        self.end.edges.append(self)  

class Arc:
    p = None
    pprev = None
    pnext = None
    edge = None
    s0 = None
    s1 = None
    
    def __init__(self, p, a=None, b=None):
        self.p = p
        self.pprev = a
        self.pnext = b
        self.edge = None
        self.s0 = None
        self.s1 = None

class Event:
    x = 0.0
    p = None
    a = None
    valid = True
    
    def __init__(self, x, p, a):
        self.x = x
        self.p = p
        self.a = a
        self.valid = True

class PriorityQueue:
    def __init__(self):
        self.heap = [] 
        self.entry_map = {}  
        self.unique_counter = itertools.count()  

    def empty(self):
        """Return true if the priority queue is empty."""
        return not self.heap
    
    def push(self, item):
        """Add an item to the priority queue."""
        if item in self.entry_map:
            return  # Avoid duplicates
        count = next(self.unique_counter)
        entry = [item.x, count, item]
        self.entry_map[item] = entry
        heapq.heappush(self.heap, entry)

    def remove_entry(self, item):
        """Mark an existing item as removed."""
        entry = self.entry_map.pop(item)
        entry[-1] = 'Removed'

    def top(self):
        """Return the lowest priority item without removing it."""
        while self.heap:
            _, _, item = heapq.heappop(self.heap)
            if item is not 'Removed':
                del self.entry_map[item]
                self.push(item)  # Reinsert 
                return item
            
    def pop(self):
        """Remove and return the lowest priority item."""
        while self.heap:
            _, _, item = heapq.heappop(self.heap)
            if item is not 'Removed':
                del self.entry_map[item]
                return item

    

    
            
