def tuple_of_tuples(lst):
    """
    This function takes a list of integers as its only parameter. 

    The list can be of any length (even or odd).

    Your task is to return a tuple that contains tuple elements  
    in which every two elements from the list make a tuple. 
    If the length of the original list is odd remove the
    middle element. 

    Example:

        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9] #NOTE: odd length 

        tuple returned: 

            ((1,2), (3,4), (6,7) (8,9)) #Like a tuple of tuples! 
                                        #NOTE: that 5 was removed.
    """
    lst1 = []
    if len(lst) % 2 != 0:
        lst.remove(lst[int((len(lst) - 1)/ 2)])
    for i in range(len(lst) - 1):
        if i % 2 == 0:
            lst1.append((lst[i],lst[i + 1]))
    return(tuple(lst1))
    
    

def key_tuple(dictionary):
    """
    This function take a dictionary as its only argument. The dictionary
    will map an integer to a list of elements. 

    Your task is to return a tuple that contains all the keys in the
    dictionary.
    """
    return(tuple([k for k in dictionary.keys()]))
    
def element_remove(tup):
    """
    This function takes a tuple containing integers.

    Your task is to remove the first, middle, and last elements of the 
    tuple and return a new tuple that has the implemented changes.
    If the length of the tuple is less than 3 return the original tuple. 
    If the length is exactly three return an empty tuple.

    Hint: Use list() and tuple() functions. 
    """
    lst1 = []
    for i in range(len(list(tup))):
        if (i != 0) and (i != len(list(tup)) // 2) and (i != len(list(tup)) - 1):
            lst1.append(list(tup)[i])
    if len(lst1) == 3:
        return(())
    elif len(lst1) < 3:
        return tup
    else:
        return(tuple(lst1))

def tuple_dict(fname):
    """
    This function takes a file object as it only parameter.

    The file object is a text file that contains a person's 
    name (first and last) and there age.

        Example:
            Henry Smith, 25
            Henry Smith, 12   #NOTE: the comma after Smith
                              # this is not a csv file!

    Your task is to create and return a dictionary that maps a tuple
    to an integer. YES tuples can be keys in a dictionary because
    they are immutable. Each key tuple will consist of two strings,
    the first and last name of the person in the file. The values that 
    are mapped to the keys is the corresponding age for that person. 
    Since names can repeat in the file you need to check if the person
    already exists in the dictionary. If that is the case, you need to 
    compare the person's current age with the age that is already mapped to 
    the person. If the current age is less than the already mapped age
    then you need to overwrite the old age with the new age. A person can
    not have a negative age! If they have an age that is negative don't add
    them to the dicitonary or if the person already exists in the dictionary
    don't update there age. 
        
        Example:
            the dictionary return would be

            name_age_dict = { ("Henry", "Smith"): 12}

            Note that Henry appeared twice in file text above, with age 25 
            and 12, since 12 < 25 then 12 will be mapped to the tuple 
            not 25.
    """
    d = {}
    with open(fname,'r') as f:
        text = f.read().splitlines()
        for line in text:
            line = line.split(', ')
            if int(line[1]) > 0:
                if tuple(line[0].split(' ')) not in d:
                    d[tuple(line[0].split(' '))] = line[1]
                else:
                    if int(line[1]) < int(d[tuple(line[0].split(' '))]):
                        d[tuple(line[0].split(' '))] =  line[1]
    print(d)

def list_to_set(lst):
    """
    This function takes a list.

    Your task is to remove duplicate elements in the list and return
    a set from the remaining elements in the list.

    If there are no elements in the list return the empty set.
    """
    return(set(lst))

def tuple_of_sets(setA, setB):
    """
    This function takes two sets. 

    Return a tuple that contains the Union, Intersection, and
    Difference of setA and setB. The resulting tuple should only 
    contain 3 sets.
    """
    return(tuple([setA.union(setB),setA.intersection(setB),setA.difference(setB)]))
    

def main():
    """
    Test your functions in main.
    """
    tuple_dict("name_age.txt") # file object for tuple_dict function


if __name__ == '__main__':
    main()