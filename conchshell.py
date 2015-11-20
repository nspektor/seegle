import google, urllib2, bs4, re
def api_stuff(query):
    pages = google.search(query,num=10,start=0,stop=10)
    texts = []
    results = []
    for r in pages:
        results.append(r)
        url = urllib2.urlopen(results[r])
        result_page = url.read().decode('ascii')
        soup = bs4.BeautifulSoup(result_page)
        raw = soup.get_text(result_page)
        text = re.sub("[\t\n ]+",' ',raw)
        texts.append(text)
    return texts

