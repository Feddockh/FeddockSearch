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

    # Peek from the front of the priority queue
    def peek(self, i = 0):

        # Check for valid indicies
        if i < 0 or i >= len(self.priority_queue):
            return None
        
        # Return the next item, if there is one
        j = i
        while(j < len(self.priority_queue)):
                
            # Get the key from the priority queue
            _, _, key = self.priority_queue[j]

            # Get the item from the dictionary using the key
            if key in self.dictionary:
                return self.dictionary[key]

            # If the key is not in the dictionary then the key-item pair must've been removed, remove the element from the priority queue
            else:
                self.priority_queue.pop(j)

            # Increment the index to the next value in the priority queue
            j += 1

        return None
    
    # Slice from the front of the priority queue
    def slice(self, i = 0, j = 1):

        # Check for valid indicies
        if i < 0 or i >= len(self.priority_queue):
            return None
        if j < 0 or j >= len(self.priority_queue):
            j = len(self.priority_queue)
        if j <= i:
            j = i + 1
        
        # Return list of items
        items = []
        k = i
        while(i < j and k < len(self.priority_queue)):
                
            # Get the key from the priority queue
            _, _, key = self.priority_queue[k]

            # Get the item from the dictionary using the key
            if key in self.dictionary:
                items.append(self.dictionary[key])
                i += 1

            # If the key is not in the dictionary then the key-item pair must've been removed, remove the element from the priority queue
            else:
                self.priority_queue.pop(k)
            
            # Increment the index to the next value in the priority queue
            k += 1

        return items

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

        




        


