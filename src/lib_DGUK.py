__author__ = 'bouchalp'

outputfolder = '../output/'

def SavePretty(JSONobject,filename):
    "Saves content of JSON as pretty-printed text"
    from pprint import pprint
    filepath = outputfolder + filename + '.json'
    dataconn=open(filepath,'w+')
    pprint(JSONobject,dataconn)
    dataconn.close()

def SaveFile(url,filename, fileext):
    import urllib2
    filepath = outputfolder + filename + '.' + fileext
    data = urllib2.urlopen(url)
    dataread = data.read()
    dataconn = open(filepath,'w+')
    dataconn.write(dataread)
    dataconn.close()

def DGUKopenAndParse(apiaction,apidata):
    'Returns parsed result from API call'
    import urllib
    import urllib2
    import json
    apibase = 'http://data.gov.uk/api/3/'
    data_string = urllib.quote(json.dumps(apidata))
    rawdata = urllib2.urlopen(apibase+'action/'+apiaction,data_string)
    # print apibase+'/action/'+apiaction+data_string
    result = json.loads(rawdata.read())['result']
    return result

def GovUkOpenAndParse(baseurl,querydata):
    'Returns parsed result from API call'
    import urllib
    import urllib2
    from bs4 import BeautifulSoup
    try:
        data_string = urllib.urlencode(querydata)
        rawdata = urllib2.urlopen(baseurl+'?'+data_string)
    except Exception:
        rawdata = urllib2.urlopen(baseurl)
    data = rawdata.read()
    result = BeautifulSoup(data,'lxml')
    return result

def WriteDict(filepath,listofdicts):
    """
    Writes dictionary to file in filepath
    @type filepath: str
    @param filepath:
    @param listofdicts: list of dictionaries
    """
    import csv
    with open(filepath, 'w+') as orgfile:
        orgwriter = csv.DictWriter(orgfile, fieldnames=listofdicts[0].keys())
        orgwriter.writeheader()
        orgwriter.writerows(listofdicts)
    result = True
    return result