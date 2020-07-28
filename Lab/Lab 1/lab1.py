import numpy as np, re
import pandas as pd

###Classes Review:

class BankCustomer:
    '''
    This class creates a BankCustomer object. A BankCustomer has a name, 
    personal identification number, transaction log and total balance ($).
    '''

    def __init__(self, name, id_num):
        '''
        This method takes in a string (name) that represents the bank 
        customer's name and an integer (id_num) that represents the customer's
        identification number.

        Your task is to initialize four instance variables: name, id, 
        transaction_history and total.

        Store the name parameter in the name instance variable and the id_num 
        parameter in the id instance variable.

        Your transaction_history instance variable should be a dictionary. In 
        your dictionary map the string, "Deposits", to an empty list and map
        another string, "Withdrawals", to an empty list. Again, you create these
        mappings in the dictionary!  

        Your total instance variable should be initialized to 0. 
        '''
        self.name = name
        self.id_num = id_num
        self.transaction_history = {'Deposits':[],'Withdrawals':[]}
        self.total = 0
        
    def __repr__(self):
        '''
        This method never takes in a parameter!

        Your task is to create and return a string. 

        You will first greet the Customer by saying Hello followed by there name. 

        Then, you will include the following string:
        "Your bank history is as follows: ". 

        After that, iterate through your transaction_history dictionary. The 
        idea here is to use nested for loops. First iterate through the keys in 
        the dictionary for each key print the key followed "Log: ". Then in the 
        inner loop iterate through the list that is mapped to the current key 
        and print out each item in the list on separate lines. DO NOT hard code 
        the strings "Withdrawals" or "Deposits" in your repr code.  

        Finally, include the string "Your current Balance: " followed by
        the customer's current total.        

            Example only:

                Hello Henry Smith! #Don't hard code the name "Henry Smith"
                Your bank history is as follows: 

                Withdrawals Log:
                100
                50              # NOTE: Withdrawals and Deposits can show up in
                                #       any order do not hard code the event!!
                Deposits Log:
                200

                Your current Balance: $50
        '''
        print("Hello "+self.name+"! ")
        print("Your bank history is as follows: ")
        print()
        print("Withdrawals Log:")
        for element in self.transaction_history['Withdrawals']:
            print(element)
        print("Deposits Log:")
        for element in self.transaction_history['Withdrawals']:
            print(element)
        print()
        print("Your current Balance: " + str((self.transaction_history['Deposits'][-1] -  self.transaction_history['Withdrawals'][-1])))
        
    def get_id_num(self):
        '''
        This method takes no parameters.

        Your task is to return the customer's identification number.
        '''
        return self.id_num
        
        
        
        
    def deposit(self, amount):
        '''
        This method takes one integer parameter, amount, which represents a 
        monetary amount.

        Your task is to append to the list that is mapped to the key "Deposits"
        and adjust the total instance variable accordingly. 
        '''
        self.transaction_history['Deposits'].append(amount)
        self.total = sum(self.transaction_history['Deposits'])
        
    def withdrawal(self, amount):
        '''
        This method takes one integer parameter, amount, which represents a 
        monetary amount.

        Your task is to append to the list that is mapped to the key 
        "Withdrawals" and adjust the total instance variable accordingly.
        '''
        self.transaction_history['Withdrawals'].append(amount)
        self.total = self.total - sum(self.transaction_history["Withdrawals"])
        
###RegEx:

def get_numbers(file: str):
    '''
    Given the text file and using regular expressions, extract all of the valid phone numbers
    from the text file and return them in a list. Account for the below phone number formats:

    (888)-888-8888
    888-888-8888
    (888) 888-8888

    Parameters:
    :file: filename - file contains phone numbers and email addresses

    Returns:
    A list containing the phone numbers
    '''
    
    lst = re.findall(r'^([0-9])-([0-9])-([0-9])',file)
    return(lst)

def get_emails(file: str):
    '''
    Given the text file and using regular expressions, extract all of the valid email addresses
    from the text file and return them in a list.

    Parameters:
    :file: filename - file contains email addresses and phone numbers

    Returns:
    A list containing the email addresses
    '''
    lst1 = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",file)
    return(lst1)
    
def main():
    '''
    Create a BankCustomer instance. Give them a name and personal identification
    number. Make use of the methods in your BankCustomer (make your customer 
    wealthy or broke). Once you have finished depositing and withdrawing 
    virtual and insignificant money, print a complete summary of your 
    BankCustomer's transaction history and current balance. 
    '''
    customer = BankCustomer("Ram Singh",2344708)
    customer.deposit(100)
    customer.deposit(500)
    customer.deposit(1000000000)
    customer.withdrawal(100)
    customer.__repr__()
    print(get_emails("iwalktheline3.txt"))
    print(get_numbers("iwalktheline3.txt"))
if __name__ == '__main__':
    main()