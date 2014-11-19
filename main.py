#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper
from Caches import JsonCache
import finsymbols

cachePath = 'corporate_boards.json'


def get_sp500_stocks():
    return finsymbols.get_sp500_symbols()


def get_sp500_symbols():
    return [stock['symbol'] for stock in get_sp500_stocks()]


def scrape_corporate_boards(symbols):
    scraper = MajorHoldersScraper()
    corpBoards = {}

    for symbol in symbols:
        print 'scraping {}/{}...'.format(symbols.index(symbol), len(symbols))
        names = scraper.scrape(symbol)
        corpBoards[symbol] = names

    #for symbol, board in corpBoards.items():
    #    print '{}: {}'.format(symbol, board)

    return corpBoards


def main():
    cache = JsonCache('corporate_boards')
    boards = None

    if cache.exists():
        print('reading cache...')
        boards = cache.read()
    else:
        symbols = get_sp500_symbols()

        boards = scrape_corporate_boards(symbols)
        cache.write(boards)

    print('done, {} boards'.format(len(boards)))

if __name__ == '__main__':
    main()
