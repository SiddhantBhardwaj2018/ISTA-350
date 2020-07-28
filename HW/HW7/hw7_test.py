from hw7 import *
from compare_files import compare_files
from compare_pandas import compare_lols
import unittest, json, os

############################
# Add a compare_lists_from_json function to 
# compare files and use for testing in 
# test_clean_and_jsonify
###########################
''' 
Files needed:
'compare_files.py', 'compare_pandas.py'
'wrcc_pcpn.html','wrcc_mint.html', 'wrcc_maxt.html'
'wrcc_pcpn_list.json','wrcc_mint_list.json', 'wrcc_maxt_list.json'
'wrcc_pcpn_clean.json','wrcc_mint_clean.json', 'wrcc_maxt_clean.json'
'wrcc_pcpn_correct.json','wrcc_mint_correct.json', 'wrcc_maxt_correct.json'
'get_soup.py' - for posting AFTER hw6 has been turned in.  Maybe.
'''

class TestFns(unittest.TestCase):
    def test_is_num(self):
        # add empty string test
        self.assertTrue(is_num('000'))
        self.assertTrue(is_num('0.00'))
        self.assertTrue(is_num('-1.32'))
        self.assertTrue(is_num('-1'))
        self.assertTrue(is_num('-.04'))
        self.assertTrue(is_num('-00.00400'))
        self.assertTrue(is_num('1.32'))
        self.assertTrue(is_num('1'))
        self.assertTrue(is_num('-13'))
        self.assertTrue(is_num('13'))
        self.assertTrue(is_num('.04'))
        self.assertTrue(is_num('00.00400'))
        self.assertTrue(is_num('00010'))
        self.assertFalse(is_num('000..'))
        self.assertFalse(is_num('--13'))
        self.assertFalse(is_num('1-3'))
        self.assertFalse(is_num('13-'))
        self.assertFalse(is_num('.1.'))
        self.assertFalse(is_num('.1.3'))
        self.assertFalse(is_num('-.1.3'))
        self.assertFalse(is_num('z'))
        
    def test_load_lists(self):
        """ 
        load_lists depends on is_num 
        !!! NEED TO USE compare_lols TO CHECK TYPES !!!
        """
        fnames = ['wrcc_pcpn.html','wrcc_mint.html', 'wrcc_maxt.html']
        for fname in fnames:
            soup = get_soup(fname=fname)
            data = load_lists(soup, -999)
            with open(fname.split('.')[0] + '_list.json') as fp:
                data_correct = json.load(fp)
            self.assertEqual(data_correct, data)
    
    def test_replace_na(self):
        # add a test for the default value of precision
        data = [[6, 1, 1, 1, 1, -999]]
        self.assertEqual(2, replace_na(data, 0, 5, -999, 2))
        data = [[-999, 1, 1, -999, -999, -999]]
        self.assertEqual(1, replace_na(data, 0, 5, -999, 2))
        data = [[100, 6, 1, 1, 1, 1, -999]]
        self.assertEqual(2, replace_na(data, 0, 6, -999, 2))
        data = [[-999, 1, 1, 1, 1, 6]]
        self.assertEqual(2, replace_na(data, 0, 0, -999, 2))
        data = [[-999, 1, 1, 1, 1, 6, 100]]
        self.assertEqual(2, replace_na(data, 0, 0, -999, 2))
        data = [[6, 1, 2, -999, 1, -999]]
        self.assertEqual(2.5, replace_na(data, 0, 5, -999, 2))
        data = [[-999, -999, 1, 1, 2, 6]]
        self.assertEqual(2.5, replace_na(data, 0, 0, -999, 2))
        data = [[6, 1, 2, -999, 1, -999]]
        self.assertEqual(2.5, replace_na(data, 0, 3, -999, 2))
        data = [[5, 4, 3, 2, 1, -999, -1, -2, -3, -4, -5]]
        self.assertEqual(0, replace_na(data, 0, 5, -999, 2))
        data = [[100, 5, 4, 3, 2, 1, -999, -1, -2, -3, -4, -5, -1000]]
        self.assertEqual(0, replace_na(data, 0, 6, -999, 2))
        
    def test_clean_data(self):
        ''' clean_data depends on replace_na '''
        # add a test for the default value of precision
        fnames = ['wrcc_pcpn.html','wrcc_mint.html', 'wrcc_maxt.html']
        for fname in fnames:
            with open(fname.split('.')[0] + '_list.json') as fp:
                data = json.load(fp)
            clean_data(data, -999, 2)
            with open(fname.split('.')[0] + '_clean.json') as fp:
                data_correct = json.load(fp)
            self.assertTrue(compare_lols(data_correct, data, 0.01))
           
    def test_recalculate_annual_data(self):
        """
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        hw7_kayda.py passes this test, but it is wrong!!!
        Use that file to figure out how to fix this test!!!
        """
        # add a test for the default value of precision
        data = [[2001, 2002, 2003],
                [  10,    1,   -1],
                [  10,    2,    0],
                [  10,    3,    1],
                [   0,    0,   11]]
        recalc = [[2001, 2002, 2003],
                  [  10,    1,   -1],
                  [  10,    2,    0],
                  [  10,    3,    1],
                  [  30,    6,    0]]
        recalculate_annual_data(data, False, 2)
        self.assertEqual(data, recalc)
        recalc = [[2001, 2002, 2003],
                  [  10,    1,   -1],
                  [  10,    2,    0],
                  [  10,    3,    1],
                  [  10,    2,    0]]
        recalculate_annual_data(data, True, 2)
        self.assertEqual(data, recalc)
        
    def test_clean_and_jsonify(self):
        '''
        Fix this one by mocking the call to recalc
        '''
        # add a test for the default value of precision
        fnames = ['wrcc_pcpn.html','wrcc_mint.html', 'wrcc_maxt.html']
        fnames2 = ['wrcc_pcpn.json','wrcc_mint.json', 'wrcc_maxt.json']
        files = os.listdir()
        for f in fnames2:
            if f in files:
                os.remove(f)
        clean_and_jsonify(fnames, -999, 2)
        with open('wrcc_pcpn_correct.json') as fp:
            correct = json.load(fp)
        with open('wrcc_pcpn.json') as fp:
            student = json.load(fp)
        self.assertTrue(compare_lols(correct, student, 0.01))
        with open('wrcc_maxt_correct.json') as fp:
            correct = json.load(fp)
        with open('wrcc_maxt.json') as fp:
            student = json.load(fp)
        self.assertTrue(compare_lols(correct, student, 0.01))
        with open('wrcc_mint_correct.json') as fp:
            correct = json.load(fp)
        with open('wrcc_mint.json') as fp:
            student = json.load(fp)
        self.assertTrue(compare_lols(correct, student, 0.01))
            
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')

if __name__ == "__main__":
    main()