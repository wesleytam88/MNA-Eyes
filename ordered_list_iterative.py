class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class'''
        dummy = Node(None)
        dummy.next = dummy
        dummy.prev = dummy
        self.head = dummy
        self.length = 0


    def size(self):
        '''Returns number of items in the OrderedList
           MUST have O(n) performance'''
        return self.length

        
    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.length <= 0


    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head of list) to highest (at tail of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance. MUST only use the < operator to compare items'''
        if self.search(item):
            return False
        current = self.head.next
        while current != self.head and current.item < item:
            current = current.next
        n = Node(item)
        n.next = current
        n.prev = current.prev
        current.prev.next = n
        current.prev = n
        self.length += 1
        return True


    def remove(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
           returns the item.  If item was not removed (was not in the list) returns None
           MUST have O(n) average-case performance'''
        if not self.search(item):
            return None
        current = self.head.next
        while current.item != item:
            current = current.next
        current.prev.next = current.next
        current.next.prev = current.prev
        self.length -= 1
        return current.item


    def get_item(self, indx):
        '''Returns the item at index indx'''
        current = self.head.next
        if indx >= self.size():
            raise IndexError
        for i in range(0, indx):
            current = current.next
            i += 1
        return current.item


    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance'''
        index = 0
        current = self.head.next
        while current != self.head:
            if current.item == item:
                return index
            else:
                current = current.next
                index += 1
        return None


    def pop(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance'''
        if index < 0 or index >= self.size():
            raise IndexError
        current = self.head.next
        i = 0
        while i != index:
            current = current.next
            i += 1
        item = current.item
        current.prev.next = current.next
        current.next.prev = current.prev
        self.length -= 1
        return item


    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           MUST have O(n) average-case performance'''
        if self.is_empty():
            return False
        current = self.head
        for i in range(self.size()):
            current = current.next
            if current.item == item:
                return True
        return False


    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        orderedList = []
        if self.is_empty():
            return orderedList
        current = self.head.next
        while current != self.head:
            orderedList.append(current.item)
            current = current.next
        return orderedList


    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           MUST have O(n) performance'''
        revList = self.python_list()
        revList.reverse()
        return revList

    def clear(self):
        '''Clears the ordered list of all nodes except for dummy node'''
        while self.length > 0:
            self.pop(0)
        return True