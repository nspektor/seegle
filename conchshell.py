import google, urllib2, bs4, re
from threading import Thread
from collections import Counter


stop_words = []

def load_stop_words():
    """reads stop-words into dictionary from static
    """
    global stop_words
    file = open("static/stop-word-list.csv", 'r')
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
    pages = google.search(query,num=20,start=0,stop=20)
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
    pattern = "([A-Z]([a-z]+))?[A-Z]([a-z]+|\.) ([A-Z]')?([A-Z]([a-z]+))?[A-Z]([a-z]+|\.)"

    freq = get_max_freq(pages, pattern)
    points = get_points(pages, pattern)
   
    #print "Pages: %d" % len(pages)
    l1 = max_val(freq)
    l2 = max_val(points)
    """
    print "By frequency: "
    print l1
    print "By points: "
    print l2
    """
    l1 += l2

    if not l1:
        return "I don't know, sorry."
    
    count = Counter(l1)
    common = count.most_common(1)
    
    return common[0][0]


def when(query):
    pages=api_stuff(query)
    regexp_std='([A-Z][a-z]{2,8}) (\d{1,2}),? (\d{1,4})'
    #regexp_std='[A-Z]'
    regexp_era='(\d{1,10}) (BC|AD)'
    l = get_max_freq(pages, regexp_std)
    """
    d={}
    result=[]
    for page in pages:
        result=result+re.findall(regexp_std,page)+re.findall(regexp_era,page)
    for name in result:
        if name in d:
            d[name]+=1
        else:
            d[name]=1
    """
    return l


def contains(phrase, l):
    words = phrase.split(" ")
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
      A dictionary of matches whose values reflect the frequency
    """
    d = {}
    for page in pages:
        #result = re.findall(pattern, page)
        it = re.finditer(pattern, page)
        for match in it:
            first = match.group(0)
            if first not in d:
                d[first] = 1
            else:
                d[first] += 1

    for key in d:
        for page in pages:
            pattern = pattern[pattern.find(" ")+1:]
            l = re.findall(pattern, page)
            words = key.split()
            for word in words:
                while (word in l):
                    d[key] += 1
                    index = l.index(word)
                    l.pop(index)
                
    return d
   

def get_points(pages, pattern):
    d = get_max_freq(pages, pattern)
    total_pages = len(pages)
   
    for key in d:
        page_count = 0
        for page in pages:
            if key in page:
                page_count += 1
        d[key] = (float(page_count) / total_pages) * d[key]

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
            d.pop(key)

    if not d:
        return []
    
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
    query=query.lower()
    if "who" in query:
        return who(query)
    elif "when" in query:
        return when(query)
    else:
        return "invalid"
    
if __name__ == "__main__":

    #print who("Who wrote The Things They Carried?")
    #print who("Who created Facebook?")
    print who("Who played the first Spiderman?")
    #print who("Who said \" Let them eat cake\"?")
    #print find_results("Who played Spiderman?")
    #print find_results("Who killed Julius Caesar?")
    #print when("When did World War II start?")        

   
           
           


