#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper
import finsymbols


def get_sp500_symbols():
    return [stock['symbol'] for stock in finsymbols.get_sp500_symbols()]


def main():
    print(len(get_sp500_symbols()))

    scraper = MajorHoldersScraper()
    names = scraper.scrape('AAPL')
    print(names)

if __name__ == '__main__':
    main()
