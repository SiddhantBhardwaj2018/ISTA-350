from hw1 import WatchList
import unittest, pickle, inspect

'''
Files needed:
hw1.py
bill_file_0.txt, bill_file_1.txt, bill_file_77.txt 
bill_file_77.pkl, bill_file_77_sorted.pkl
recovered_bills.txt
'''

class TestFns(unittest.TestCase):
    def test_init_I(self):
        wl = WatchList()
        correct = {'5': [], '10': [], '20': [], '50': [], '100': []}
        self.assertEqual(correct, wl.bills)
        self.assertTrue(wl.is_sorted)
        self.assertTrue(wl.validator.match('CF35365625U'))
        
        wl = WatchList('bill_file_0.txt')
        self.assertEqual(correct, wl.bills)
        self.assertFalse(wl.is_sorted)
        self.assertTrue(wl.validator.match('CF35365625U'))
        
        wl = WatchList('bill_file_1.txt')
        correct = {'5': [], '10': [], '20': [], '50': [], '100': ['CF35365625U']}
        self.assertEqual(correct, wl.bills)
        self.assertFalse(wl.is_sorted)
        self.assertTrue(wl.validator.match('CF35365625U'))
        
        wl = WatchList('bill_file_77.txt')
        sorted_dict = pickle.load(open('bill_file_77_sorted.pkl', 'rb'))
        self.assertNotEqual(sorted_dict, wl.bills)
        correct = pickle.load(open('bill_file_77.pkl', 'rb'))
        self.assertEqual(correct, wl.bills)
        self.assertFalse(wl.is_sorted)
        self.assertTrue(wl.validator.match('CF35365625U'))
        
    def test_init_re(self):
        wl = WatchList()
        self.assertTrue(wl.validator.search('AI84639149A'))
        self.assertTrue(wl.validator.search('KI21489455W'))
        self.assertTrue(wl.validator.search('AF19683425I'))
        self.assertTrue(wl.validator.search('AI00010000A'))
        self.assertTrue(wl.validator.search('MI84639149A'))
        self.assertTrue(wl.validator.search('AL84639149A'))
        self.assertTrue(wl.validator.search('AI84639149Y'))
        self.assertFalse(wl.validator.search('AI84639149Z'))
        self.assertTrue(wl.validator.search('AI84779149N'))
        self.assertTrue(wl.validator.search('AI84779149P'))
        self.assertFalse(wl.validator.search('AI0001000A'))
        self.assertFalse(wl.validator.search('AI00000000A'))
        self.assertFalse(wl.validator.search('AII84779149A'))
        self.assertFalse(wl.validator.search('AI84779149AA'))
        self.assertFalse(wl.validator.search('A84779149A'))
        self.assertFalse(wl.validator.search('AI84639149AA'))
        self.assertFalse(wl.validator.search('AI84639149A1'))
        self.assertFalse(wl.validator.search('AI84639149AAI84639149A'))
        self.assertFalse(wl.validator.search('AAI84639149A'))
        self.assertFalse(wl.validator.search('1AI84639149A'))
        self.assertFalse(wl.validator.search('AI84639149O'))
        self.assertFalse(wl.validator.search('aI84639149A'))
        self.assertFalse(wl.validator.search('Ai84639149A'))
        self.assertFalse(wl.validator.search('AI84639149a'))
        self.assertFalse(wl.validator.search('AN84639149A'))
        self.assertFalse(wl.validator.search('AM84639149A'))
        self.assertFalse(wl.validator.search('AI846392149A'))

    def test_insert(self):
        '''
        Not testing for how dups are being handled.  Which we should,
        because there aren't supposed to be any dups put in.
        '''
        wl = WatchList()
        source_code = inspect.getsource(wl.insert)
        self.assertFalse('sort(' in source_code)
        self.assertFalse('sorted(' in source_code)
        self.assertFalse('sort_bills' in source_code)
        self.assertIsNone(wl.insert('AI84639149A 100'))
        wl.insert('AE84639149A 100')
        wl.insert('AH84639149A 100')
        wl.insert('AL84639149A 100')
        self.assertFalse(wl.bills['5'] or wl.bills['10'] or 
                         wl.bills['20'] or wl.bills['50'])
        correct = ['AE84639149A', 'AH84639149A', 'AI84639149A', 'AL84639149A']
        self.assertEqual(correct, wl.bills['100'])
        wl.insert('AI84639149A 10')
        wl.insert('AE84639149A 10')
        wl.insert('AH84639149A 10')
        wl.insert('AL84639149A 10')
        self.assertFalse(wl.bills['5'] or 
                         wl.bills['20'] or wl.bills['50'])
        correct = ['AE84639149A', 'AH84639149A', 'AI84639149A', 'AL84639149A']
        self.assertEqual(correct, wl.bills['10'])
        wl = WatchList('bill_file_1.txt')
        wl.insert('AI84639149A 100')
        wl.insert('AE84639149A 100')
        correct = ['CF35365625U', 'AI84639149A', 'AE84639149A']
        self.assertEqual(correct, wl.bills['100'])
        wl = WatchList()
        wl.is_sorted = False
        self.assertIsNone(wl.insert('AI84639149A 100'))
        wl.insert('AE84639149A 100')
        wl.insert('AH84639149A 100')
        wl.insert('AL84639149A 100')
        self.assertFalse(wl.bills['5'] or wl.bills['10'] or 
                         wl.bills['20'] or wl.bills['50'])
        correct = ['AI84639149A', 'AE84639149A', 'AH84639149A', 'AL84639149A']
        self.assertEqual(correct, wl.bills['100'])
        
    def test_sort_bills(self):
        wl = WatchList('bill_file_77.txt')
        correct = pickle.load(open('bill_file_77_sorted.pkl', 'rb'))
        self.assertIsNone(wl.sort_bills())
        self.assertEqual(correct, wl.bills)
        self.assertTrue(wl.is_sorted)
        
    def test_linear_search(self):
        wl = WatchList('bill_file_77.txt')
        self.assertTrue(wl.linear_search('JB67705552I 5'))
        self.assertTrue(wl.linear_search('GJ03569965R 50'))
        self.assertTrue(wl.linear_search('AL18844331R 20'))
        self.assertTrue(wl.linear_search('HE44178509U 10'))
        self.assertTrue(wl.linear_search('LB21339931W 20'))
        self.assertTrue(wl.linear_search('AG35934714H 100'))
        self.assertFalse(wl.linear_search('JB67705552I 50'))
        self.assertFalse(wl.linear_search('AG35934714H 10'))
        self.assertFalse(wl.linear_search('AL18944331R 20'))
        self.assertFalse(wl.linear_search('JB67805552I 5'))
        self.assertFalse(wl.linear_search('AG35924714H 100'))
        
    def test_binary_search(self):
        wl = WatchList('bill_file_77.txt')
        wl.sort_bills()
        self.assertTrue(wl.binary_search('JB67705552I 5'))
        self.assertTrue(wl.binary_search('GJ03569965R 50'))
        self.assertTrue(wl.binary_search('AL18844331R 20'))
        self.assertTrue(wl.binary_search('HE44178509U 10'))
        self.assertTrue(wl.binary_search('LB21339931W 20'))
        self.assertTrue(wl.binary_search('AG35934714H 100'))
        self.assertFalse(wl.binary_search('JB67705552I 50'))
        self.assertFalse(wl.binary_search('AG35934714H 10'))
        self.assertFalse(wl.binary_search('AL18944331R 20'))
        self.assertFalse(wl.binary_search('JB67805552I 5'))
        self.assertFalse(wl.binary_search('AG35924714H 100'))
        wl = WatchList()
        self.assertFalse(wl.binary_search('JB67705552I 5'))
        wl = WatchList('bill_file_1.txt')
        self.assertFalse(wl.binary_search('JB67705552I 5'))
        self.assertFalse(wl.binary_search('JB67705552I 100'))
        self.assertTrue(wl.binary_search('CF35365625U 100'))
        wl.bills['100'].append('JB67705552I')
        self.assertTrue(wl.binary_search('JB67705552I 100'))
        self.assertTrue(wl.binary_search('CF35365625U 100'))
    
    def test_check_bills(self):
        wl = WatchList('bill_file_77.txt')
        correct = ['JB67705552I 5', 'GJ03569965R 50', 'AL18844331R 20',
                   'HE44178509U 10', 'LB21339931W 20', 'AG35934714H 100',
                   'AAG35924714H 100']
        self.assertEqual(correct, wl.check_bills('recovered_bills.txt'))
        sorted_dict = pickle.load(open('bill_file_77_sorted.pkl', 'rb'))
        self.assertNotEqual(sorted_dict, wl.bills)
        self.assertEqual(correct, wl.check_bills('recovered_bills.txt', True))
        self.assertEqual(sorted_dict, wl.bills)
       
if __name__ == "__main__":
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')
