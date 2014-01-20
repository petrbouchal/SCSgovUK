__author__ = 'petrbouchal'

import csv

testcsv = './blah.csv'
writer = csv.writer(open(testcsv,'a',encoding='UTF8'))

row=['+ěščřžýáíé','éíáýžřšňúů']
# row=['abc','def']
print(row)
# writer.writerow(bytes(row, 'UTF-8'))
writer.writerow(row)
