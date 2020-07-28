'''
Name - Siddhant Bhardwaj
Section Leader - Gwen Hopper
ISTA 350 HW2
Date - 1/27/2020
Collaborators - Vibhor Mehta
'''
import re
class Node:
    def __init__(self,item = None):
        '''
        This magic method takes an argument item which defaults to None
        which is then put to the instance variable datum and initializes
        an instance variable children to an empty list.
        '''
        self.datum = item
        self.children = []
        
    def get_child(self,key = None):
        '''
        This method checks if a key is presence in the datum of a Node 
        in the instance variable children and returns the Node if present
        else returns None.
        '''
        for i in self.children:
            if i.datum == key:
                return i 
        return None
        
    def __eq__(self,other):
        '''
        The data comparison happens in get_child.
        This is strictly a helper method.
        '''
        if len(self.children) != len(other.children):
            return False
        if not self.children:
            return True
        equal = True
        for child in self.children:
            other_child = other.get_child(child.datum)
            if not other_child:
                return False
            equal = equal and child == other_child
        return equal
        
class WatchListLinked:
    def __init__(self,fname = ""):
        '''
        This magic method sets an instance variable root to a node of 5
        children with each denomination being a child and if the file name
        is given, then inserts each bill number to the watchlistlinked class.
        '''
        self.root = Node() 
        self.root.children = [Node('5'),Node('10'),Node('20'),Node('50'),Node('100')]
        self.validator = re.compile(r'^[A-M][A-L](?!00000000)\d{8}(?!O)(?!Z)[A-Z]$')
        if fname:
            with open(fname,'r') as file:
                text = file.read().splitlines()
                for line in text:
                    line = line.split(' ')
                    self.insert(line[0],line[1])                
        
    def insert(self,serial_num,denom):
        '''
        This method inserts the bill number into the watchlistlinked.
        '''
        current = self.root.get_child(denom)
        for ch in serial_num:
            if not current.get_child(ch):
                current.children.append(Node(ch))
            current = current.get_child(ch)
        if not current.get_child():
            current.children.append(Node())
        
    def search(self,serial_num,denom):
        '''
        This method checks if a bill number is in the watchlistlinked.
        '''
        current = self.root.get_child(denom)
        for ch in serial_num:
            if not current.get_child(ch):
               return False
            current = current.get_child(ch)
        if current.get_child(None):
           return True
            
                
        
        
class WatchListDict:
    def __init__(self,fname = ""):
        '''
        This magic method initializes a root variable to a dictionary with each 
        denomination being a key to an empty dictionary.
        '''
        self.root = {'5':{},'10':{},'20':{},'50':{},'100':{}}
        self.validator = re.compile(r'^[A-M][A-L](?!00000000)\d{8}(?!O)(?!Z)[A-Z]$')
        if fname:
            with open(fname,'r') as file:
                text = file.read().splitlines()
                for line in text:
                    line = line.split(' ')
                    self.insert(line[0],line[1])
        
    def insert(self,serial_num,denom):
        '''
        This method adds a serial number to the watchlistDict.
        '''
        current = self.root[denom]
        for ch in serial_num:
            if ch not in current:
                current[ch] = {}            
            current = current[ch]
        if None not in current:
            current[None] =  None
                
                
    def search(self,serial_num,denom):
        '''
        This method searches a serial number to the watchlistDict.
        '''
        current = self.root[denom]
        for ch in serial_num:
            if ch not in current:
                return False
            current = current[ch]
        if None in current:
            return True
        

def check_bills(class1,fname):
    '''
    This function checks if a bill is a bad bill and appends it to 
    a list and returns it.
    '''
    lst = []
    with open(fname,'r') as file:
        text = file.read().splitlines()
        for line in text:
            line1= line.split(' ')
            if not class1.validator.match(line1[0]):
                lst.append(line)
            if class1.search(line1[0],line1[1]):
                lst.append(line)
    return lst
            