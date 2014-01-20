__author__ = 'petrbouchal'

import urllib2
import json

apibase = 'http://data.gov.uk/api/3'
limit=1000
searchterm='organogram'

action = '/action/package_search'
query = apibase + action + '?q=' + searchterm + '&rows=' + str(limit)
print(query)

data = urllib2.urlopen(query).read()
jdata=json.loads(data)

rescount = csvcount = nodatecount = xlscount = 0
for dgpack in jdata['result']['results']:
    for dgres in dgpack['resources']:
        # pprint(dgres)
        # print dgres['date']
        print dgres['format']
        try: print dgres['date']
        except (KeyError):
            print('no date')
            nodatecount += 1
        rescount += 1
        if dgres['format'].lower()=='csv': csvcount +=1
        if dgres['format'].lower()=='xls': xlscount +=1

print(rescount)
print(csvcount)
print(xlscount)
print(nodatecount)