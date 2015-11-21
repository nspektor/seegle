import google, urllib2, bs4, re


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
