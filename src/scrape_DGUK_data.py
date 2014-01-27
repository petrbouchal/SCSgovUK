__author__ = 'petrbouchal'

from lib_DGUK import SavePretty,DGUKopenAndParse, WriteDict
import os
from datetime import datetime

filedatestringlong = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')

dirstems = ['packagesjson','resourcesjson','packagesdata','resourcesdata']
for i in dirstems:
    rawdir = '../output/' + i + '/' + i + '_' + filedatestringlong
    os.makedirs(rawdir)


limit=1000
searchterm='organogram'

action = 'package_search'
apidata = {'rows': limit,'q': searchterm}

allpackages = DGUKopenAndParse(action,apidata)

packagerows = []
resourcerows = []

packagefile='../output/packages_'+filedatestringlong + '.csv', 'w+'
resourcefile='../output/resources_'+filedatestringlong + '.csv', 'w+'

rescount = csvcount = nodatecount = xlscount = 0
for dgpack in allpackages['results']:
    SavePretty(dgpack,'packagesjson/packagesjson_'+filedatestringlong + '/' + dgpack['id']+'_'+filedatestringlong)
    try: pack_temporal_coverage_to=dgpack['last_major_modification'],
    except KeyError: pack_last_major_modification = 'None'
    try: pack_temporal_coverage_to=dgpack['temporal_coverage_to'],
    except KeyError: pack_temporal_coverage_to = 'None'
    try: pack_temporal_coverage_from=dgpack['temporal_coverage_from'],
    except KeyError: pack_temporal_coverage_from = 'None'
    try: pack_unpublished=dgpack['unpublished'],
    except KeyError: pack_unpublished = 'None'
    packagerow = {
        'id':dgpack['id'],
        'title':dgpack['title'],
        'organisation_name':dgpack['organization']['name'],
        'organisation_id':dgpack['organization']['id'],
        'num_resources':dgpack['num_resources'],
        'last_major_modification':pack_last_major_modification,
        'unpublished':pack_unpublished,
        'notes':dgpack['notes'],
        'title':dgpack['title'],
        'temporal_coverage_to':pack_temporal_coverage_to,
        'temporal_coverage_from':pack_temporal_coverage_from
    }
    packagerows.append(packagerow)
    for dgres in dgpack['resources']:
        # pprint(dgres)
        # print dgres['date']
        print dgres['format']
        try:
            print dgres['date']
        except KeyError:
            print('no date')
            nodatecount += 1
        rescount += 1
        dgresdata = DGUKopenAndParse('resource_show',{'id':dgres['id']})
        SavePretty(dgresdata,'resourcesjson/resourcesjson_'+filedatestringlong+'/' + dgres['id']+'_'+filedatestringlong)
        resourcerow= {
            'id':dgresdata['id'],
            'last_modified':dgresdata['last_modified'],
            'mimetype':dgresdata['mimetype'],
            'name':dgresdata['name'],
            'format':dgresdata['format'],
            'description':dgresdata['description'],
            'created':dgresdata['created'],
            'url':dgresdata['url'],
        }
        if dgres['format'].lower()=='csv': csvcount += 1
        if dgres['format'].lower()=='xls': xlscount += 1
        resourcerows.append(resourcerow)

WriteDict(packagefile,packagerows)
WriteDict(resourcefile,resourcerows)

print(rescount)
print(csvcount)
print(xlscount)
print(nodatecount)