import google, urllib2, bs4, re


def who(query):
    pages = api_stuff(query)
    pattern = "[A-Z]{1}[a-z]{2,} [A-Z]{1}[a-z]{1,}"
    names = max_freq(pages, pattern)


def max_freq(pages, pattern):
    d = {}
    for page in pages:
        result = re.findall(pattern, page)
        for name in result:
            if name not in d:
                d["name"] = 1
            else:
                d["name"] += 1
    max_key = get_max(d)
    return max_key

                    
def get_max(d):
    max_val = max(d.values())
    keys = []
    for x,y in d.items():
        if y == max_val:
            keys.append(x)
    return keys


if __name__ == "__main__":

    d = { "hell": 2, "potato": 15,
          "cow": 15, "chain saw": 2 }
    
    print get_max(d)
            
