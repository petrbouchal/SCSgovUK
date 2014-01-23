__author__ = 'bouchalp'

import urllib2
import json
from pprint import pprint
from lib_DGUK import SavePretty

apibase = 'http://data.gov.uk/api/3'
limit = 1000

searchterm = ''

action = '/action/organization_list?all_fields=true'
query = apibase + action + '&rows=' + str(limit)
print(query)

data = urllib2.urlopen(query).read()
jdata = json.loads(data)
pprint(jdata['result'])

orgaction = '/action/organization_show'

for org in jdata['result']:
    orgquery = apibase + orgaction + '?id=' + org['id']
    print(orgquery)
    orgdata = urllib2.urlopen(orgquery).read()
    jorgdata = json.loads(orgdata)
    print(jorgdata['result']['title'])
    SavePretty(jorgdata,'output/'+'org_'+jorgdata['result']['name']+'.json')

