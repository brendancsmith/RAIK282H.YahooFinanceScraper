#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper
import finsymbols


def get_sp500_stocks():
    return finsymbols.get_sp500_symbols()


def get_sp500_symbols():
    return [stock['symbol'] for stock in get_sp500_stocks()]


def scrape_corporate_boards(symbols):
    scraper = MajorHoldersScraper()
    corpBoards = {}

    for symbol in symbols:
        names = scraper.scrape(symbol)
        corpBoards[symbol] = names

    #for symbol, board in corpBoards.items():
    #    print '{}: {}'.format(symbol, board)

    return corpBoards


def main():
    symbols = get_sp500_symbols()

    boards = scrape_corporate_boards(symbols[:5])
    print(boards)

if __name__ == '__main__':
    main()
