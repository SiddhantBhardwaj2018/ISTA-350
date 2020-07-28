from hw6 import *
import hw6
import unittest, gzip, os, sys, io, requests
from contextlib import redirect_stdout
from unittest.mock import patch
from bs4 import BeautifulSoup

"""
Files needed: index.html, test_save_soup.txt
"""

class MockResponse:
    def __init__(self, content):
        self.content = content
        
class TestFns(unittest.TestCase):
    def test_get_soup(self):
        # test the case of gzipped response content that Python can't 
        # automatically unzip due to a broken header
        sample_html = open('index.html').read()
        zipped_html = gzip.compress(bytes(sample_html, 'utf-8'))
        mock_response = MockResponse(zipped_html)
        with patch('requests.get', side_effect=[mock_response]):
            soup = get_soup('http://test.html', gzipped=True)
        self.assertEqual(BeautifulSoup(sample_html), soup)
        # test the case of a response that was successfully 
        # processed by Python
        sample_html = open('index.html').read()
        mock_response = MockResponse(sample_html)
        with patch('requests.get', side_effect=[mock_response]):
            soup = get_soup('http://test.html')
        self.assertEqual(BeautifulSoup(sample_html), soup)
        # test for the case of html in a file
        soup = get_soup(fname='index.html')
        self.assertEqual(BeautifulSoup(sample_html), soup)
        # test the exception
        with self.assertRaises(RuntimeError) as cm:
            get_soup()
        self.assertEqual(cm.exception.args[0], 'Either url or filename must be specified.')
    
    def test_save_soup(self):
        files = os.listdir()
        if 'test_save_soup.txt' in files:
            os.remove('test_save_soup.txt')
        soup = BeautifulSoup(open('index.html').read())
        save_soup('test_save_soup.txt', soup)
        soup_test = BeautifulSoup(open('test_save_soup.txt').read())
        self.assertEqual(soup, soup_test)
        
    def test_scrape_and_save(self):
        files = os.listdir()
        for file in files:
            if file in ['wrcc_pcpn.html', 'wrcc_mint.html', 'wrcc_maxt.html']:
                os.remove(file)
        scrape_and_save()
        
        url = 'http://www.wrcc.dri.edu/WRCCWrappers.py?sodxtrmts+028815+por+por+pcpn+none+msum+5+01+F'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        pcpn_string = repr(soup)

        url='http://www.wrcc.dri.edu/WRCCWrappers.py?sodxtrmts+028815+por+por+mint+none+mave+5+01+F'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        mint_string = repr(soup)
        
        url='http://www.wrcc.dri.edu/WRCCWrappers.py?sodxtrmts+028815+por+por+maxt+none+mave+5+01+F'
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        maxt_string = repr(soup)

        self.assertEqual(pcpn_string, open('wrcc_pcpn.html').read())
        self.assertEqual(mint_string, open('wrcc_mint.html').read())
        self.assertEqual(maxt_string , open('wrcc_maxt.html').read())
                
    def test_main(self):
        files = os.listdir()
        for file in files:
            if file in ['wrcc_pcpn.html', 'wrcc_mint.html', 'wrcc_maxt.html']:
                os.remove(file)
        with io.StringIO() as buf, redirect_stdout(buf):
            hw6.main()
            self.assertEqual('---- scraping and saving ----\n', buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            hw6.main()
            self.assertEqual('', buf.getvalue())
            
def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    sys.stdout = sys.__stdout__
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')

if __name__ == "__main__":
    main()