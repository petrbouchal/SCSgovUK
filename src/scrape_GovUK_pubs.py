__author__ = 'petrbouchal'

from lib_DGUK import GovUkOpenAndParse, SaveFile, WriteDict
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

filedatestringlong = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
pubsurl = 'http://www.gov.uk/government/publications'
govukurl = 'http://www.gov.uk'

searchterm = "organogram OR \"staff data\""

searchdata = {"keywords": searchterm, "publication_filter_option": "all", "departments[]": "all",
              "topics[]": "all", "from_date": "", "to_date": "", 'official_document_status': 'all',
              'world_locations[]': 'all'}

pubdatadir = '../output/govukpubfiles/' + filedatestringlong
os.makedirs(pubdatadir)

soup = GovUkOpenAndParse(pubsurl, searchdata)

rescount = soup.find('span', {'class': 'count'}).contents[0]
print('Total results - publications: ' + str(len(rescount)))
rescountnum = re.sub(',','',rescount)
runsnum = int(rescountnum) / 40 + 1

pagecounter = 1
pages = []
#while (pagecounter < runsnum+1):
while (pagecounter < 6):
    searchdata['page']=pagecounter
    pagecounter = pagecounter+1
    pagesoup = GovUkOpenAndParse(pubsurl,searchdata)
    pages.append(pagesoup)

print('Number of pages: ' + str(len(pages)))

pubpagerows = []
pubfilerows = []
pubfilecounter = 0

for page in pages:
    container = page.find('ol', {'class': 'js-document-list document-list'})
    pubs = container.find_all('li', {'class': 'document-row'})
    print('Total results - pages: ' + str(len(pubs)))
    for i in pubs:
        pubtitle = i.h3.a.contents[0]
        print('Publication page: ' + pubtitle)
        puburl = govukurl+i.h3.a['href']
        print('Going to ' + puburl)
        pubsoup = GovUkOpenAndParse(govukurl+i.h3.a['href'],'')
        puborg = pubsoup.find('span',{'class':'organisation lead'}).a.contents[0]
        pubdecription = pubsoup.find('div',{'class':'summary'}).p.contents[0]
        pubfiles = pubsoup.find_all('div',{'class':'attachment-details'})
        pubrow = {'puburl': puburl, 'pubdescription': pubdecription, 'pubtitle': pubtitle, 'puborg':puborg}
        pubpagerows.append(pubrow)
        for pubfile in pubfiles:
            try:
                filetitle = pubfile.h2.contents[0]
                fileurl = pubfile.find('span',{'class':'download'}).a['href']
                csvmarked = re.search(r'CSV',pubfile.find('span',{'class':'download'}).a.contents[1].contents[0])
                if csvmarked is None: csvlabel = False
                else: csvlabel = True
            except Exception:
                filetitle = pubfile.h2.contents[0].contents[0]
                fileurl = pubfile.h2.contents[0]['href']
            try:
                ext = re.search(r'[a-zA-z]{3}$',fileurl).group(0)
                csvext = re.search(r'[a-zA-z]{3}$',fileurl).group(0)=='csv'
            except AttributeError:
                ext = ''
                csvext = False

            print('File: '+filetitle)
            pubfileurl = govukurl + fileurl
            print('URL for file download: ' + pubfileurl)
            filedatestringlong_current = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S%f')
            pubfilename = puborg + '_' + str(pubfilecounter)
            pubfilecounter += 1
            SaveFile(govukurl+fileurl,pubdatadir+'/'+pubfilename,ext)
            pubfilerow = {'url':pubfileurl, 'saved-as':pubfilename,'filetitle':filetitle,'extension':ext,
                          'marked-as-csv':csvlabel,'pageurl':puburl}
            pubfilerows.append(pubfilerow)

WriteDict('../output/pubpages_'+filedatestringlong+'.csv',pubpagerows)
WriteDict('../output/pubfiles_'+filedatestringlong+'.csv',pubfilerows)