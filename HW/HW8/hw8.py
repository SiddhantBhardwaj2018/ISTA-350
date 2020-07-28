'''
Name - Vibhor Mehta
Date - 4/30/2020
ISTA 350 HW8
Collaborators - Siddhant Bhardwaj
'''

from bs4 import BeautifulSoup
import requests,zlib,os,numpy as np,json,pandas as pd
import matplotlib.pyplot as plt

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
    This is the is_num function.
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
    This is the load_lists function.
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
    This is the replace_na function.
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
    This is the clean_data function.
    '''
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == flag:
                lst[i][j] = replace_na(lst,i,j,flag,precision = 5)
                
def recalculate_annual_data(lst,bool1 = False,precision = 5):
    '''
    This is the recalculate_annual_data function.
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
    This is the clean_and_jsonify function.
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

def get_panda(fname):
    '''
    This is the get_panda function.
    '''
    with open(fname,'r') as file:
        new = json.load(file)
    df = pd.DataFrame(data = new[1:],index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Ann'],columns = [i for i in range(1894,2009)])
    return df
    
def get_stats(df):
    '''
    This is the get_stats function.
    '''
    lst = []
    means = df.mean(1).values
    sigma = df.std(1,ddof = 0).values
    s = df.std(1,ddof = 1).values
    cols = pd.Series(df.columns.values)
    r =  [pd.Series(df.loc[s].values).corr(cols) for s in df.index]
    return pd.DataFrame(data = [means,sigma,s,r],index = ['mean','sigma','s','r'],columns = df.index)
    
def print_stats(fname):
    '''
    This is the print_stats function.
    '''
    print('----- Statistics for ' + fname + ' -----\n')
    df = get_panda(fname)
    new = get_stats(df)
    print(new)
    print()
    
def smooth_data(df,precision = 5):
    '''
    This is the smooth_data function.
    '''
    new_df = df.copy()
    for i in range(len(df)):
        for j in range(len(df.columns)):
            sum1  = 0
            count = 0
            if (j - 5) < 0:
                v = j
                j = 0
                for k in df.iloc[i,j:v + 6]:
                    sum1 += k
                    count += 1
                new_df.iloc[i,v] = round(sum1 / count,precision)
            else:
                for k in df.iloc[i,(j-5):(j + 6)]:
                    sum1 += k
                    count += 1
                new_df.iloc[i,j] = round(sum1 / count,precision)
    return new_df

def make_plot(fname,mon = None,precision = 5):
    '''
    This is the make_plot function.
    '''
    df = get_panda(fname)
    smooth_df = smooth_data(df)
    transposed = smooth_df.transpose()
    transposed_df = df.transpose()
    if mon is None:
        var1 = transposed_df.plot(subplots = True,title = fname,legend = None,yticks = [])
        for i in range(len(transposed.columns)):
            var1[i].set_ylabel(transposed.columns[i])     
            transposed.iloc[:,i].plot(ax = var1[i])
    else:
        var2 = transposed_df.loc[:,mon].plot(title = fname + ':' + mon,legend = None,yticks = [])
        transposed.loc[:,mon].plot(ax = var2)
    

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
    for fname in fnames:
        json_fname = fname.split('.')[0] + '.json'
        print_stats(json_fname)
        make_plot(json_fname,precision = 2)
    plt.figure()
    make_plot(fnames[0].split('.')[0] + '.json','Jan')
    plt.show()
    
if __name__ == "__main__":
    main()