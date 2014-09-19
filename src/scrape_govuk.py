__author__ = 'petrbouchal'

import urllib
import urllib2
from bs4 import BeautifulSoup

baseurl = 'http://www.gov.uk/government/people'

data = urllib2.urlopen(baseurl)
html = data.read()
soup = BeautifulSoup(html)

personbits = soup.find_all('li',{'class':'person'})
print(len(personbits))

personurls = []
for i in personbits:
    personurl = i.find('a')['href']
    personid = i['id']
    print(personurl + ' ' + personid)
    personurls.append(personurl)
    print('hello')
print(len(personurls))

# hello dolly

# hello dolly test 2

# for url in personurls: