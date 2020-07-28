from hw8 import *
import hw8
import unittest, json, filecmp, sys, io, pandas as pd
from contextlib import redirect_stdout
from compare_files import compare_files
from compare_pandas import compare_frames
import matplotlib.pyplot as plt
from unittest.mock import patch

# First run this, then run the module itself to create the figs.

''' 
Files needed:
'compare_files.py', 'compare_pandas.py'
'wrcc_pcpn_panda.pkl','wrcc_mint_panda.pkl', 'wrcc_maxt_panda.pkl'
'wrcc_pcpn_stats.pkl','wrcc_mint_stats.pkl', 'wrcc_maxt_stats.pkl'
'wrcc_pcpn_smooth.json','wrcc_mint_smooth.json', 'wrcc_maxt_smooth.json'
'wrcc_pcpn_correct.json','wrcc_mint_correct.json', 'wrcc_maxt_correct.json'

This is what your output should look like:
'pcpn_all.png','mint_all.png','maxt_all.png','pcpn_jan.png'

Also provided:
'wrcc_pcpn.json', 'wrcc_maxt.json', 'wrcc_mint.json'
These are provided so that hw8.py can run correctly, in case
students failed to get hw7 to create them correctly.
'''

def load_panda(fname=None, txt=None):
    if fname:
        txt = open(fname).read()
    txt = txt.split('\n')
    return [line.split() for line in txt]

class TestFns(unittest.TestCase):
    def test_get_panda(self):
        self.assertTrue(compare_frames(pd.read_pickle('wrcc_pcpn_panda.pkl'), get_panda('wrcc_pcpn_correct.json')))
        self.assertTrue(compare_frames(pd.read_pickle('wrcc_mint_panda.pkl'), get_panda('wrcc_mint_correct.json')))
        self.assertTrue(compare_frames(pd.read_pickle('wrcc_maxt_panda.pkl'), get_panda('wrcc_maxt_correct.json')))
        
    def test_get_stats(self):
        '''
        this test will fail if get_panda doesn't work
        '''
        self.assertTrue(compare_frames(pd.read_pickle('wrcc_pcpn_stats.pkl'), get_stats(get_panda('wrcc_pcpn_correct.json')), 0.001))     
        self.assertTrue(compare_frames(pd.read_pickle('wrcc_mint_stats.pkl'), get_stats(get_panda('wrcc_mint_correct.json')), 0.001))     
        self.assertTrue(compare_frames(pd.read_pickle('wrcc_maxt_stats.pkl'), get_stats(get_panda('wrcc_maxt_correct.json')), 0.001))     

    """ 
    # not using this anymore, grading by hand:
    def test_print_stats(self):
        '''
        this test will fail if either get_panda or get_stats doesn't work
        '''
        with io.StringIO() as buf, redirect_stdout(buf):
            print_stats('wrcc_pcpn_correct.json')
            self.assertEqual('----- Statistics for wrcc_pcpn_correct.json -----\n\n' + open('wrcc_pcpn_stats.txt').read() + '\n\n',
                buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            print_stats('wrcc_mint_correct.json')
            self.assertEqual('----- Statistics for wrcc_mint_correct.json -----\n\n' + open('wrcc_mint_stats.txt').read() + '\n\n',
                buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            print_stats('wrcc_maxt_correct.json')
            self.assertEqual('----- Statistics for wrcc_maxt_correct.json -----\n\n' + open('wrcc_maxt_stats.txt').read() + '\n\n',
                buf.getvalue())
    """
    
    def test_smooth_data(self):
        '''
        this test will fail if get_panda doesn't work
        '''
        # add a test for the default value of precision
        self.assertTrue(compare_frames(get_panda('wrcc_pcpn_smooth.json'), smooth_data(get_panda('wrcc_pcpn_correct.json'), 2)))     
        self.assertTrue(compare_frames(get_panda('wrcc_mint_smooth.json'), smooth_data(get_panda('wrcc_mint_correct.json'), 2)))     
        self.assertTrue(compare_frames(get_panda('wrcc_maxt_smooth.json'), smooth_data(get_panda('wrcc_maxt_correct.json'), 2)))    

def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    sys.stdout = sys.__stdout__
    hw8.main()
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 60) + ' / 60')
    
if __name__ == "__main__":
    main()