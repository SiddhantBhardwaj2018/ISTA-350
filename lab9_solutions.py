import requests

def get_page(url):
    """
    This function takes a string that represents a url.
    
    Your task is to send a request from the url given as a parameter.
    From this request, return a string containing the content of the request.
    """
    r = requests.get(url)
    return r.text  #or str(r.content)

def how_bold(c):
    """
    This function takes a string containing the content of a webpage.
    
    Using the provided string, return a count of how many times 
    the string '<b>' (the bold tag) appears in the page.
    """
    return c.count('<b>')

def get_title(c):
    """
    This function takes a string containing the content of a webpage.
    
    Using the provided string, return the title of the page.
    The title is enclosed between the '<title>' and '</title>' tags.
    """
    start = c.find('<title>') + 7
    end = c.find('</title>')
    title = str(c[start:end])
    return title

def upgrade_python(c):
    """
    This function takes a string containing the content of a webpage.
    
    Return a new copy of the content string, but with
    all instances of "Python" replaced with "Anaconda".
    Maintain the same capitalization in the replacement words as with the originals.
    """
    newc = c
    newc = newc.replace('Python', 'Anaconda').replace('python', 'anaconda')
    return newc
            
def main():
    c = get_page('http://www.pythonchallenge.com/')
    print(c,'\n')
    print('number of <b>\'s:',how_bold(c),'\n')
    print('the title is:',get_title(c),'\n')
    print(upgrade_python(c))
    
if __name__ == '__main__':
    main()
