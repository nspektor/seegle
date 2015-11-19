import google, urllib2, bs4, re
def api_stuff():
    pages = google.search(q,num=10,start=0,stop=10)
    
    results = []
    for r in pages:
        results.append(r)
        url = urllib2.urlopen(results[r])
        result_page = url.read().decode('ascii')
        soup
