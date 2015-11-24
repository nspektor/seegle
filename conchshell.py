import google, urllib2, bs4, re

stop_words = []

def load_stop_words():
    """
    reads stop-words into dictionary from static
    """
    global stop_words
    file = open("static/stop-word-list.csv", 'r')
    for line in file:
        l = line.split(", ")
        stop_words += l
    file.close()

    
def api_stuff(query):
    pages = google.search(query,num=10,start=0,stop=10)
    texts = []
    for r in pages:
        try:
            url = urllib2.urlopen(r)
            result_page = url.read().encode("ascii", 'ignore')
            soup = bs4.BeautifulSoup(result_page, "html.parser")
            raw = soup.get_text()
            text = re.sub("[\t\n ]+",' ', raw)
            texts.append(text)
        except:
            pass
    return texts


def who(query):
    pages = api_stuff(query)
    pattern = "[A-Z]{1}[a-z]{2,} [A-Z]{1}[']?[A-Z]?[a-z]{1,}"
    names = get_max_freq(pages, pattern)
    #if there is more than one name in names
    #do some more stuff
    #if len(names) == 1:
        #return names[0]
   
    return names

def contains(string, l):
    words = string.split(" ")
    for word in words:
        #word = word.lower()
        if word.lower() in l:
            return True
    return False

    

def get_max_freq(pages, pattern):
    """Tallies up matches to pattern within pages and calculates the match with the highest frequency

    Arguments:
      pages: A list of strings holding text 
      pattern: a regex string for matching

    Returns:
      A list of keys with the max occurences
    """
    if not stop_words:
        load_stop_words()
        
    d = {}
    for page in pages:
        result = re.findall(pattern, page)
        for name in result:
            #print name
            if not contains(name, stop_words):
                if name not in d:
                    d[name] = 1
                else:
                    d[name] += 1
    maxx = max_val(d)
    return maxx
   


def max_val(d):
    """finds the key with the largest corresponding value in dictionary d

    Arguments: 
      d: a dictionary of strings whose values reflect frequency

    Return:
      A list of keys with the max occurences (in case there are multiple)
    """
    max_val = max(d.values())
    keys = []
    for x,y in d.items():
        if y == max_val:
            keys.append(x)
    return keys


if __name__ == "__main__":

    print who("Who wrote The Things They Carried?")
    #print who("Who said \" Let them eat cake\"?")
            
