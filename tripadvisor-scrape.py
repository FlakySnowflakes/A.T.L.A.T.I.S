import requests
from codes.url_parser import *
# import re
# # import sqlite3 as db


start_urls = [ 'https://www.tripadvisor.com/Hotel_Review-g56943-d226686-Reviews-Bryce_Canyon_Pines-Bryce_Utah.html'
]


def start():
    for url in start_urls:
        p = ParseTripAdvisor(15)  # (15) <-- Number of reviews to limit
        p.parse(url, p.get_soup(url))
        df = to_DataFrame(results)  # Convert list to DataFrame
        with open(p.hotel_name + '.csv', 'a') as f:
            df.to_csv(f, header=f.tell() == 0, na_rep='NULL')  # <---- save pandas to csv


def main():
    start()


if __name__ == '__main__':
    main()
