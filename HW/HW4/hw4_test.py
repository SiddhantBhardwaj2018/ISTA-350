from hw4 import Binary
import unittest, numpy as np, inspect, re

'''
!!!!!!!!!!
use inspect.getsource to check for illegal use of int and list in init
!!!!!!!!!!
'''

# add tests to make sure old instances are unchanged
class TestBinary(unittest.TestCase):
    def setUp(self):
        self.bin_0 = Binary("")
        self.bin_1 = Binary("01")
        self.bin_neg_1 = Binary("1")
        self.bin_neg_2 = Binary("10")
        self.bin_neg_3 = Binary("101")
        self.bin_2 = Binary("010")
        self.bin_3 = Binary("011")
        self.bin_5 = Binary("0101")
        self.bin_neg_5 = Binary("1011")
        self.bin_7 = Binary("0000000111")
        self.bin_neg_7 = Binary("1111111001")
        self.bin_neg_32768 = Binary("1000000000000000")
        self.bin_32767 = Binary("0111111111111111")
        self.bin_neg_32767 = Binary("1000000000000001")
        self.bin_32766 = Binary("0111111111111110")

    def test_init(self):
        self.assertTrue(all(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == self.bin_0.bit_array))
        self.assertTrue(all(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == self.bin_1.bit_array))
        self.assertTrue(all(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]) == self.bin_2.bit_array))
        self.assertTrue(all(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == self.bin_neg_1.bit_array))
        self.assertTrue(all(np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == self.bin_32767.bit_array))
        self.assertTrue(all(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]) == self.bin_neg_5.bit_array))
        self.assertTrue(all(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1]) == self.bin_neg_7.bit_array))
        self.assertTrue(all(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == self.bin_neg_32768.bit_array))
        self.assertRaises(RuntimeError, Binary, "abc")
        self.assertRaises(RuntimeError, Binary, "010120101")
        self.assertRaises(RuntimeError, Binary, "00000000000000000")
        text = inspect.getsource(Binary.__init__)
        self.assertTrue('list' not in text)
        self.assertTrue('ray([' not in text)       
        
    def test_repr(self):
        self.assertEqual("0000000000000000", repr(self.bin_0))
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual("0000000000000001", repr(self.bin_1))
        self.assertEqual(Binary('01'), self.bin_1)
        self.assertEqual("1111111111111011", repr(self.bin_neg_5))
        self.assertEqual(Binary('1011'), self.bin_neg_5)
        self.assertEqual("1111111111111001", repr(self.bin_neg_7))

    def test_add(self):
        self.assertEqual(self.bin_1, self.bin_7 + self.bin_neg_7 + self.bin_5 + self.bin_neg_3 + self.bin_neg_1)
        self.assertEqual(Binary('1001'), self.bin_neg_7)
        self.assertEqual(Binary('0111'), self.bin_7)
        self.assertEqual(self.bin_0, self.bin_0 + self.bin_0)
        self.assertEqual(self.bin_0, self.bin_1 + self.bin_neg_1)
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual(self.bin_neg_1, self.bin_0 + self.bin_neg_1)
        self.assertEqual(self.bin_neg_2, self.bin_neg_1 + self.bin_neg_1)
        with self.assertRaises(RuntimeError):
            self.bin_neg_32768 + self.bin_neg_1
        with self.assertRaises(RuntimeError):
            self.bin_32767 + self.bin_1
        self.assertEqual(self.bin_neg_32768, self.bin_0 + self.bin_neg_32768)
        self.assertEqual(self.bin_32767, self.bin_0 + self.bin_32767)
        self.assertEqual(self.bin_neg_32767, self.bin_1 + self.bin_neg_32768)
        self.assertEqual(self.bin_32766, self.bin_neg_1 + self.bin_32767)
        text = inspect.getsource(Binary.__add__)
        i = text.find('int')
        while i >= 0:
            self.assertTrue(text[i+3] == ')')
            i = text.find('int', i+1)
        
    def test_neg(self):
        self.assertEqual(self.bin_0, -self.bin_0)
        self.assertTrue(self.bin_0 is not -self.bin_0)
        self.assertFalse(self.bin_0 is -self.bin_0)
        self.assertEqual(self.bin_1, -self.bin_neg_1)
        self.assertEqual(self.bin_neg_1, -self.bin_1)
        self.assertEqual(self.bin_7, -self.bin_neg_7)
        self.assertEqual(self.bin_neg_7, -self.bin_7)
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual(Binary('1001'), self.bin_neg_7)
        self.assertEqual(Binary('0111'), self.bin_7)
        with self.assertRaises(RuntimeError):
            -self.bin_neg_32768
        with self.assertRaises(RuntimeError):
            -self.bin_32767 + self.bin_neg_1 + self.bin_neg_1
        text = inspect.getsource(Binary.__neg__)
        self.assertTrue('int' not in text)
        
    def test_sub(self):
        self.assertEqual(self.bin_0, self.bin_7 - self.bin_7)
        self.assertEqual(self.bin_2, self.bin_neg_3 - self.bin_neg_5)
        self.assertEqual(self.bin_neg_7, self.bin_neg_5 - self.bin_2)
        self.assertEqual(self.bin_neg_1, self.bin_5 - self.bin_3 - self.bin_3)
        self.assertEqual(self.bin_neg_3, self.bin_neg_5 - self.bin_neg_1 - self.bin_neg_1)
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual(Binary('1001'), self.bin_neg_7)
        self.assertEqual(Binary('0111'), self.bin_7)
        with self.assertRaises(RuntimeError):
            self.bin_neg_32768 - self.bin_1
        with self.assertRaises(RuntimeError):
            self.bin_32767 - self.bin_neg_1
        text = inspect.getsource(Binary.__sub__)
        self.assertTrue('int' not in text)
    
    def test_int(self):
        self.assertEqual(0, int(self.bin_0))
        self.assertEqual(1, int(self.bin_1))
        self.assertEqual(2, int(self.bin_2))
        self.assertEqual(3, int(self.bin_3))
        self.assertEqual(5, int(self.bin_5))
        self.assertEqual(7, int(self.bin_7))
        self.assertEqual(32767, int(self.bin_32767))
        self.assertEqual(-1, int(self.bin_neg_1))
        self.assertEqual(-3, int(self.bin_neg_3))
        self.assertEqual(-5, int(self.bin_neg_5))
        self.assertEqual(-7, int(self.bin_neg_7))
        self.assertEqual(-32767, int(self.bin_neg_32767))
        self.assertEqual(-32768, int(self.bin_neg_32768))
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual(Binary('1001'), self.bin_neg_7)
        self.assertEqual(Binary('0111'), self.bin_7)
        
    def test_eq(self):
        self.assertEqual(Binary("0101"), self.bin_5)
        self.assertEqual(Binary("0101"), self.bin_5)
        self.assertEqual(Binary("1011"), self.bin_neg_5)
        self.assertEqual(Binary("1011"), self.bin_neg_5)
        text = inspect.getsource(Binary.__eq__)
        self.assertTrue('int' not in text)
        
    def test_lt(self):
        self.assertTrue(self.bin_neg_32768 < self.bin_1)
        self.assertTrue(self.bin_0 < self.bin_1)
        self.assertFalse(self.bin_0 < self.bin_0)
        self.assertFalse(self.bin_1 < self.bin_0)
        self.assertFalse(self.bin_1 < self.bin_1)
        self.assertIsNotNone(self.bin_1 < self.bin_1)
        self.assertIsNotNone(self.bin_1 < self.bin_neg_1)
        self.assertIsNotNone(self.bin_neg_1 < self.bin_neg_1)
        self.assertIsNotNone(self.bin_neg_1 < self.bin_neg_3)
        self.assertIsNotNone(self.bin_5 < self.bin_neg_3)
        self.assertIsNotNone(self.bin_5 < self.bin_1)
        self.assertFalse(self.bin_1 < self.bin_neg_1)
        self.assertFalse(self.bin_neg_1 < self.bin_neg_1)
        self.assertFalse(self.bin_neg_1 < self.bin_neg_3)
        self.assertFalse(self.bin_5 < self.bin_neg_3)
        self.assertFalse(self.bin_5 < self.bin_1)
        self.assertFalse(self.bin_1 < self.bin_neg_5)
        self.assertTrue(self.bin_neg_5 < self.bin_1)
        self.assertTrue(self.bin_neg_32768 < self.bin_neg_1)
        self.assertTrue(self.bin_neg_5 < self.bin_neg_3)
        self.assertFalse(self.bin_neg_5 < self.bin_neg_5)
        self.assertTrue(self.bin_neg_32768 < self.bin_32767)
        self.assertFalse(self.bin_32767 < self.bin_neg_32768)
        self.assertFalse(self.bin_neg_32767 < self.bin_neg_32767)
        self.assertTrue(self.bin_neg_32767 < self.bin_32767)
        self.assertTrue(self.bin_1 < self.bin_32767)
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual(Binary('1011'), self.bin_neg_5)
        self.assertEqual(Binary('0101'), self.bin_5)
        text = inspect.getsource(Binary.__lt__)
        self.assertTrue('int' not in text)
        
    # add test to make sure is a new instance
    def test_abs(self):
        self.assertEqual(Binary("0101"), abs(self.bin_5))
        self.assertEqual(Binary("0101"), abs(self.bin_neg_5))
        self.assertEqual(Binary("0"), abs(self.bin_0))
        self.assertEqual(Binary(), self.bin_0) # make sure original instance is intact
        self.assertEqual(Binary('1011'), self.bin_neg_5)
        self.assertEqual(Binary('0101'), self.bin_5)
        self.assertTrue(self.bin_0 is not abs(self.bin_0))
        self.assertTrue(self.bin_0 is self.bin_0)
        self.assertTrue(self.bin_5 is not abs(self.bin_5))
        self.assertFalse(self.bin_0 is abs(self.bin_0))
        self.assertFalse(self.bin_5 is abs(self.bin_5))
        text = inspect.getsource(Binary.__abs__)
        self.assertTrue('int' not in text)
        

def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestBinary )
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + '%')

if __name__ == "__main__":
    main()