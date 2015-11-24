import google, urllib2, bs4, re

def api_stuff(query):
    pages = google.search(query,num=10,start=0,stop=10)
    texts = []

    for r in pages:
        try:
           
            url = urllib2.urlopen(r)
            result_page = url.read().decode('ascii', 'ignore')
            soup = bs4.BeautifulSoup(result_page, "html_parser")
            raw = soup.get_text()
            text = re.sub("[\t\n ]+",' ',raw)
            texts.append(text)
        except:
            pass
    return texts

