from urllib.request import urlopen
from bs4 import BeautifulSoup

baseUrl = 'https://finance.yahoo.com/q'


def construct_url(symbol, queryAcronym):
    url = baseUrl

    if(queryAcronym):  # add acronym for page type (ie. 'mh' for Major Holders)
        url += '/{}'.format(queryAcronym)

    url += '?s={}'.format(symbol)  # add symbol parameter

    return url


def create_MH_soup(symbol):
    url = construct_url(symbol, 'mh')
    page = urlopen(url)
    soup = BeautifulSoup(page)

    return soup


def extract_major_holders(soup):
    # get major holders table
    table = soup.find('table', attrs={'class': 'yfnc_tableout1'}).find('table')

    rows = table.findAll('tr')  # includes header, we'll filter it out
    hasDataCell = lambda x: x.find('td', attrs={'class': 'yfnc_tabledata1'})
    rows = filter(hasDataCell, rows)

    names = [row.find('td').text for row in rows]  # content of first column
    return names


def main():
    names = extract_major_holders(create_MH_soup('AAPL'))
    print(names)

if __name__ == '__main__':
    main()
