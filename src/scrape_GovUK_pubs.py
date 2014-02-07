__author__ = 'petrbouchal'

from lib_DGUK import GovUkOpenAndParse
from bs4 import BeautifulSoup
import re

pubsurl = 'http://www.gov.uk/government/publications'
govukurl = 'http://www.gov.uk'
searchdata = {"keywords": "organogram OR \"staff data\"", "publication_filter_option": "all", "departments[]": "all",
              "topics[]": "all", "from_date": "", "to_date": "", 'official_document_status': 'all',
              'world_locations[]': 'all'}

soup = GovUkOpenAndParse(pubsurl, searchdata)

rescount = soup.find('span', {'class': 'count'}).contents[0]
print(rescount)
rescountnum = re.sub(',','',rescount)
runsnum = int(rescountnum) / 40 + 1

pagecounter = 1
pages = []
#while (pagecounter < runsnum+1):
while (pagecounter < 2):
    searchdata['page']=pagecounter
    pagecounter = pagecounter+1
    pagesoup = GovUkOpenAndParse(pubsurl,searchdata)
    pages.append(pagesoup)

print(len(pages))

for page in pages:
    container = page.find('ol', {'class': 'js-document-list document-list'})
    pubs = container.find_all('li', {'class': 'document-row'})
    print(len(pubs))
    for i in pubs:
        print('Publication page: ' + i.h3.a.contents[0])
        print('Going to ' + govukurl+i.h3.a['href'])
        pubsoup = GovUkOpenAndParse(govukurl+i.h3.a['href'],'')
        pubfiles = pubsoup.find_all('div',{'class':'attachment-details'})
        for pubfile in pubfiles:
            try:
                filetitle = pubfile.h2.contents[0]
                fileurl = pubfile.find('span',{'class':'download'}).a['href']
            except Exception:
                filetitle = pubfile.h2.contents[0].contents[0]
                fileurl = pubfile.h2.contents[0]['href']
            print('File: '+filetitle)
            print('URL for file download: ' + govukurl + fileurl)
