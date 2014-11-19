#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper
from Caches import JsonCache
import finsymbols

cachePath = 'corporate_boards.json'


def get_sp500_stocks():
    return finsymbols.get_sp500_symbols()


def get_sp500_symbols():
    return [stock['symbol'] for stock in get_sp500_stocks()]


# Creates a dictionary of the corporate boards for the companies
# associated with the specified stock market symbols.
#   key: stock symbol
#   value: list of member names
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


# Given a dictionary of corporate boards, create a dictionary of members who
# are on multiple boards. If prune is false, majority holders of a single
# company will be included
#   key: member name
#   value: list of stock symbols
def find_shared_members(boards, prune=True):
    sharedMembers = {}

    for symbol, members in boards.items():
        for member in members:
            if member in sharedMembers:
                sharedMembers[member] += symbol
            else:
                sharedMembers[member] = [symbol]

    if(prune):
        for member, symbols in sharedMembers.items():
            if len(symbols) < 2:
                sharedMembers.pop(member)  # purposefully omitting default arg

    return sharedMembers


def main():
    cache = JsonCache('corporate_boards')
    boards = None

    # get a dictionary of the corporate boards
    # (read from cache, or scrape and write to cache)
    if cache.exists():
        print('reading cache...')
        boards = cache.read()
    else:
        symbols = get_sp500_symbols()

        boards = scrape_corporate_boards(symbols)
        cache.write(boards)

    print('found {} boards'.format(len(boards)))

    import pprint
    pprint.pprint(find_shared_members(boards))

if __name__ == '__main__':
    main()
