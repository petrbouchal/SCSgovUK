__author__ = 'bouchalp'

def SavePretty(JSONobject,filename,):
    "Saves content of JSON as pretty-printed text"
    from pprint import pprint
    dataconn=open(filename,'w+')
    pprint(JSONobject,dataconn)

