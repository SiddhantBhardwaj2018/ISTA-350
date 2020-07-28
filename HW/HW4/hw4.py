'''
Name - Siddhant Bhardwaj
Section Leader - Gwen Hopper
ISTA 350 HW4
Date - 2/29/2020
Collaborators - Vibhor Mehta
'''
import numpy as np
class Binary:
    def __init__(self,str1 = '0'):
        '''
        This method takes in a string parameter with a default of '0'. It can be empty or comprised of 0s and 1s and should
        be 16 characters or less.Else,it raises RuntimeError.It creates an instance variable called bit_array which has 0s and 
        1s in the same order as in the argument.
        '''
        if str1 == '' or ((set(str1) == {'0','1'} or set(str1) == {'0'} or set(str1) == {'1'}) and len(str1) <= 16):
            if str1 == '':
                self.bit_array = np.zeros(16)
            elif str1[0] == '1':
                x = np.ones(16 - len(str1))
                y = [int(i) for i in str1]
                z = np.array(y)
                self.bit_array = np.concatenate((x,z))
            else:
                x = np.zeros(16 - len(str1))
                y = [int(i) for i in str1]
                z = np.array(y)
                self.bit_array = np.concatenate((x,z))
        else:
            raise RuntimeError 
     
    def __eq__(self,object):
        '''
        This method takes in a Binary object and returns true if it is the same else returns False.
        '''
        if all(self.bit_array == object.bit_array):
            return True
        return False     
    
    def __repr__(self):
        '''
        This returns a 16 character string representing the  fixed width binary string.
        '''
        string = ''
        for i in self.bit_array:
            string += str(int(i))
        return string            
        
    def __add__(self,other):
        '''
        This method takes a Binary object as an argument and returns the sum of self and the argument.
        '''
        result = np.empty(16,dtype = int)
        carry = 0
        for i in range(15,-1,-1):
            bit_sum = self.bit_array[i] + other.bit_array[i] + carry
            result[i] = bit_sum % 2
            carry = bit_sum > 1
        if self.bit_array[0] ==  other.bit_array[0] != result[0]:
            raise RuntimeError("Binary: Overflow")
        return Binary("".join([str(i) for i in result]))
        
        
    def __neg__(self):
        '''
        This method returns the negative of the self object.
        ''' 
        bin_new = Binary('')
        for i in range(len(self.bit_array)):
            bin_new.bit_array[i] =  1 - self.bit_array[i]
        return bin_new + Binary('01')
        
    def __sub__(self,other):
        '''
        This method takes in a Binary object as argument and returns the difference between self and the object.
        '''
        return self + (-other)
        
    def __int__(self):
        '''
        This method returns the decimal value of the Binary object.
        '''
        value = 0
        lst = list(self.bit_array)[::-1]
        if lst[-1] != 1:
            for i in range(len(lst)):
                value += (2 ** i) * lst[i]
        else:
            for i in range(len(lst) - 1):
                value += (2 ** i) * lst[i]
            value += (-1) * (2 ** (len(lst) - 1)) 
        return int(value)
        
    def __lt__(self,other):
        '''
        This method takes Binary object as argument and returns True if self < other
        else returns False.
        '''
        if self.bit_array[0] != other.bit_array[0]:
            if self.bit_array[0] == 1:
                return True
            else:
                return False
        else:
            return bool((self - other).bit_array[0])
            
    def __abs__(self):
        '''
        This method returns a Binary object representing the absolute value of the self.
        '''
        if self.bit_array[0] == 0:
            return self + Binary()
        else:
            return -self
            