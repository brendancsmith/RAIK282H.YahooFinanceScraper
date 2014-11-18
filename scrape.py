from urllib.request import urlopen
from bs4 import BeautifulSoup

optionsUrl = 'https://finance.yahoo.com/q/mh?s=AAPL+Major+Holders'
optionsPage = urlopen(optionsUrl)

soup = BeautifulSoup(optionsPage)

table = soup.find('table', attrs={'class': 'yfnc_tableout1'}).find('table')
#cells = table.findAll('td', attrs={'class': 'yfnc_tabledata1'})
#print([cell.parent for cell in cells])

rows = table.findAll('tr')
rows = [row for row in rows
        if row.find('td', attrs={'class': 'yfnc_tabledata1'})]
names = [row.find('td').text for row in rows]

print(names)
