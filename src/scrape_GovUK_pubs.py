__author__ = 'petrbouchal'

from lib_DGUK import GovUkOpenAndParse, SaveFile, WriteDict
import re
import time
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
print('Total results - publications: ' + rescount)
rescountnum = re.sub(',', '', rescount)
runsnum = int(rescountnum) / 40 + 1

pagecounter = 1
pages = []
runsnum=1
while pagecounter <= runsnum:
    searchdata['page'] = pagecounter
    pagecounter += 1
    pagesoup = GovUkOpenAndParse(pubsurl, searchdata)
    pages.append(pagesoup)

print('Number of pages of results to process: ' + str(len(pages)))

pubpagerows = []
pubfilerows = []
pubfilecounter = 0

pubcounter = 0
filecounter = 0
pagecounter = 1
time_start = time.time()
itemstodo = len(pages)*40
for page in pages:
    container = page.find('ol', {'class': 'js-document-list document-list'})
    pubs = container.find_all('li', {'class': 'document-row'})
    print('Page '+ str(pagecounter) + '. ' + 'Total results - on this page: ' + str(len(pubs)))
    for i in pubs:
        pubtitle = i.h3.a.contents[0].encode('ascii','ignore')
        # print('Publication page: ' + pubtitle)
        puburl = govukurl + i.h3.a['href']
        # print('Going to ' + puburl)
        pubsoup = GovUkOpenAndParse(govukurl + i.h3.a['href'], '')
        puborg = pubsoup.find('span', {'class': 'organisation lead'}).a.contents[0]
        pubdecription = pubsoup.find('div', {'class': 'summary'}).p.contents[0].encode('ascii','ignore')
        pubfiles = pubsoup.find_all('div', {'class': 'attachment-details'})
        pubrow = {'puburl': puburl, 'pubdescription': pubdecription, 'pubtitle': pubtitle, 'puborg': puborg}
        pubpagerows.append(pubrow)
        for pubfile in pubfiles:
            try:
                filetitle = pubfile.h2.contents[0].encode('ascii','ignore')
                fileurl = pubfile.find('span', {'class': 'download'}).a['href']
                csvmarked = re.search(r'CSV', pubfile.find('span', {'class': 'download'}).a.contents[1].contents[0])
                if csvmarked is None:
                    csvlabel = False
                else:
                    csvlabel = True
            except Exception:
                filetitle = pubfile.h2.contents[0].contents[0].encode('ascii','ignore')
                fileurl = pubfile.h2.contents[0]['href']
            try:
                ext = re.search(r'[a-zA-z]{3}$', fileurl).group(0)
                csvext = re.search(r'[a-zA-z]{3}$', fileurl).group(0) == 'csv'
            except AttributeError:
                ext = ''
                csvext = False

            # print('File: ' + filetitle)
            pubfileurl = govukurl + fileurl
            # print('URL for file download: ' + pubfileurl)
            filedatestringlong_current = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S%f')
            pubfilename = puborg + '_' + str(pubfilecounter)
            SaveFile(govukurl + fileurl, pubdatadir + '/' + pubfilename, ext)
            pubfilerow = {'url': pubfileurl, 'saved-as': pubfilename, 'filetitle': filetitle, 'extension': ext,
                          'marked-as-csv': csvlabel, 'puburl': puburl}
            pubfilerows.append(pubfilerow)
            pubfilecounter += 1
        pubcounter += 1
        if pubcounter%5==0:
            print('\nRoughly ' + str(float(pubcounter)/float(itemstodo)*100)+'% done.\n')
            time_elapsed = time.time() - time_start
            print('ETA in ' + str(float(time_elapsed)/float(pubcounter)*itemstodo-time_elapsed) + 's')
    pagecounter +=1

WriteDict('../output/pubpages_' + filedatestringlong + '.csv', pubpagerows)
WriteDict('../output/pubfiles_' + filedatestringlong + '.csv', pubfilerows)

print('Saved ' + str(pubfilecounter) + ' files from ' + str(pubcounter) + ' publications.')
print('Date-time marker: ' + filedatestringlong)