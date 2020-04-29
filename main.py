import requests
from codes.url_parser import *
from codes.Filter_Reviews import *
from data_Conversion import *
import time

ip = requests.get('http://icanhazip.com').text

url = 'https://www.tripadvisor.com.ph/Hotel_Review-g298573-d5037302-Reviews-V_Hotel-Manila_Metro_Manila_Luzon.html'


def main():
    global results
    print('\nCurrent IP:', ip)
    city = input('City: ').title()
    p = ParseTripAdvisor(20, city)
    print('Collecting soup...\n')
    time.sleep(2)
    p.get_soup(url)
    p.parse(url)
    if p.HotelExist() == True:
        print("File ", p.hotelName, " already exists and is readable\n")
        return
    else:
        print("The file does not exist...\n" + "Creating new file...\n")
        df = to_DataFrame(results)  # Convert list to DataFrame
        del results[:]
        print('Filtering review...\n')
        time.sleep(2)
        df = filter_review(df, p.hotelName, city)  # Divide the review sentences from the DataFrame
        print('Saving to sql and csv...\n')
        time.sleep(1)
        SetSave(df, p.hotelName, p.city, p.address)  # <---- save pandas to sql and csv
        print(str(p.hotelName) + " Dataframe saved to sql and csv successfully!")


if __name__ == '__main__':
    main()
