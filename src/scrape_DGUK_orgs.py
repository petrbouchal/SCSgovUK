__author__ = 'bouchalp'

from lib_DGUK import SavePretty, DGUKopenAndParse, WriteDict

limit = 1000
apidata = {'all_fields':'true','rows':limit}

action = 'organization_list'
allorgs=DGUKopenAndParse(action,apidata)

orgrows = []

iternum = 0
for org in allorgs:
    orgaction = 'organization_show'
    orgapidata = {'id':org['id']}
    odata = DGUKopenAndParse(orgaction,orgapidata)
    print(odata['title'])
    SavePretty(odata,'orgjson/org_'+odata['name'])
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

WriteDict('../output/orgdata.csv',orgrows)