import requests
from codes.url_parser import *
from codes.Filter_Reviews import *
from data_Conversion import *

ip = requests.get('http://icanhazip.com').text

start_urls = [
    'https://www.tripadvisor.com.ph/Hotel_Review-g298573-d306018-Reviews-Diamond_Hotel_Philippines-Manila_Metro_Manila_Luzon.html'
]


def start():
    global results
    for url in start_urls:
        print('Current IP:', ip)
        p = ParseTripAdvisor(20) # (#)<-- Number of reviews to limit
        check = p.parse(url, p.get_soup(url))
        if check == True:
            pass
        else:
            df = to_DataFrame(results)  # Convert list to DataFrame
            del results[:]
            df = filter_review(df, p.hotel_name)  # Divide the review sentences from the DataFrame
            saveto_sql(df, p.hotel_name)  # <---- save pandas to sql
            saveto_csv(df, p.hotel_name)  # <---- save pandas to csv
        
        # hotel_data_tocsv(df)
        


def main():
    start()


if __name__ == '__main__':
    main()
