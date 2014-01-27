__author__ = 'bouchalp'

from lib_DGUK import SavePretty, DGUKopenAndParse, WriteDict
from datetime import datetime
import os

filedatestringlong = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')

action = 'organization_list'
limit = 1000
apidata = {'all_fields':'true','rows':limit}

allorgs=DGUKopenAndParse(action,apidata)

rawdir = '../output/orgsjson/orgsjson_' + filedatestringlong
os.makedirs(rawdir)

orgrows = []

iternum = 0
for org in allorgs:
    orgaction = 'organization_show'
    orgapidata = {'id':org['id']}
    odata = DGUKopenAndParse(orgaction,orgapidata)
    print(odata['title'])
    SavePretty(odata,rawdir+'/org_'+odata['name'])
    try: orgcat=odata['category']
    except (KeyError,IndexError): orgcat='None'
    try: orggroupname=odata['groups'][0]['name']
    except (KeyError,IndexError): orggroupname='None'
    try: orggroupcapacity=odata['groups'][0]['capacity']
    except (KeyError, IndexError): orggroupcapacity='None'
    orgrow = {'id':odata['id'],
              'name':odata['name'],
              'category':orgcat,
              'title':odata['title'],
              'group':orggroupname,
              'capacity':orggroupcapacity,
              'type':odata['type']}
    iternum +=1
    # if iternum == 2: break
    orgrows.append(orgrow)

WriteDict('../output/orgdata_'+filedatestringlong+'.csv',orgrows)