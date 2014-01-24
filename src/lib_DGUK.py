__author__ = 'bouchalp'

outputfolder = '../output/'

def SavePretty(JSONobject,filename):
    "Saves content of JSON as pretty-printed text"
    from pprint import pprint
    filepath = outputfolder + filename + '.json'
    dataconn=open(filepath,'w+')
    pprint(JSONobject,dataconn)

def DGUKopenAndParse(apiaction,apidata):
    'Returns parsed result from API call'
    import urllib
    import urllib2
    import json
    apibase = 'http://data.gov.uk/api/3/'
    data_string = urllib.quote(json.dumps(apidata))
    rawdata = urllib2.urlopen(apibase+'/action/'+apiaction,data_string)
    # print apibase+'/action/'+apiaction+data_string
    assert rawdata.code==200
    result = json.loads(rawdata.read())['result']
    return result

def WriteDict(filepath,listofdicts):
    """
    Writes dictionary to file in filepath
    @type filepath: str
    @param filepath:
    @param listofdicts: list of dictionaries
    """
    global orgfile, orgwriter
    import csv
    orgfile = open(filepath, 'w+')
    orgwriter = csv.DictWriter(orgfile, fieldnames=listofdicts[0].keys())
    orgwriter.writeheader()
    orgwriter.writerows(listofdicts)
    orgfile.close()