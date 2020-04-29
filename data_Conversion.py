import pandas as pd
from sqlalchemy import create_engine


def to_DataFrame(x):
    df = pd.DataFrame(x)
    return df


def SetSave(df, hotel_name, city, address):
    saveto_csv(df, hotel_name, city)
    # hotel_data_tocsv(df, city, address)
    saveto_sql(df, hotel_name)
    hotel_data_tosql(df, hotel_name, city, address)


def saveto_csv(df, hotel_name, city):
    with open('csvFiles/' + city  + '/'+ hotel_name + '.csv', 'a') as f:
        df.to_csv(f, header=f.tell() == 0, na_rep='NULL')


def saveto_sql(df, hotel_name):
    engine = create_engine('sqlite:///dbFiles/hotel-TA.db')
    df.to_sql(name=hotel_name, con=engine, if_exists='append')


def hotel_data_tocsv(df, city, address):
    dnf = df.groupby('hotel').agg(
        {'review': 'count', 'P_sentiment': 'count', 'N_sentiment': 'count'})
    dnf.columns = ['reviews', 'positives', 'negatives']
    dnf['pos_percent'] = dnf['positives'][0]/dnf['reviews'][0]
    dnf['neg_percent'] = dnf['negatives'][0]/dnf['reviews'][0]
    dnf['address'] = address
    dnf['city'] = city
    dnf = dnf.reset_index().round(decimals=3)
    with open('csvFiles/Hotels.csv', 'a') as f:
        dnf.to_csv(f, header=f.tell() == 0, index=False)


def hotel_data_tosql(df, hotel_name, city, address):
    dnf = df.groupby('hotel').agg(
        {'review': 'count', 'P_sentiment': 'count', 'N_sentiment': 'count'})
    dnf.columns = ['reviews', 'positives', 'negatives']
    dnf['pos_percent'] = dnf['positives'][0]/dnf['reviews'][0]
    dnf['neg_percent'] = dnf['negatives'][0]/dnf['reviews'][0]
    dnf['address'] = address
    dnf = dnf.reset_index().round(decimals=3)
    engine2 = create_engine('sqlite:///dbFiles/Cityhotels.db')
    dnf.to_sql(name=city, con=engine2, if_exists='append', index=False)


# def read_Data()
    # df = pd.read_csv
