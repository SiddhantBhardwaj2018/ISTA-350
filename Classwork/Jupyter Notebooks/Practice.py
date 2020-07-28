
def word_count(string,insensitive = True):
    if insensitive:
        string = string.lower()
    words = string.split(' ')
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] = 0
        else:
            word_counts[word] += 1
    return pd.Series(word_counts).sort_index()
    
def is_symmetric(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix.columns)):
            if matrix.iloc[row,column] != matrix.iloc[column,row]
                return False
    return True
    
def is_symmetric(matrix):
    for row in matrix.index:
        for column in matrix.columns:
            if matrix.loc[row,column] != matrix.loc[column,row]:
                return False
    return True
    
def is_symmetric(matrix):
    return all((matrix == matrix.T).all())
    
def letter_count(text,insensitive = True):
    smalls = 'abcdefghijklmnopqrstuvwxyz'
    if insensitive:
        letters = list(small)
        text = text.lower()
    else:
        letters = list(small +  smaller.upper())
    s = pd.Series(0,letters)
    for ch in s:
        if ch.isalpha():
            s.loc[ch] += 1
    return s
    
def sum_rows(df,string):
    if not string:
        return sum(df.sum())
    total = 0
    for row_label in df.index:
        if string in row_label:
            total += sum(df.loc[row_label])
    return total
    

    
    