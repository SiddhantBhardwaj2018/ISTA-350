'''
Name - Siddhant Bhardwaj
Date - 4/9/2020
ISTA 350 HW6
Collaborators - Vibhor Mehta
'''

from bs4 import BeautifulSoup
import requests,zlib,os

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