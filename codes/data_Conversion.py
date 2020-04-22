import pandas as pd
from sqlalchemy import create_engine


def saveto_csv(df, hotel_name):
    with open('csvFiles/' + hotel_name + '.csv', 'a') as f:
        df.to_csv(f, header=f.tell() == 0, na_rep='NULL')
    hotel_data_tocsv(df)


def hotel_data_tocsv(df):
    dnf = df.groupby('hotel').agg(
        {'review': 'count', 'P_sentiment': 'count', 'N_sentiment': 'count'})
    dnf.columns = ['reviews', 'positives', 'negatives']
    dnf['pos_percent'] = dnf['positives'][0]/dnf['reviews'][0]
    dnf['neg_percent'] = dnf['negatives'][0]/dnf['reviews'][0]
    dnf = dnf.reset_index().round(decimals=3)
    with open('csvFiles/hotels.csv', 'a') as f:
        dnf.to_csv(f, header=f.tell() == 0, index=False)


def to_DataFrame(x):
    df = pd.DataFrame(x)
    return df


def saveto_sql(df, hotel_name):
    engine = create_engine('sqlite:///dbFiles/hotel-TA.db')
    df.to_sql(name=hotel_name, con=engine, if_exists='append')
    hotel_data_tosql(df, hotel_name, engine)


def hotel_data_tosql(df, hotel_name, engine):
    dnf = df.groupby('hotel').agg(
        {'review': 'count', 'P_sentiment': 'count', 'N_sentiment': 'count'})
    dnf.columns = ['reviews', 'positives', 'negatives']
    dnf['pos_percent'] = dnf['positives'][0]/dnf['reviews'][0]
    dnf['neg_percent'] = dnf['negatives'][0]/dnf['reviews'][0]
    dnf = dnf.reset_index().round(decimals=3)
    engine2 = create_engine('sqlite:///dbFiles/Datahotels.db')
    dnf.to_sql(name='hotels', con=engine2, if_exists='append')


# def read_Data()
    # df = pd.read_csv
