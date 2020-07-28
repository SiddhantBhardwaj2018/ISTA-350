from hw2 import Node, WatchListLinked, WatchListDict, check_bills
import unittest, pickle

'''
Files needed:
hw2.py
bill_file_0.txt, bill_file_1.txt, bill_file_5.txt, 
bill_file_77.txt, bill_file_100.txt 
bill_file_0_wll.pkl, bill_file_1_wll.pkl, bill_file_5_wll.pkl, 
bill_file_77_wll.pkl, bill_file_100_wll.pkl
bill_file_77_wld.pkl
recovered_bills.txt
'''

"""
Many of these tests depend upon other tests.  
If Node isn't right, kod.
"""

'''
Illustrated below are two techniques for adding a method to an existing
class in Python.  The first is inheritance, the classic approach.  It is
commented out.  Following that is monkey patching, cool Python!
Google python monkey patch to learn more.
'''

"""
class WLTester(WatchListLinked):
    def __eq__(self, other):
        if len(self.root.children) != 5 or len(other.root.children) != 5:
            return False
        equal = True
        for denomination in ['5', '10', '20', '50', '100']:
            child = self.root.get_child(denomination)
            if not child:
                return False
            other_child = other.root.get_child(denomination)
            equal = equal and child == other_child
        return equal
"""   
     
def mp_eq(self, other):
    if len(self.root.children) != 5 or len(other.root.children) != 5:
        return False
    equal = True
    for denomination in ['5', '10', '20', '50', '100']:
        child = self.root.get_child(denomination)
        if not child:
            return False
        other_child = other.root.get_child(denomination)
        equal = equal and child == other_child
    return equal
   
WatchListLinked.__eq__ = mp_eq

WLTester = WatchListLinked # goes with monkey patch, comment out if using inheritance

