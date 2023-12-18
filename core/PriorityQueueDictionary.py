# Hayden Feddock

import heapq

class PriorityQueueDictionary:
    def __init__(self) -> None:
        self.unique_id = 0 # Define a unique id value for dealing with conflicts in the priority queue
        self.priority_queue = [] # Use to hold items in priority queue
        self.dictionary = {} # Use to with key to get item

    def isempty(self):
        return len(self.dictionary) == 0
    
    # Push to the priority queue dictionary
    def push(self, key, item, priority):

        # Store the item at the key
        self.dictionary[key] = item
        
        # We are purposely not updating the exisiting (priority, key) pair and are instead just adding with the new pair
        # Since the priorities are likely different and we only really care about the min priority value then we can ignore
        # duplicates later when we are popping 
        heapq.heappush(self.priority_queue, (priority, self.unique_id, key))
        self.unique_id += 1

    # Pop the frontmost item from the priority queue
    def pop(self):
        
        # Get the priority and the key from the entry with the min priority value
        while self.priority_queue:
            _, _, key = heapq.heappop(self.priority_queue)

            # Check if there is a key-item pair in the dictionary, and if there is return the item and delete the pair
            if key in self.dictionary:
                item = self.dictionary[key]
                del self.dictionary[key]
                return item
            # If there is not a key-item pair, then it is possible that that it was already popped
            # Therefore this pair can discarded

        return None
        
    # Get the item at the key
    def get(self, key):
        if key in self.dictionary:
            return self.dictionary[key]
        else:
            return None
        
    # Support for "in" command
    def __contains__(self, key):
        return key in self.dictionary
    
    # Support for len() command
    def __len__(self):
        return len(self.dictionary)

        




        


