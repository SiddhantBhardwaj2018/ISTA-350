from lab2 import *
import unittest, io
from contextlib import redirect_stdout

class TestFunctions(unittest.TestCase):
    
    def test_init_Node(self):
        n = Node()
        self.assertEqual(None, n.datum)
        self.assertEqual(None, n.next)
        self.assertEqual(['__weakref__', 'datum', 'next'], dir(n)[-3:])
        n = Node(100)
        self.assertEqual(100, n.datum)
        self.assertEqual(None, n.next)
        self.assertEqual(['__weakref__', 'datum', 'next'], dir(n)[-3:])
        
    def test_init_LinkedList(self):
        ll = LinkedList()
        self.assertEqual(None, ll.head)
        self.assertEqual(['__weakref__', 'append', 'head', 'insert', 
            'pop', 'remove', 'to_list'], dir(ll)[-7:])
        
    def test_to_list(self):
        ll = LinkedList()
        self.assertEqual([], ll.to_list())
        ll.head = Node()
        self.assertEqual([None], ll.to_list())
        ll.head.datum = 100
        self.assertEqual([100], ll.to_list())
        ll.head.next = Node(101)
        self.assertEqual([100, 101], ll.to_list())
        temp = ll.head
        ll.head = Node(102)
        ll.head.next = temp
        self.assertEqual([102, 100, 101], ll.to_list())
        
    def test_append(self):
        ll = LinkedList()
        ll.append(200)
        self.assertEqual([200], ll.to_list())
        ll.append(201)
        self.assertEqual([200, 201], ll.to_list())
        ll.append(202)
        self.assertEqual([200, 201, 202], ll.to_list())
        
    def test_remove(self):
        ll = LinkedList()
        ll.append(200)
        ll.append(201)
        ll.append(202)
        ll.append(203)
        ll.append(204)
        self.assertEqual([200, 201, 202, 203, 204], ll.to_list())
        ll.remove(204)
        self.assertEqual([200, 201, 202, 203], ll.to_list())
        ll.remove(202)
        self.assertEqual([200, 201, 203], ll.to_list())
        ll.remove(200)
        self.assertEqual([201, 203], ll.to_list())
        
    def test_insert(self):
        ll = LinkedList()
        ll.insert(0, 200)
        self.assertEqual([200], ll.to_list())
        
        ll = LinkedList()
        ll.insert(10, 200)
        self.assertEqual([200], ll.to_list())
        ll.insert(0, 201)
        self.assertEqual([201, 200], ll.to_list())
        
        ll = LinkedList()
        ll.insert(10, 200)
        self.assertEqual([200], ll.to_list())
        ll.insert(1, 201)
        self.assertEqual([200, 201], ll.to_list())
        
        ll = LinkedList()
        ll.insert(10, 200)
        self.assertEqual([200], ll.to_list())
        ll.insert(10, 201)
        self.assertEqual([200, 201], ll.to_list())
        ll.insert(0, 202)
        self.assertEqual([202, 200, 201], ll.to_list())
        ll.insert(1, 203)
        self.assertEqual([202, 203, 200, 201], ll.to_list())
        ll.insert(3, 204)
        self.assertEqual([202, 203, 200, 204, 201], ll.to_list())
        ll.insert(10, 205)
        self.assertEqual([202, 203, 200, 204, 201, 205], 
            ll.to_list())
        ll.insert(0, 205)
        self.assertEqual([205, 202, 203, 200, 204, 201, 205], 
            ll.to_list())
        ll.insert(2, 206)
        self.assertEqual([205, 202, 206, 203, 200, 204, 201, 205], 
            ll.to_list())
            
    def test_pop(self):
        ll = LinkedList()
        
        with self.assertRaises(IndexError): # using kwarg msg doesn't help
            with io.StringIO() as buf, redirect_stdout(buf):
                ll.pop()
                self.assertEqual('pop from empty list', buf.getvalue())
                
        ll.insert(10, 200)
        with self.assertRaises(IndexError): # using kwarg msg doesn't help
            with io.StringIO() as buf, redirect_stdout(buf):
                ll.pop(1)
                self.assertEqual('pop index out of range', buf.getvalue())
        self.assertEqual(200, ll.pop(0))
        self.assertEqual([], ll.to_list())
        
        ll.insert(10, 201)
        ll.insert(0, 202)
        self.assertEqual([202, 201], ll.to_list())
        self.assertEqual(202, ll.pop(0))
        
        ll.insert(0, 202)
        self.assertEqual(201, ll.pop(1))
        self.assertEqual([202], ll.to_list())
        
        ll.insert(0, 201)
        self.assertEqual(202, ll.pop())
        self.assertEqual([201], ll.to_list())
            
        ll.insert(0, 202)
        ll.insert(0, 200)
        self.assertEqual(201, ll.pop())
        self.assertEqual([200, 202], ll.to_list())
        ll.insert(10, 201)
        self.assertEqual(201, ll.pop(2))
        self.assertEqual([200, 202], ll.to_list())
        ll.insert(0, 201)
        self.assertEqual(201, ll.pop(0))
        self.assertEqual([200, 202], ll.to_list())
        ll.insert(1, 201)
        self.assertEqual(201, ll.pop(1))
        self.assertEqual([200, 202], ll.to_list())
 
if __name__ == "__main__":
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFunctions)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')

