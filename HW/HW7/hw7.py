'''
Name - Vibhor Mehta 
Date - 4/23/2020
ISTA 350 HW7
Collaborators - Siddhant Bhardwaj
'''

from bs4 import BeautifulSoup
import requests,zlib,os,numpy as np,json

def get_soup(url = None,fname = None,gzipped = False):
    '''
    This function takes in 3 arguments - url,fname which default to None and gzipped which defaults
    to False. If the fname is not None, it returns a BeautifulSoup object which opens a filename.
    If the url is None, it raises a RunTime error else server = requests.get(url). If gzipped is true,
    it decompresses the file and and returns the BeautifulSoup object for the new variable.
    '''
    if fname:
        return BeautifulSoup(open(fname))
    if not url:
        raise RuntimeError("Either url or filename must be specified.")
    server = requests.get(url)
    if gzipped:
        new_var = zlib.decompress(server.content,16 + zlib.MAX_WBITS)
        return BeautifulSoup(new_var)
    return BeautifulSoup(server.content)
    
def save_soup(fname,soup_obj):
    '''
    This function writes a textual representation of a soup object to a text file.
    '''
    string1 = repr(soup_obj)
    with open(fname,'w') as file:
        file.write(string1)
        
def scrape_and_save():
    '''
    This function soupifies the contents of a webpage and saves them to a text file.
    '''
    soup_obj1 = get_soup(url = 'http://www.wrcc.dri.edu/WRCCWrappers.py?sodxtrmts+028815+por+por+pcpn+none+msum+5+01+F')
    save_soup("wrcc_pcpn.html",soup_obj1)
    soup_obj2 = get_soup(url = "https://wrcc.dri.edu/WRCCWrappers.py?sodxtrmts+028815+por+por+mint+none+mave+5+01+F")
    save_soup("wrcc_mint.html",soup_obj2)
    soup_obj3 = get_soup(url = "http://www.wrcc.dri.edu/WRCCWrappers.py?sodxtrmts+028815+por+por+maxt+none+mave+5+01+F")
    save_soup("wrcc_maxt.html",soup_obj3)
    
def is_num(string):
    '''
    This function checks if a string is a number.
    '''
    d = dict()
    for elem in string:
        if elem not in d:
            d[elem] = 1
        else:
            d[elem] += 1
    if '.' in string or '-' in string:
        if '.' in string:
            if d['.'] > 1:
                return False
        if '-' in string:
            if d['-'] > 1:
                return False
            if string[0] != '-':
                return False
        return True
    else:
        return string.isdigit()
        
       
def load_lists(soup_obj,flags):
    '''
    This function takes in a soup object and creates a list of lists.
    '''
    data = [[] for i in range(14)]
    rows = soup_obj.find_all('tr')[1:-7]
    for row in rows:
        tds = row.find_all('td')
        j = 0
        for i in tds:
            text = i.get_text()
            if j == 0:
                if text.isdigit():
                    data[0].append(int(text))
                    j += 1         
            elif is_num(text):
                data[j].append(float(text))
                j += 1
                
            elif text == '-----':
                data[j].append(flags)
                j += 1
    return data
            

def replace_na(lst,row,col,flag,precision):
    '''
    This function calculates in place of a flag 
    the average of 5 numbers behind and ahead of it.
    '''
    mean = 0
    count = 0
    num1 = col - 5
    if col - 5 < 0:
        num1 = 0
    for i in lst[row][num1:col + 6]:
        if i != flag:
            mean += i
            count += 1            
    
    return round(mean / count,precision)
    
def clean_data(lst,flag,precision):
    '''
    This function cleans data.
    '''
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == flag:
                lst[i][j] = replace_na(lst,i,j,flag,precision = 5)
                
def recalculate_annual_data(lst,bool1 = False,precision = 5):
    '''
    This function recalculates annual data.
    '''
    for i in range(len(lst[-1])):
            mini = [row[i] for row in lst[1:-1]]
            total = round(sum(mini),precision)            
            if not bool1:
                lst[-1][i] = total
            else:
                lst[-1][i] = round(total / len(mini),precision)
                
def clean_and_jsonify(lst,flag,precision = 5):
    '''
    This function cleans and jsonifies list of lists.
    '''
    for file in lst:
        soup_item = get_soup(fname = file)
        lst_item = load_lists(soup_item,flag)
        clean_data(lst_item,flag,precision)
        if 'pcpn' in file:
            recalculate_annual_data(lst_item,False,precision)
        else:
            recalculate_annual_data(lst_item,True,precision)
        with open(file[:file.index('.')] + '.json','w') as fp:
            json.dump(lst_item,fp)
            


def main():
    '''
    This main function checks if the check_file is present in the directory and if it is not there, it scrapes
    and saves it to the file.
    '''
    check_file = "wrcc_pcpn.html"
    files = os.listdir()
    if check_file not in files:
        print('---- scraping and saving ----')
        scrape_and_save()
    fnames = ['wrcc_pcpn.html','wrcc_maxt.html','wrcc_mint.html']
    clean_and_jsonify(fnames,-999,2)