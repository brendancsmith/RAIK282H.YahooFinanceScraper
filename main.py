#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper
from Caches import JsonCache
import finsymbols
import itertools

cachePath = 'corporate_boards.json'


def get_sp500_stocks():
    return finsymbols.get_sp500_symbols()


def get_sp500_symbols():
    return [stock['symbol'] for stock in get_sp500_stocks()]


def scrape_sp500_boards():
    symbols = get_sp500_symbols()
    boards = scrape_corporate_boards(symbols)
    return boards


# Creates a dictionary of the corporate boards for the companies
# associated with the specified stock market symbols.
#   key: stock symbol
#   value: list of member names
def scrape_corporate_boards(symbols):
    scraper = MajorHoldersScraper()
    corpBoards = {}

    for symbol in symbols:
        # not a fan of print statements outside main(), but whatever
        print 'scraping {}/{}...'.format(symbols.index(symbol) + 1,
                                         len(symbols))
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
                sharedMembers[member] += [symbol]
            else:
                sharedMembers[member] = [symbol]

    if(prune):
        for member, symbols in sharedMembers.items():
            if len(symbols) < 2:
                sharedMembers.pop(member)  # purposefully omitting default arg

    return sharedMembers


# given a dictionary of majority holders for multiple companies
# (from `find_shared_members`), create a network edge list
def create_edge_list(sharedMembers):
    edges = set()

    for member, symbols in sharedMembers.items():
        combinations = itertools.combinations(symbols, 2)
        edges |= set(combinations)

    return list(edges)


def main():
    cache = JsonCache('corporate_boards')

    boards = cache.retrieve(scrape_sp500_boards)
    print('found {} boards'.format(len(boards)))

    sharedMembers = find_shared_members(boards)
    edges = create_edge_list(sharedMembers)

    JsonCache('multi_holders').write(sharedMembers)
    print('found {} holders of multiple companies'.format(len(sharedMembers)))

    with open('edge_list.txt', 'w') as f:
        for edge in edges:
            f.write(','.join(edge) + '\n')

if __name__ == '__main__':
    main()
