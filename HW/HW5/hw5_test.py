from hw5 import *
import unittest, pickle, inspect

'''
Files needed:
hw5.py
test_in.txt
'''

"""
All of these tests depend upon previously tested methods 
working correctly.  
"""

class TestClasses(unittest.TestCase):
    def test_init_Node(self):
        n = Node('10')
        self.assertEqual('10', n.datum)
        self.assertIsNone(n.left)
        self.assertIsNone(n.right)
        self.assertFalse(hasattr(n, 'children'))
     
    def test_add_Node(self):
        n = Node(5)
        n + 3
        self.assertEqual(3, n.left.datum)
        self.assertIsNone(n.left.left)
        self.assertIsNone(n.left.right)
        self.assertIsNone(n.right)
        n + 7
        n + 5
        n + 3
        n + 7
        n + 2
        n + 4
        n + 6
        n + 8
        self.assertEqual(2, n.left.left.datum)
        self.assertEqual(4, n.left.right.datum)
        self.assertEqual(3, n.left.datum)
        self.assertEqual(6, n.right.left.datum)
        self.assertEqual(8, n.right.right.datum)
        self.assertEqual(7, n.right.datum)
        self.assertIsNone(n.left.left.left)
        self.assertIsNone(n.left.left.right)
        self.assertIsNone(n.left.right.left)
        self.assertIsNone(n.left.right.right)
        self.assertIsNone(n.right.left.left)
        self.assertIsNone(n.right.left.right)
        self.assertIsNone(n.right.right.left)
        self.assertIsNone(n.right.right.right)
        n = Node(5)
        n + 7
        self.assertEqual(7, n.right.datum)
        self.assertIsNone(n.right.left)
        self.assertIsNone(n.right.right)
        self.assertIsNone(n.left)
        
    def test_in_Node(self):
        n = Node(5)
        self.assertTrue(5 in n)
        self.assertFalse(3 in n)
        n + 3
        n + 7
        n + 5
        n + 3
        n + 7
        n + 2
        n + 4
        n + 6
        n + 8
        for i in range(3, 9):
            self.assertTrue(i in n)
        for x in range(2, 9):
            self.assertFalse(x + 0.5 in n)
        n = Node(5)
        self.assertIsNotNone(n.__contains__(7))
        self.assertIsNotNone(n.__contains__(3))
        
    def test_sort_Node(self):
        n = Node(5)
        srtd = []
        n.sort(srtd)
        self.assertEqual([5], srtd)
        n + 3
        n + 7
        n + 5
        n + 3
        n + 7
        n + 2
        n + 4
        n + 6
        n + 8
        srtd = []
        n.sort(srtd)
        self.assertEqual(list(range(2, 9)), srtd)

    def test_eq_Node(self):
        n1 = Node(5)
        n2 = Node(5)
        self.assertEqual(n1, n2)
        
        n3 = Node(3)
        self.assertNotEqual(n1, n3)
        
        n1 + 1
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n1 + 10
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n2 + 10
        self.assertNotEqual(n1, n2)
           
        n1 = Node(5)
        n2 = Node(5)
        n2 + 1
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n1 + 7
        n2 + 3
        n1 + 3
        n2 + 7
        n1 + 2
        n2 + 4
        n1 + 4
        n2 + 2
        n1 + 6
        n2 + 8
        n1 + 8
        n2 + 6
        self.assertEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n1 + 7
        n2 + 3
        n1 + 3
        n2 + 7
        n1 + 2
        n2 + 4
        n1 + 4
        n2 + 2
        n1 + 6
        n2 + 8
        n1 + 8
        n2 + 99
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n1 + 7
        n2 + 3
        n1 + 3
        n2 + 7
        n1 + 2
        n2 + 4
        n1 + 4
        n2 + -1
        n1 + 6
        n2 + 8
        n1 + 8
        n2 + 6
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n1 + 7
        n2 + 3
        n1 + 3
        n2 + 7
        n1 + 2
        n2 + 4
        n1 + 4
        n2 + 2
        n1 + 88
        n2 + 8
        n1 + 8
        n2 + 6
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n1 + 7
        n2 + 3
        n1 + 3
        n2 + 7
        n1 + 2
        n2 + 4
        n1 + -3
        n2 + 2
        n1 + 6
        n2 + 8
        n1 + 8
        n2 + 6
        self.assertNotEqual(n1, n2)
        
        n1 = Node(5)
        n2 = Node(5)
        n1 + 3
        n2 + 3
        self.assertEqual(n1, n2)

        n1 = Node(5)
        n2 = Node(5)
        n1 + 7
        n2 + 7
        self.assertEqual(n1, n2)
        
        n1 = Node(2)
        n1 + 1
        n1 + 3
        n2 = Node(1)
        n1 + 2
        n1 + 3
        self.assertNotEqual(n1, n2)

    def test_init_BST(self):
        bst = BST()
        self.assertIsNone(bst.root)
        bst = BST('10')
        self.assertEqual('10', bst.root.datum)
        self.assertIsNone(bst.root.left)
        self.assertIsNone(bst.root.right)
     
    def test_add_BST(self):
        bst = BST()
        self.assertIsNone(bst.root)
        bst + 3
        self.assertEqual(3, bst.root.datum)
        bst = BST(5)
        bst + 3
        self.assertEqual(3, bst.root.left.datum)
        self.assertIsNone(bst.root.left.left)
        self.assertIsNone(bst.root.left.right)
        self.assertIsNone(bst.root.right)
        bst + 7
        bst + 5
        bst + 3
        bst + 7
        bst + 2
        bst + 4
        bst + 6
        bst + 8
        self.assertEqual(2, bst.root.left.left.datum)
        self.assertEqual(4, bst.root.left.right.datum)
        self.assertEqual(3, bst.root.left.datum)
        self.assertEqual(6, bst.root.right.left.datum)
        self.assertEqual(8, bst.root.right.right.datum)
        self.assertEqual(7, bst.root.right.datum)
        self.assertIsNone(bst.root.left.left.left)
        self.assertIsNone(bst.root.left.left.right)
        self.assertIsNone(bst.root.left.right.left)
        self.assertIsNone(bst.root.left.right.right)
        self.assertIsNone(bst.root.right.left.left)
        self.assertIsNone(bst.root.right.left.right)
        self.assertIsNone(bst.root.right.right.left)
        self.assertIsNone(bst.root.right.right.right)
        bst = BST(5)
        bst + 7
        self.assertEqual(7, bst.root.right.datum)
        self.assertIsNone(bst.root.right.left)
        self.assertIsNone(bst.root.right.right)
        self.assertIsNone(bst.root.left)
        
    def test_from_file_BST(self):
        bst_correct = BST('5')
        bst_correct + '3'
        bst_correct + '7'
        bst_correct + '5'
        bst_correct + '2'
        bst_correct + '4'
        bst_correct + '6'
        bst_correct + '8'
        bst = BST.from_file('test_in.txt')
        self.assertEqual(bst_correct.root, bst.root)
        bst_correct = BST(5)
        bst_correct + 3
        bst_correct + 7
        bst_correct + 5
        bst_correct + 2
        bst_correct + 4
        bst_correct + 6
        bst_correct + 8
        bst = BST.from_file('test_in.txt', int)
        self.assertEqual(bst_correct.root, bst.root)

    def test_in_BST(self):
        bst = BST()
        self.assertFalse(5 in bst)
        bst = BST(5)
        self.assertTrue(5 in bst)
        self.assertFalse(3 in bst)
        bst + 3
        bst + 7
        bst + 5
        bst + 3
        bst + 7
        bst + 2
        bst + 4
        bst + 6
        bst + 8
        for i in range(3, 9):
            self.assertTrue(i in bst)
        for x in range(2, 9):
            self.assertTrue(x + 0.5 not in bst)
           
    def test_sort_BST(self):
        bst = BST()
        self.assertEqual([], bst.sort())
        bst = BST(5)
        srtd = bst.sort()
        self.assertEqual([5], srtd)
        bst + 3
        bst + 7
        bst + 5
        bst + 3
        bst + 7
        bst + 2
        bst + 4
        bst + 6
        bst + 8
        srtd = bst.sort()
        self.assertEqual(list(range(2, 9)), srtd)
           
    def test_eq_BST(self):
        bst1 = BST(5)
        bst2 = BST(5)
        self.assertEqual(bst1, bst2)
        
        bst3 = BST(3)
        self.assertNotEqual(bst1, bst3)
        
        bst1 + 1
        self.assertNotEqual(bst1, bst2)
        
        bst1 = BST(5)
        bst1 + 10
        self.assertNotEqual(bst1, bst2)
        
        bst1 = BST(5)
        bst2 = BST(5)
        bst2 + 10
        self.assertNotEqual(bst1, bst2)
           
        bst1 = BST(5)
        bst2 = BST(5)
        bst2 + 1
        self.assertNotEqual(bst1, bst2)
        
        bst1 = BST(5)
        bst2 = BST(5)
        bst1 + 7
        bst2 + 3
        bst1 + 3
        bst2 + 7
        bst1 + 2
        bst2 + 4
        bst1 + 4
        bst2 + 2
        bst1 + 6
        bst2 + 8
        bst1 + 8
        bst2 + 6
        self.assertEqual(bst1, bst2)
        
        bst1 = BST(5)
        bst2 = BST(5)
        bst1 + 3
        bst2 + 3
        self.assertEqual(bst1, bst2)

        bst1 = BST(5)
        bst2 = BST(5)
        bst1 + 7
        bst2 + 7
        self.assertEqual(bst1, bst2)
        
        bst1 = BST()
        bst2 = BST(5)
        self.assertNotEqual(bst1, bst2)

        bst1 = BST(5)
        bst2 = BST()
        self.assertNotEqual(bst1, bst2)

        
    def test_selection_sort(self):
        lst = []
        selection_sort(lst)
        self.assertEqual([], lst)
        correct = list(range(10))
        lst = list(range(9, -1, -1))
        selection_sort(lst)
        self.assertEqual(correct, lst)
        text = inspect.getsource(selection_sort)
        self.assertTrue('sort' not in text[19:])
           
if __name__ == "__main__":
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestClasses)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')

