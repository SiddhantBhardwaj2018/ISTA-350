'''
Name - Siddhant Bhardwaj
Section Leader - Gwen Hopper
ISTA 350 HW3
Date - 2/22/2020
Collaborators - Vibhor Mehta
'''
import os,sqlite3,sys

class Person:
    def __init__(self,first = '',last = '',bday = '',email = ''):
        '''
        This instance method takes 4 parameters - first,last,bday and email
        and sets them by default to ''. If new parameters are not given, then 
        the an input statement asks for values for the instance variables corresponding
        to the parameters.
        '''
        self.first = first if first != '' else input("Enter person's first name: ")
        self.last = last if last != '' else input("Enter person's last name: ")
        self.bday = bday if bday != '' else input("Enter person's birthday: ")
        self.email = email if email != '' else input("Enter person's e-mail: ")
        
    def __repr__(self):
        '''
        This instance method returns a string comprising of all the instance variables
        corresponding to the first name,last name,birthday and email address of the person.
        '''
        return(self.first + ' ' + self.last + ': ' + self.bday + ', ' + self.email)
    
    @classmethod    
    def read_person(cls,file_obj):
        '''
        This is a class method and reads from a file object the first name,last name,
        birthday and email of a person.
        '''
        first = file_obj.readline().strip()
        if not first:
            return False
        last = file_obj.readline().strip()
        bday = file_obj.readline().strip()
        email = file_obj.readline().strip()
        return cls(first,last,bday,email)
        
    def write_person(self,file_object):
        '''
        This instance method writes to a file object the first name,
        last name,birthday and email of a Person.
        '''
        file_object.write(self.first + '\n')
        file_object.write(self.last + '\n')
        file_object.write(self.bday + '\n')
        file_object.write(self.email + '\n')
        
        
def open_persons_db():
    '''
    This function checks if persons.db file exists and creates a connection and sets the row_factory to sqlite3.Row.
    It checks the length of the database to see if it is empty and if empty, then creates 2 tables,friends and 
    colleagues with first,last,bday and email as columns with email as primary key.
    '''
    exists = os.path.exists('persons.db')
    conn = sqlite3.connect('persons.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    result = c.fetchall()
    if len(result) == 0:
        c.execute('CREATE TABLE IF NOT EXISTS friends (first TEXT,last TEXT, bday TEXT,email TEXT PRIMARY KEY)')
        c.execute('CREATE TABLE IF NOT EXISTS colleagues (first TEXT, last TEXT,bday TEXT,email TEXT PRIMARY KEY)')
    return conn   
    
def add_person(person_db,Person,friend = True,colleague = False):
    '''
    This function adds a person to the person_db database.It takes 4 arguments - person_db connection,
    Person class,bool object friend set to True and bool object colleague set to False.If both bool objects are False,
    then print a warning statement that the person must be friend or colleague. Else if friend is True, then insert the person
    into friends table and if colleague is True, then insert the person into the colleagues table.
    '''
    c = person_db.cursor()
    if friend == False and colleague == False:
        print('Warning: ' + Person.email + ' not added - must be friend or colleague',file = sys.stderr)
    else:
        if friend == True:
            c.execute("INSERT INTO friends values(?,?,?,?)",(Person.first,Person.last,Person.bday,Person.email))
        if colleague == True:
            c.execute("INSERT INTO colleagues values(?,?,?,?)",(Person.first,Person.last,Person.bday,Person.email))
            
        person_db.commit()
        return True
   
def delete_person(person_db,Person):
    '''
    This function deletes a person from all tables in a database.
    '''
    c = person_db.cursor()
    c.execute("DELETE FROM friends WHERE email = (?)",(Person.email,))
    c.execute("DELETE FROM colleagues WHERE email = (?)",(Person.email,))
    
def to_Person_list(cursor1):
    '''
    This function takes a cursor object and appends to a list all Persons whose data is in the database.
    '''
    lst = []
    for row in cursor1:
        lst.append(Person(row['first'],row['last'],row['bday'],row['email']))
    return lst

def get_friends(person_db):
    '''
    This function returns a list of all persons from the friends table in the database.
    '''
    c = person_db.cursor()
    q = "SELECT * FROM friends"
    return(to_Person_list(c.execute(q)))
        
    
def get_colleagues(person_db):
    '''
    This function returns a list of all persons from the colleagues table in the database.
    '''
    c = person_db.cursor()
    q = "SELECT * FROM colleagues"
    return(to_Person_list(c.execute(q)))
    
def get_all(person_db):
    '''
    This function returns all unique individuals from the 2 tables in the database.
    '''
    c = person_db.cursor()
    q = "SELECT * FROM friends UNION SELECT * FROM colleagues"
    return(to_Person_list(c.execute(q)))
    
def get_and(person_db):
    '''
    This function returns a list of all persons who are both present in the friends and colleagues in the
    database.
    '''
    c = person_db.cursor()
    q = "SELECT * FROM friends INTERSECT SELECT * FROM colleagues"
    return(to_Person_list(c.execute(q)))