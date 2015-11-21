import google, urllib2, bs4, re


def when(query):
    pages=api_stuff(query)
    regexp_std='(?<month>[A-Z][a-z]{2,8}) (?<day>\d{1,2}),? (?<year>\d{1,4})'
    regexp_era='(\d{1,10}) (BC|AD)'
    d={}
    for page in pages:
        result_std=findall(regexp_std,page)
        result_era=findall(regexp_era,page)
        for name in result_std:
            if name in d:
                d[name]+=1
            else:
                d[name]=1
        for name in result_era:
            if name in d:
                d[name]+=1
            else:
                d[name]=1
