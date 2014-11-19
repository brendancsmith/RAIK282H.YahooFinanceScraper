#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper
import finsymbols
import json


def get_sp500_stocks():
    return finsymbols.get_sp500_symbols()


def get_sp500_symbols():
    return [stock['symbol'] for stock in get_sp500_stocks()]


def scrape_corporate_boards(symbols):
    scraper = MajorHoldersScraper()
    corpBoards = {}

    for symbol in symbols:
        print 'scraping {}/{}'.format(symbols.index(symbol), len(symbols))
        names = scraper.scrape(symbol)
        corpBoards[symbol] = names

    #for symbol, board in corpBoards.items():
    #    print '{}: {}'.format(symbol, board)

    return corpBoards


def write_cache(boards):
    with open('corporate_boards.json', 'w') as cache:
        text = json.dumps(boards)
        cache.write(text)


def read_cache():
    with open('corporate_boards.json', 'r') as cache:
        text = cache.read()
        return json.loads(text)


def main():
    symbols = get_sp500_symbols()

    boards = scrape_corporate_boards(symbols)
    write_cache(boards)

if __name__ == '__main__':
    main()
