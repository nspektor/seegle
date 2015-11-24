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

def when(query):
    pages=api_stuff(query)
    regexp_std='(?<month>[A-Z][a-z]{2,8}) (?<day>\d{1,2}),? (?<year>\d{1,4})'
    regexp_era='(\d{1,10}) (BC|AD)'
    d={}
    result=[]
    for page in pages:
        result=result+findall(regexp_std,page)+findall(regexp_era,page)
    for name in result:
        if name in d:
            d[name]+=1
        else:
            d[name]=1

