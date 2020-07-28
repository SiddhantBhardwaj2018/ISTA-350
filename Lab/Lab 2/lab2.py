"""
Linked Lists and While Loops

A Node object will always evaluate to 
True when used as a Boolean expression.
Therefore, if node.next is pointing at a
Node object, node.next will evaluate to True
when used as a condition.

There is no terminal node on the list.  The
list just ends when a node with next == None
is reached.
"""

class Node:
    def __init__(self, datum=None):
        self.datum = datum
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None

    def to_list(self):
        """
        Returns linked list as a regular list.
        Can be used to print what's in your linked list use for debugging!
        """
        lst = []
        current = self.head
        while current:
            lst.append(current.datum)
            current = current.next
        return lst

    #Implement the methods below

    def append(self, datum):
        """
        This method appends a new node to the end of your linked list
        with datum as its datum.
        If there's nothing in the linked list (self.head = None), set the
        head to the new node and return.
        """
        new_node = Node(datum)
        if self.head is None:
            self.head = new_node
        else:
            last = self.head
            while (last.next):
                last = last.next
            last.next = new_node
        return new_node            
             
    def remove(self, datum):
        """
        Remove the first occurrence of element x from the list.
        If it isn't in the list, raise the ValueError with message
        'list.remove(x): x not in list'
        """
        if self.head is None:
            raise ValueError('list.remove(x): x not in list')
        current = self.head
        if current.datum == datum:
            self.head = current.next
            return
        while current.next:
            if current.next.datum != datum:
                current = current.next
            else:
                current.next = current.next.next
                return 
        
        if current.next is None:
            raise ValueError('list.remove(x): x not in list')
            
                 
    def insert(self, i, datum):
        """
        Insert a new node at position i with datum as its datum.
        If i >= len(list), insert at the end.
        """
        tracker = 1
        current = self.head
        

    def pop(self, i = None):
        """
        Remove the node at position i and return its datum.
        If the list is empty, raise an IndexError with the message
        'pop from empty list'.  If i >= len(list), raise an 
        IndexError with the message 'pop index out of range'.
        """
        pass




