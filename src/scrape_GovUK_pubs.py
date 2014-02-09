__author__ = 'petrbouchal'

from lib_DGUK import GovUkOpenAndParse, SaveFile, WriteDict
import re
import time
from datetime import datetime
import os
import sys

# set up reusable strings
filedatestringlong = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
pubsurl = 'http://www.gov.uk/government/publications'
govukurl = 'http://www.gov.uk'
pubdatadir = '../output/govukpubfiles/' + filedatestringlong

# use first command-line argument as search term, if available
if len(sys.argv) > 1:
    searchterm = sys.argv[1]
else:
    searchterm = "organogram salaries"

print("Searching for: " + searchterm)

# data to pass to server
searchdata = {"keywords": searchterm, "publication_filter_option": "all", "departments[]": "all",
              "topics[]": "all", "from_date": "", "to_date": "", 'official_document_status': 'all',
              'world_locations[]': 'all'}

# create time-marked directory for downloaded files
os.makedirs(pubdatadir)

# download first page or results
soup = GovUkOpenAndParse(pubsurl, searchdata)

# print stats on search results
rescount = soup.find('span', {'class': 'count'}).contents[0]
print('Total results - publications: ' + rescount)
rescountnum = int(re.sub(',', '', rescount))
runsnum = rescountnum / 40 + 1

# loop through pages and put them into a dictionary
pagecounter = 1
pages = []
# runsnum=1 # for testing purpose
while pagecounter <= runsnum:
    searchdata['page'] = pagecounter
    pagecounter += 1
    pagesoup = GovUkOpenAndParse(pubsurl, searchdata)
    pages.append(pagesoup)

print('Number of pages of results to process: ' + str(len(pages)))

# initiate lists of dictionaries for CSV writing
pubpagerows = []
pubfilerows = []

pubcounter = 0
pubfilecounter = 0
pagecounter = 1

# timing for progress counter
time_start = time.time()
itemstodo = len(pages)*40

# loop through pages, publications, and files
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
        puborg = pubsoup.find('span', {'class': 'organisation lead'}).a.contents[0].encode('ascii','ignore')
        try:
            pubdecription = pubsoup.find('div', {'class': 'summary'}).p.contents[0].encode('ascii','ignore')
        except AttributeError:
            pubdecription = 'NA'
        pubfiles = pubsoup.find_all('div', {'class': 'attachment-details'})
        pubpagerow = {}
        pubpagerow = {'puburl': puburl, 'pubdescription': pubdecription, 'pubtitle': pubtitle, 'puborg': puborg}
        pubpagerows.append(pubpagerow)
        for pubfile in pubfiles:
            try:
                filetitle = pubfile.h2.contents[0].encode('ascii','ignore')
                fileurl = pubfile.find('span', {'class': 'download'}).a['href']
                csvmarked = re.search(r'CSV', pubfile.find('span', {'class': 'download'}).a.contents[1].contents[0])
                if csvmarked is None:
                    csvlabel = 'FALSE'
                else:
                    csvlabel = 'TRUE'
            except Exception:
                filetitle = pubfile.h2.contents[0].contents[0].encode('ascii','ignore')
                fileurl = pubfile.h2.contents[0]['href']
                csvlabel = False
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
            pubfilerow = {}
            pubfilerow = {'url': pubfileurl, 'saved-as': pubfilename, 'filetitle': filetitle, 'extension': ext,
                          'marked-as-csv': csvlabel, 'puburl': puburl}
            pubfilerows.append(pubfilerow)
            pubfilecounter += 1
        pubcounter += 1
        if pubcounter%10==0:
            print('\nRoughly ' + '{0:.0f}%'.format(pubcounter/float(itemstodo)*100)+' done.\n')
            time_elapsed = time.time() - time_start
            print('ETA in ' + '{0:.0f}'.format(float(time_elapsed)/float(pubcounter)*itemstodo-time_elapsed) + ' seconds')
    pagecounter +=1

# write dictionaries
WriteDict('../output/pubpages_' + filedatestringlong + '.csv', pubpagerows)
WriteDict('../output/pubfiles_' + filedatestringlong + '.csv', pubfilerows)

# print time ID for use in R analysis, and basic stats
print('Saved ' + str(pubfilecounter) + ' files from ' + str(pubcounter) + ' publications.')
print('Date-time marker: ')
print(str(filedatestringlong))