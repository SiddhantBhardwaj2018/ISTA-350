    def __add__(self, other):
        """
        Return a new Binary instance that = self + other.
        Raises a runtime error on overflow.
        """
        result_num = np.empty(16, dtype=int)
        carry = 0
        
        for i in range(15, -1, -1):
            bit_sum = self.bit_array[i] + other.bit_array[i] + carry
            result_num[i] = bit_sum % 2
            carry = bit_sum > 1
            
        if self.bit_array[0] == other.bit_array[0] != result_num[0]:
            raise RuntimeError("Binary: overflow")
                
        return Binary(''.join([str(i) for i in result_num]))
        
