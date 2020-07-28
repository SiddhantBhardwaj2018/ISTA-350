from hw3 import *
import unittest, sys, io, os
from unittest.mock import patch
from contextlib import redirect_stdout, redirect_stderr

import warnings
warnings.filterwarnings("error")
'''
These tests depend on each other.  Must get them right one after another. 

Files needed:
hw3_init_in.txt, pout.txt, p1.txt, p2.txt, p3.txt
'''

# an example of monkey patching:
def equals(p1, p2):
    return p1.email == p2.email
    
Person.__eq__ = equals

class TestPerson(unittest.TestCase):
    def setUp(self):
        with patch('builtins.input', 
              side_effect=['Rich', 'Thompson', '5/21', 'rm@g']):
            self.p1 = Person()
        with patch('builtins.input', 
              side_effect=['Suse', '11/54', 'sb@g']):
            self.p2 = Person(last='Blues')
        with patch('builtins.input', 
              side_effect=['Warrant', '11/51']):
            self.p3 = Person('Pete', email='pw@g')
        self.p4 = Person('John', 'Doe', '9/51', 'jd@g')
        with patch('builtins.input', 
              side_effect=['', '']):
            self.p5 = Person('Randy', email='rmr@g')
        
    def test_init(self):
        self.assertEqual('Rich', self.p1.first)
        self.assertEqual('Thompson', self.p1.last)
        self.assertEqual('5/21', self.p1.bday)
        self.assertEqual( 'rm@g', self.p1.email)
        self.assertEqual('Suse', self.p2.first)
        self.assertEqual('Blues', self.p2.last)
        self.assertEqual('11/54', self.p2.bday)
        self.assertEqual('sb@g', self.p2.email)
        self.assertEqual('Pete', self.p3.first)
        self.assertEqual('Warrant', self.p3.last)
        self.assertEqual('11/51', self.p3.bday)
        self.assertEqual('pw@g', self.p3.email)
        self.assertEqual('John', self.p4.first)
        self.assertEqual('Doe', self.p4.last)
        self.assertEqual('9/51', self.p4.bday)
        self.assertEqual('jd@g', self.p4.email)
        self.assertEqual('Randy', self.p5.first)
        self.assertEqual('', self.p5.last)
        self.assertEqual('', self.p5.bday)
        self.assertEqual('rmr@g', self.p5.email)
         
        # test the prompts
        sys.stdin = open('hw3_init_in.txt')
        with io.StringIO() as buf, redirect_stdout(buf):
            p = Person()
            prompts = "Enter person's first name: Enter person's last name: " + \
                      "Enter person's birthday: Enter person's e-mail: "
            self.assertEqual(prompts, buf.getvalue())
        sys.stdin.close()
        sys.stdin = sys.__stdin__
        
    def test_repr(self):
        self.assertEqual('Rich Thompson: 5/21, rm@g', repr(self.p1))
        self.assertEqual('Suse Blues: 11/54, sb@g', repr(self.p2))
        self.assertEqual('Pete Warrant: 11/51, pw@g', repr(self.p3))
        self.assertEqual('John Doe: 9/51, jd@g', repr(self.p4))
        self.assertEqual('Randy : , rmr@g', repr(self.p5))
        
    def test_read_person(self):
        file = open('p1.txt', 'r')
        self.assertFalse(Person.read_person(file))
        file.close()
        file = open('p2.txt', 'r')
        p = Person.read_person(file)
        self.assertEqual('Rich Thompson: 5/21, rm@g', repr(p))
        self.assertFalse(Person.read_person(file))
        file.close()
        file = open('p3.txt', 'r')
        p = Person.read_person(file)
        self.assertEqual('Rich Thompson: 5/21, rm@g', repr(p))
        p = Person.read_person(file)
        self.assertEqual('Suse Blues: 11/54, sb@g', repr(p))
        self.assertFalse(Person.read_person(file))
        file.close()
    
    def test_write_person(self):
        file = open('pout.txt', 'w')
        self.p1.write_person(file)
        file.close()
        file = open('pout.txt', 'r')
        p = Person.read_person(file)
        self.assertEqual('Rich Thompson: 5/21, rm@g', repr(p))
        self.assertFalse(Person.read_person(file))
        file.close()
        file = open('pout.txt', 'w')
        self.p1.write_person(file)
        self.p2.write_person(file)
        file.close()
        file = open('pout.txt', 'r')
        p = Person.read_person(file)
        self.assertEqual('Rich Thompson: 5/21, rm@g', repr(p))
        p = Person.read_person(file)
        self.assertEqual('Suse Blues: 11/54, sb@g', repr(p))
        self.assertFalse(Person.read_person(file))
        file.close()
        
    def test_open_persons_db(self):
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        self.assertTrue(os.path.exists('persons.db'))
        c = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.assertEqual(['friends', 'colleagues'], [row['name'] for row in c])
        c = db.execute('SELECT * FROM friends;')
        self.assertEqual(['first', 'last', 'bday', 'email'], [f[0] for f in c.description])
        c = db.execute('PRAGMA TABLE_INFO("friends");')
        types = [row['type'] for row in c.fetchall()]
        self.assertEqual(['TEXT'] * 4, types)
        c = db.execute('SELECT * FROM colleagues')
        self.assertEqual(['first', 'last', 'bday', 'email'], [f[0] for f in c.description])
        c = db.execute('PRAGMA TABLE_INFO("colleagues");')
        types = [row['type'] for row in c.fetchall()]
        self.assertEqual(['TEXT'] * 4, types)
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        self.assertRaises(sqlite3.IntegrityError, db.execute, query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        self.assertRaises(sqlite3.IntegrityError, db.execute, query)
        db.commit()
        db.close()
        db = open_persons_db()
        c = db.execute('SELECT * FROM friends;')
        row = c.fetchone()
        self.assertEqual('Rocket', row['first'])
        self.assertEqual('Doggy', row['last'])
        self.assertEqual('doggy@happy.com', row['email'])
        self.assertEqual('6/8/2011', row['bday'])
        self.assertIsNone(c.fetchone())
        c = db.execute('SELECT * FROM colleagues;')
        row = c.fetchone()
        self.assertEqual('Rocket', row['first'])
        self.assertEqual('Doggy', row['last'])
        self.assertEqual('doggy@happy.com', row['email'])
        self.assertEqual('6/8/2011', row['bday'])
        self.assertIsNone(c.fetchone())
        db.close()
        
    def test_add_person(self):
        ''' Uses open_persons_db '''
        # self.p1 = 'Rich', 'Thompson', '5/21', 'rm@g'
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        with io.StringIO() as buf, redirect_stderr(buf):
            self.assertFalse(add_person(db, self.p1, friend=False))
            self.assertEqual('Warning: rm@g not added - must be friend or colleague\n', buf.getvalue())
        self.assertTrue(add_person(db, self.p1, colleague=True))
        c = db.execute('SELECT * FROM friends;')
        row = c.fetchone()
        self.assertEqual('Rich', row['first'])
        self.assertEqual('Thompson', row['last'])
        self.assertEqual('5/21', row['bday'])
        self.assertEqual('rm@g', row['email'])
        self.assertIsNone(c.fetchone())
        c = db.execute('SELECT * FROM colleagues;')
        row = c.fetchone()
        self.assertEqual('Rich', row['first'])
        self.assertEqual('Thompson', row['last'])
        self.assertEqual('5/21', row['bday'])
        self.assertEqual('rm@g', row['email'])
        self.assertIsNone(c.fetchone())
        
        # W/o placeholders, will inject executescript, break execute:
        # ------------ attack colleagues -----------------
        p = Person('a', 'b', 'c', "d');DROP TABLE colleagues;--")
        add_person(db, p)
        c = db.execute('SELECT * FROM friends;')
        row = c.fetchone()
        row = c.fetchone()
        self.assertEqual("d');DROP TABLE colleagues;--", row['email'])
        
        c.fetchone() # without this, something breaks badly
        
        p = Person('a', 'b', 'c', 'd");DROP TABLE colleagues;--')
        add_person(db, p)

        c = db.execute('SELECT * FROM friends;')
        row = c.fetchone()
        row = c.fetchone()
        row = c.fetchone()
        self.assertEqual('d");DROP TABLE colleagues;--', row['email'])

        # ----------------- Now attack friends ----------------
        
        p = Person('a', 'b', 'c', "d');DROP TABLE friends;--")
        add_person(db, p, friend=False, colleague=True)
        c = db.execute('SELECT * FROM colleagues;')
        row = c.fetchone()
        row = c.fetchone()
        self.assertEqual("d');DROP TABLE friends;--", row['email'])
        
        c.fetchone() # without this, something breaks badly
        
        p = Person('a', 'b', 'c', 'd");DROP TABLE friends;--')
        add_person(db, p, friend=False, colleague=True)

        c = db.execute('SELECT * FROM colleagues;')
        row = c.fetchone()
        row = c.fetchone()
        row = c.fetchone()
        self.assertEqual('d");DROP TABLE friends;--', row['email'])

        db.close()
        
    def test_delete_person(self):
        ''' Uses open_persons_db '''
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        p1 = Person("Rocket", "Doggy", "6/8/2011", "doggy@happy.com")
        p2 = Person("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com")
        p3 = Person("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com")
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com");'
        db.execute(query)
        db.commit()
        delete_person(db, p1)
        c = db.execute('SELECT * FROM friends;')
        self.assertEqual(1, len([row for row in c.fetchall()]))
        c = db.execute('SELECT * FROM colleagues;')
        self.assertEqual(1, len([row for row in c.fetchall()]))
        delete_person(db, p2)
        c = db.execute('SELECT * FROM friends;')
        self.assertEqual(0, len([row for row in c.fetchall()]))
        c = db.execute('SELECT * FROM colleagues;')
        self.assertEqual(1, len([row for row in c.fetchall()]))
        delete_person(db, p3)
        c = db.execute('SELECT * FROM friends;')
        self.assertEqual(0, len([row for row in c.fetchall()]))
        c = db.execute('SELECT * FROM colleagues;')
        self.assertEqual(0, len([row for row in c.fetchall()]))

        # W/o placeholders, will inject executescript, break execute:
        # ------------ attack colleagues -----------------
        p = Person('a', 'b', 'c', 'd";DROP TABLE colleagues;--')
        delete_person(db, p)
        p = Person('a', 'b', 'c', "d';DROP TABLE colleagues;--")
        delete_person(db, p)
        
        db.close()
        
    def test_to_Person_list(self):
        ''' Uses open_persons_db '''
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        p1 = Person("Rocket", "Doggy", "6/8/2011", "doggy@happy.com")
        p2 = Person("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com")
        p3 = Person("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com")
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com");'
        db.execute(query)
        db.commit()
        self.assertEqual([p1, p2, p3], to_Person_list(db.execute('SELECT * FROM friends')))
        db.close()
    
    def test_get_friends(self):
        ''' Uses open_persons_db '''
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        p1 = Person("Rocket", "Doggy", "6/8/2011", "doggy@happy.com")
        p2 = Person("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com")
        p3 = Person("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com")
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com");'
        db.execute(query)
        db.commit()
        self.assertEqual([p1, p2, p3], get_friends(db))
        db.close()
       
    def test_get_colleagues(self):
        ''' Uses open_persons_db '''
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        p1 = Person("Rocket", "Doggy", "6/8/2011", "doggy@happy.com")
        p2 = Person("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com")
        p3 = Person("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com")
        query = 'INSERT INTO colleagues (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com");'
        db.execute(query)
        db.commit()
        self.assertEqual([p1, p2, p3], get_colleagues(db))
        db.close()

    def test_get_all(self):
        ''' Uses open_persons_db '''
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        p1 = Person("Rocket", "Doggy", "6/8/2011", "doggy@happy.com")
        p2 = Person("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com")
        p3 = Person("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com")
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com");'
        db.execute(query)
        db.commit()
        friends_and_colleagues = get_all(db)
        self.assertEqual(3, len(friends_and_colleagues))
        self.assertIn(p1, friends_and_colleagues)
        self.assertIn(p2, friends_and_colleagues)
        self.assertIn(p3, friends_and_colleagues)
        db.close()
        
    def test_get_and(self):
        ''' Uses open_persons_db '''
        if os.path.exists('persons.db'):
            os.remove('persons.db')
        db = open_persons_db()
        p1 = Person("Rocket", "Doggy", "6/8/2011", "doggy@happy.com")
        p2 = Person("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com")
        p3 = Person("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com")
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO friends (first, last, bday, email) ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy2@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy@happy.com");'
        db.execute(query)
        query = 'INSERT INTO colleagues (first, last, bday, email)  ' + \
            'VALUES ("Rocket", "Doggy", "6/8/2011", "doggy3@happy.com");'
        db.execute(query)
        db.commit()
        friends_and_colleagues = get_and(db)
        self.assertEqual([p1], friends_and_colleagues)
        db.close()
        
if __name__ == "__main__":
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestPerson)
    results = unittest.TextTestRunner().run(test)
    tests_run = results.testsRun
    failures = len(results.failures)
    errors = len(results.errors)
    sys.stdout = sys.__stdout__
    print('Correctness score = ', str((tests_run - errors - failures) / tests_run * 100) + '%')
