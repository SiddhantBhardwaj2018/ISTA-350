
class Binary:

    def is_square(self):
        """
        Return True if self represents the square of an integer.
        """
        one = Binary('01')
        count = Binary() # zero at this point
        if self < count:
            return False
        while count <= self:
            if count * count == self:
                return True
            count += one
        return False
        
    def is_square2(self):
        one = Binary('01')
        count = Binary()
        if self < count:
            return False
        while True:
            square = count * count
            if square == self:
                return True
            if square > self:
                return False
            count += one

class LinkedList:

    def prepend(self, datum):
        """
        In addition to lab, do not post.  For practice on the
        final review worksheet.
        """
        self.head, self.head.next = Node(datum), self.head
         
    @classmethod
    def from_list(cls, item_lst):
        """
        In addition to lab, do not post.  For practice on the
        final review worksheet.
        """
        ll = cls()
        for item in item_lst:
            ll.append(item)
        return ll

ll = LinkedList.from_list([3, 8, 10])

class Node:

    def __contains__(self, item):
        if self.datum == item:
            return True
        if item < self.datum:
            if self.left:
                return item in self.left
            return False
        if self.right: # item > self.datum
            return item in self.right
        return False # self.right is None
                
class BST:

    def __contains__(self, item):
        if self.root:
            return item in self.root
        return False

import requests
from bs4 import BeautifulSoup         
def get_table_soup(url, table_num):
    r = requests.get(url)
    tables = BeautifulSoup(r.content, features='lxml').find_all('table')
    if table_num >= len(tables):
        return
    return tables[table_num]
    
def get_speed(category):
    if category < 0 or category > 5:
        raise IndexError('Bad category number: Fujita scale numbers run 0 to 5')
    url = "https://www.iii.org/fact-statistic/facts-statistics-tornadoes-and-thunderstorms"
    table = get_table_soup(url, 0)
    trs = table.tr.find_all('tr')[2:] 
    # there are tr's inside the first tr!!  The ones we need!!  Hence, table.tr.find_all
    return trs[category].find_all('td')[2].get_text()
    
print(get_speed(0))
print(get_speed(3))
print(get_speed(5))
print(get_speed(6))
    



