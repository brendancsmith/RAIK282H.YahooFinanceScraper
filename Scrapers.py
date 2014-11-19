from urllib import urlopen
from bs4 import BeautifulSoup


class BaseYahooScraper(object):

    baseUrl = 'https://finance.yahoo.com/q'
    endpoint = None

    @classmethod
    def construct_url(cls, symbol):
        url = cls.baseUrl

        # add acronym for query type (ie. 'mh' for Major Holders)
        if(cls.endpoint):
            url += '/{}'.format(cls.endpoint)

        url += '?s={}'.format(symbol)  # add symbol parameter

        return url

    def create_soup(self, symbol):
        url = self.construct_url(symbol)
        page = urlopen(url)
        soup = BeautifulSoup(page)

        return soup


class MajorHoldersScraper(BaseYahooScraper):

    endpoint = 'mh'

    def scrape(self, symbol):
        soup = self.create_soup(symbol)
        return self._scrape(soup)

    # not a fan of this structure, but it's organized at least
    @staticmethod
    def _scrape(soup):
        # get major holders table
        table = soup.find('table',
                          attrs={'class': 'yfnc_tableout1'}).find('table')

        rows = table.findAll('tr')  # includes header, we'll filter it out
        hasDataCell = lambda x: x.find('td',
                                       attrs={'class': 'yfnc_tabledata1'})
        rows = filter(hasDataCell, rows)

        # content of first column
        names = [row.find('td').text for row in rows]

        return names


def main():
    scraper = MajorHoldersScraper()
    names = scraper.scrape('AAPL')
    print(names)

if __name__ == '__main__':
    main()