class TestClasses(unittest.TestCase):
    def test_init_Node(self):
        n = Node()
        self.assertEqual(None, n.datum)
        self.assertEqual([], n.children)
        self.assertEqual(['__weakref__', 'children', 'datum', 'get_child'], dir(n)[-4:])
        n = Node('10')
        self.assertEqual('10', n.datum)
        self.assertEqual([], n.children)
        self.assertEqual(['__weakref__', 'children', 'datum', 'get_child'], dir(n)[-4:])
     
    def test_get_child(self):
        n = Node('a')
        n.children.extend([Node('b'), Node('c')])
        self.assertEqual(Node('b'), n.get_child('b'))
        self.assertEqual(Node('c'), n.get_child('c'))
        self.assertIsNone(n.get_child('d'))
        n.children[1].children.append(Node('d'))
        self.assertIsNone(n.get_child('d'))
        self.assertEqual(Node('d'), n.get_child('c').get_child('d'))
        n.children.append(Node())
        self.assertEqual(Node(None), n.get_child())
    
    def test_init_WatchListLinked(self):
        correct = Node()
        correct.children = [Node('5'), Node('10'), Node('20'), 
                              Node('50'), Node('100')]
        wl = WatchListLinked()
        self.assertEqual(correct, wl.root)
        self.assertIsNone(wl.root.datum)
        self.assertTrue(wl.validator.match('CF35365625U'))
        self.assertEqual(['__weakref__', 'insert', 'root', 'search', 'validator'],
                         dir(wl)[-5:])
                         
        fives = correct.children[0]
        fives.children.append(Node('a'))
        a = fives.children[0]
        a.children.append(Node('b'))
        b = a.children[0]
        b.children.extend([Node('e'), Node('c')])
        b.children[0].children.append(Node('f'))
        b.children[0].children[0].children.append(Node())
        c = b.children[1]
        c.children.extend([Node(), Node('d'), Node('e')])
        d = c.children[1]
        d.children.extend([Node(), Node('e')])
        d.children[1].children.append(Node())
        c.children[2].children.append(Node())
        wl = WatchListLinked('bill_file_5.txt')
        self.assertEqual(correct, wl.root)
        
        correct = pickle.load(open('bill_file_77_wll.pkl', 'rb'))
        wl = WLTester('bill_file_77.txt')
        self.assertEqual(correct, wl)
        
        correct = pickle.load(open('bill_file_0_wll.pkl', 'rb'))
        wl = WLTester('bill_file_0.txt')
        self.assertEqual(correct, wl)
        
        correct = pickle.load(open('bill_file_1_wll.pkl', 'rb'))
        wl = WLTester('bill_file_1.txt')
        self.assertEqual(correct, wl)
        
        correct = pickle.load(open('bill_file_100_wll.pkl', 'rb'))
        wl = WLTester('bill_file_100.txt')
        self.assertEqual(correct, wl)
        
    def test_insert_WatchListLinked(self):
        wl = WLTester()
        wl.insert('abc', '5')
        wl.insert('abcd', '5')
        wl.insert('abef', '5')
        wl.insert('abcde', '5')
        wl.insert('abce', '5')
        correct = pickle.load(open('bill_file_5_wll.pkl', 'rb'))
        self.assertEqual(correct, wl)
        
    def test_search_WatchListLinked(self):
        wl = WatchListLinked('bill_file_77.txt')
        self.assertTrue(wl.search('JB67705552I', '5'))
        self.assertTrue(wl.search('GJ03569965R', '50'))
        self.assertTrue(wl.search('AL18844331R', '20'))
        self.assertTrue(wl.search('HE44178509U', '10'))
        self.assertTrue(wl.search('LB21339931W', '20'))
        self.assertTrue(wl.search('AG35934714H', '100'))
        self.assertFalse(wl.search('JB67705552I', '50'))
        self.assertFalse(wl.search('JB67705552', '5'))
        self.assertFalse(wl.search('JB6770555', '5'))
        self.assertFalse(wl.search('AG35934714H', '10'))
        self.assertFalse(wl.search('AL18944331R', '20'))
        self.assertFalse(wl.search('JB67805552I', '5'))
        self.assertFalse(wl.search('AG35924714H', '100'))
        wl = WatchListLinked()
        self.assertFalse(wl.search('JB67705552I', '5'))
        wl = WatchListLinked('bill_file_1.txt')
        self.assertFalse(wl.search('JB67705552I', '5'))
        self.assertFalse(wl.search('JB67705552I', '100'))
        self.assertTrue(wl.search('CF35365625U', '100'))
        wl = WatchListLinked('bill_file_5.txt')
        self.assertFalse(wl.search('a', '5'))
        self.assertFalse(wl.search('ab', '5'))
        self.assertFalse(wl.search('abe', '5'))
        self.assertFalse(wl.search('abf', '5'))
        self.assertTrue(wl.search('abc', '5'))
        self.assertTrue(wl.search('abcd', '5'))
        self.assertTrue(wl.search('abef', '5'))
        self.assertTrue(wl.search('abcde', '5'))
        self.assertTrue(wl.search('abce', '5'))
    
    def test_init_WatchListDict(self):
        correct = {'5': {}, '10': {}, '20': {}, '50': {}, '100': {}}
        wl = WatchListDict()
        self.assertEqual(correct, wl.root)
        
        wl = WatchListDict('bill_file_0.txt')
        self.assertEqual(correct, wl.root)
        
        correct = {'5': {'a': {'b': {'c': {None: None, 'd': {None: None, 'e': {None: None}}, 
                   'e': {None: None}}, 'e': {'f': {None: None}}}}}, 
                   '10': {}, '20': {}, '50': {}, '100': {}}
        wl = WatchListDict('bill_file_5.txt')
        self.assertEqual(correct, wl.root)
        self.assertTrue(wl.validator.match('CF35365625U'))
        self.assertEqual(['__weakref__', 'insert', 'root', 'search', 'validator'],
                         dir(wl)[-5:])
                         
        correct = {'5': {}, '10': {}, '20': {}, '50': {}, 
                   '100': {'C': {'F': {'3': {'5': {'3': {'6': {'5': {'6': 
                   {'2': {'5': {'U': {None: None}}}}}}}}}}}}}
        wl = WatchListDict('bill_file_1.txt')
        self.assertEqual(correct, wl.root)
        
        correct = pickle.load(open('bill_file_77_wld.pkl', 'rb'))
        wl = WatchListDict('bill_file_77.txt')
        self.assertEqual(correct.root, wl.root)
        
    def test_insert_WatchListDict(self):
        wl = WatchListDict()
        wl.insert('abc', '5')
        wl.insert('abcd', '5')
        wl.insert('abef', '5')
        wl.insert('abcde', '5')
        wl.insert('abce', '5')
        correct = {'5': {'a': {'b': {'c': {None: None, 'd': {None: None, 'e': {None: None}}, 
                   'e': {None: None}}, 'e': {'f': {None: None}}}}}, 
                   '10': {}, '20': {}, '50': {}, '100': {}}
        self.assertEqual(correct, wl.root)
        
    def test_search_WatchListDict(self):
        wl = WatchListDict('bill_file_77.txt')
        self.assertTrue(wl.search('JB67705552I', '5'))
        self.assertTrue(wl.search('GJ03569965R', '50'))
        self.assertTrue(wl.search('AL18844331R', '20'))
        self.assertTrue(wl.search('HE44178509U', '10'))
        self.assertTrue(wl.search('LB21339931W', '20'))
        self.assertTrue(wl.search('AG35934714H', '100'))
        self.assertFalse(wl.search('JB67705552I', '50'))
        self.assertFalse(wl.search('JB67705552', '5'))
        self.assertFalse(wl.search('JB6770555', '5'))
        self.assertFalse(wl.search('AG35934714H', '10'))
        self.assertFalse(wl.search('AL18944331R', '20'))
        self.assertFalse(wl.search('JB67805552I', '5'))
        self.assertFalse(wl.search('AG35924714H', '100'))
        wl = WatchListDict()
        self.assertFalse(wl.search('JB67705552I', '5'))
        wl = WatchListDict('bill_file_1.txt')
        self.assertFalse(wl.search('JB67705552I', '5'))
        self.assertFalse(wl.search('JB67705552I', '100'))
        self.assertTrue(wl.search('CF35365625U', '100'))
        wl = WatchListDict('bill_file_5.txt')
        self.assertFalse(wl.search('a', '5'))
        self.assertFalse(wl.search('ab', '5'))
        self.assertFalse(wl.search('abe', '5'))
        self.assertFalse(wl.search('abf', '5'))
        self.assertTrue(wl.search('abc', '5'))
        self.assertTrue(wl.search('abcd', '5'))
        self.assertTrue(wl.search('abef', '5'))
        self.assertTrue(wl.search('abcde', '5'))
        self.assertTrue(wl.search('abce', '5'))
    
    def test_check_bills(self):
        wl = WatchListLinked('bill_file_77.txt')
        correct = ['JB67705552I 5', 'GJ03569965R 50', 'AL18844331R 20',
                   'HE44178509U 10', 'LB21339931W 20', 'AG35934714H 100',
                   'AAG35924714H 100']
        self.assertEqual(correct, check_bills(wl, 'recovered_bills.txt'))
        
        wl = WatchListDict('bill_file_77.txt')
        self.assertEqual(correct, check_bills(wl, 'recovered_bills.txt'))
        
if __name__ == "__main__":
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestClasses)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')

""" # getting this out of the way for clarity's sake
    # used it to test my eq in the Node class
    def test_eq(self):
        n = Node('10')
        m = Node('20')
        self.assertEqual(n, m)
        
        n.children.extend([Node('5'), Node('20')])
        self.assertNotEqual(n, m)
        
        m.children.append(Node('20'))
        self.assertNotEqual(n, m)
        
        m.children.append(Node('5'))
        self.assertEqual(n, m)
        
        n.children[0].children.append(Node('7'))
        self.assertNotEqual(n, m)
        
        m.children[1].children.append(Node('7'))
        self.assertEqual(n, m)
        
        m.children[1].children.append(Node('8'))
        self.assertNotEqual(n, m)
        
        n.children[0].children.append(Node('8'))
        self.assertEqual(n, m)
"""
    


