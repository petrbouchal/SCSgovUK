__author__ = 'petrbouchal'

from lib_DGUK import SavePretty,DGUKopenAndParse, WriteDict

limit=1000
searchterm='organogram'

action = 'package_search'
apidata = {'rows':limit,'q':searchterm}

allpackages = DGUKopenAndParse(action,apidata)

packagerows = []
resrows = []

packfile=open('/output/','w+')
resfile=open('/output/','w+')

rescount = csvcount = nodatecount = xlscount = 0
for dgpack in allpackages['results']:
    SavePretty(dgpack)
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