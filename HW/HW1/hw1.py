'''
Name - Siddhant Bhardwaj
Section Leader - Gwen Hopper
ISTA 350 HW1
Date - 1/27/2020
Collaborator - Vibhor Mehta
'''
import re, bisect
class WatchList:
  def __init__(self,file = ""):
    '''
    This method takes in a filename and initializes a dictionary by the name 
    of bills which contains serial numbers of all the denominations contained 
    as keys.It also checks if the lists in the keys of bills are sorted and 
    uses regex module to check for valid serial numbers.
    '''
    self.file = file
    self.bills = {'5': [], '10': [], '20': [], '50': [], '100': []}
    if len(self.file) != 0:
            with open(self.file,'r') as f:
                text = f.read().splitlines()
                for line in text:
                    if line.split(' ')[1] == '5':
                       self.bills['5'].append(line.split(' ')[0])
                    elif line.split(' ')[1] == '10':
                       self.bills['10'].append(line.split(' ')[0])
                    elif line.split(' ')[1] == '20':
                       self.bills['20'].append(line.split(' ')[0])
                    elif line.split(' ')[1] == '50':
                       self.bills['50'].append(line.split(' ')[0])
                    else:
                       self.bills['100'].append(line.split(' ')[0])
    if len(self.file) != 0:
        self.is_sorted = False
    else:
        self.is_sorted = True
    self.validator = re.compile(r'^[A-M][A-L](?!00000000)\d{8}(?!O)(?!Z)[A-Z]$')
    
  def insert(self,string):
       '''
       This method appends to the correct list in the key of the dictionary
       which matches with its denomination. If the lists in the bills 
       dictionary are sorted, then, it appends to them in a sorted fashion
       otherwise, it just appends to them.
       '''
       lst = string.split(' ')
       if self.file == "":
            if self.is_sorted == True:
               if lst[0] not in self.bills[lst[1]]:
                    bisect.insort_right(self.bills[lst[1]],lst[0])
            else:
                if lst[0] not in self.bills[lst[1]]:
                    self.bills[lst[1]].append(lst[0])     
       else:
            if lst[0] not in self.bills[lst[1]]:
               self.bills[lst[1]].append(lst[0])
               
  def sort_bills(self):
      '''
      This method sorts all lists the dictionary bills.
      '''
      for i in self.bills:
          self.bills[i].sort()
      self.is_sorted = True
      
  def linear_search(self,bill_str):
      '''
      This method performs a linear search in the dictionary list whose key
      matches its denomination and and returns True if it is there else 
      it returns False.
      '''
      bill_details = bill_str.split(' ')
      if bill_details[1] in self.bills:
         if bill_details[0] in self.bills[bill_details[1]]:
            return True
      return False
    
  def binary_search(self,bill_str):
      '''
      This method performs performs a binary search in the dictionary list whose key
      matches its denomination and and returns True if it is there else 
      it returns False.
      '''
      bill2 = bill_str.split(' ')
      i = 0
      j = len(self.bills[bill2[1]]) - 1
      while i <= j:
            mid = (i + j) // 2
            if self.bills[bill2[1]][mid] == bill2[0]:
                return True
            elif bill2[0] < self.bills[bill2[1]][mid]:
                j = mid - 1
            else:
                i = mid + 1
      return False
      
  
                        
  def check_bills(self,fname,bool1 = False):
    '''
    This method checks if the bill details in a given file are valid and appends 
    them to a list of bad serial numbers if they are bad. 
    '''
    lst = []
    if bool1:
        with open(fname,'r') as file:
            text = file.read().splitlines()
            for line in text:
                z = line.split(' ')
                self.sort_bills()
                if self.binary_search(line):
                    lst.append(line.rstrip())
                if self.validator.match(z[0]) == None:
                    lst.append(line.rstrip())
                    
    else:
        with open(fname,'r') as file:
            text = file.read().splitlines()
            for line in text:
                z = line.split(' ')
                if z[0] in self.bills[z[1]]:
                   lst.append(line.rstrip())
                if self.validator.match(z[0]) == None:
                    lst.append(line.rstrip())
    return(lst)