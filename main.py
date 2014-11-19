#!/usr/bin/env python2

from Scrapers import MajorHoldersScraper


def main():
    scraper = MajorHoldersScraper()
    names = scraper.scrape('AAPL')
    print(names)

if __name__ == '__main__':
    main()
