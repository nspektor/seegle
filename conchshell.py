import google, urllib2, bs4, re
import random
from threading import Thread



stop_words = []
answers = [ "It is certain", "It is decidedly so",
            "Without a doubt", "Yes, definitely",
            "You may rely on it", "As I see it, yes",
            "Most likely", "Outlook good",
            "Yes", "Signs point to yes",
            "Reply hazy, try again", "Ask again later",
            "Better not tell you now", "Concentrate and ask again",
            "Cannot predict now", "Don't count on it",
            "My reply is no", "My sources say no",
            "Outlook not so good", "Very doubtful" , "42"]

def load_stop_words():
    """
    reads stop-words into dictionary from static
    """
    global stop_words
    file = open("static/stop3.csv", 'r')
    for line in file:
        l = line.split(", ")
        stop_words += l
    file.close()


def process_page(page, l):
    """Opens url and uses Beautiful Soup to extract text
    
    Arguments:
      page: a url string
      l: the list to append the result to
    """
    text = None
    try:
        url = urllib2.urlopen(page)
        result_page = url.read().encode("ascii", 'ignore')
        soup = bs4.BeautifulSoup(result_page, "html.parser")
        raw = soup.get_text()
        text = re.sub("[\t\n ]+",' ', raw)
    except:
        pass

    if text:
        l.append(text)

        
def api_stuff(query):
    """Extract text from several urls using threads
    
    Arguments:
      query: a string containing a question
    Returns:
      texts: a list of text strings, one for each url page
    """
    pages = google.search(query,num=10,start=0,stop=20)
    threads = []
    texts = []
    
    for page in pages:
        threads.append(Thread(target = process_page,
                              args = (page, texts)))
        
    [t.start() for t in threads]
    [t.join() for t in threads]
 
    return texts


def who(query):
    pages = api_stuff(query)
    pattern = "(([A-Z]([a-z]+))?[A-Z]([a-z]+|\.) ([A-Z]')?([A-Z]([a-z]+))?[A-Z]([a-z]+|\.))"

    freq = get_max_freq(pages, pattern)
    maxx = max_val(freq)
   
    if not maxx:
        return random.choice(answers)
    
    return maxx[0]


def when(query):
    pages=api_stuff(query)
    #regexp_std='([A-Z][a-z]{2,8}) (\d{1,2}),? (\d{1,4})'
    regexp="([A-Z][a-z]{2,8}) (\d{1,2}),? (\d{1,4})|(\d{1,10}) (BC|AD)|in (\d{1,6})"
    #regexp_era='(\d{1,10}) (BC|AD)'
    l = get_max_freq(pages, regexp)
    maxx = max_val(l)
    
    if not maxx:
        return random.choice(answers)
    
    return maxx[0]


def contains(string, l):
    words = string.split(" ")
    for word in words:
        if word.lower() in l:
            #print "word: "+word.lower()
            return True
    return False

    

def get_max_freq(pages, pattern):
    """Tallies up matches to pattern within pages and calculates the match with the highest frequency

    Arguments:
      pages: A list of strings holding text 
      pattern: a regex string for matching

    Returns:
      A dictionary of matches whose values reflect the frequency

    >>> get_max_freq(["John Smith is not James Smith.","Julius Caesar was the Roman emperor."], "[A-Z]{1}[a-z]{2,} [A-Z]{1}[']?[A-Z]?[a-z]{1,}")
    {"John Smith":1, "James Smith": 1, "Julius Caesar":1}
    >>> get_max_freq(["World War Two began on September 1, 1939.", "The Roman Empire fell in 476 AD."], "([A-Z][a-z]{2,8}) (\d{1,2}),? (\d{1,4})")
    {"September 1, 1939":1}
    >>> get_max_freq(["World War Two began on September 1, 1939.", "The Roman Empire fell in 476 AD."], "(\d{1,10}) (BC|AD)")
    {"476 AD"}
    """
    d = {}
    for page in pages:
        it = re.finditer(pattern, page)
        for match in it:
            first = match.group(0)
            if first not in d:
                d[first] = 1
            else:
                d[first] += 1

    return d
   
   


def max_val(d):
    """finds the key with the largest corresponding value in dictionary d

    Arguments: 
      d: a dictionary of strings whose values reflect frequency

    Return:
      A list of keys with the max occurences (in case there are multiple)
    """
    if not stop_words:
        load_stop_words()

    for key in d.keys():
        if contains(key, stop_words):
            #print 'out: '+ key
            d.pop(key)
            
    max_val = max(d.values())
    keys = []
    for x,y in d.items():
        if y == max_val:
            keys.append(x)
    return keys


def find_results(query):
    """Parses user query to determine which search to perform, then performs the search

    Arguments:
     query: a string that is the user's query input

    Return:
     If the query is valid, return results of the query. Else, return error
     
    """
    q=query.lower()
    if "who" in q:
        return who(query)
    elif "when" in q:
        return when(query)
    else:
        return random.choice(answers)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #print who("Who wrote The Things They Carried?")
    #print who("Who said \" Let them eat cake\"?")
    #print who("Who was emperor of Rome?")
    #print when("When did World War II start?")        

       
           
           
           


