import pandas as pd
import numpy as np
from nltk import sent_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob, Word
from sqlalchemy import create_engine

# Reads each line in txt and append them in array
with open('Lexicon/other_stopwords.txt') as f:
    other_stopwords = [line.strip() for line in f]
with open('Lexicon/positive-words.txt') as f:
    pos_words = [line.strip() for line in f]
with open('Lexicon/negative-words.txt') as f:
    neg_words = [line.strip() for line in f]


def hotel_stopwords(hotel_name):
    other_stopwords.extend(hotel_name.lower().split())
    try:
        other_stopwords.remove('hotel')
    except:
        pass


def filter_review(df, hotel_name, city):
    hotel_stopwords(hotel_name)
    df = div_sentences(df)  # Seperates sentences of a content review
    # Lowercase each words from the reviews
    df['lowercase'] = df['review'].apply(lambda x: " ".join(word.lower() for word in x.split()))
    # Remove all punctuation marks
    df['punctuation'] = df['lowercase'].str.replace('[^\w\s]', ' ')
    # Remove all stopwords (such as 'i', 'we', 'they', 'us', etc in nltk.stopwords)
    stop_words = stopwords.words('english')
    df['stopwords'] = df['punctuation'].apply(lambda x: " ".join(
        word for word in x.split() if word not in stop_words and word not in other_stopwords))
    # Lemmatization
    df['lemmatize'] = df['stopwords'].apply(
        lambda x: " ".join(Word(word).lemmatize() for word in x.split()))
    # if there are still unnecessary common words, custom stopwords will be added
    df['cleanreview'] = df['stopwords'].apply(lambda x: " ".join(
        word for word in x.split() if word not in pos_words and word not in neg_words))
    # Get the most and least common word used in each reviews.
    keywords = KeysandRares(df, hotel_name, city)
    # Get the Sentimental Analysis
    df = sentiment(df, keywords)
    # with open('csvFiles/corpus1.csv', 'a') as f:
    #     df.to_csv(f, header=f.tell() == 0, na_rep='NULL')
    # Drop unnecessary columns
    df.drop(['lowercase', 'punctuation', 'stopwords',
             'lemmatize', 'cleanreview'], axis=1, inplace=True)

    return df


def div_sentences(df):
    # Seperating the sentences from a review
    df['Sentences'] = df['review'].apply(lambda x: sent_tokenize(str(x)))
    # create new DataFrame to organize each column
    df2 = df.filter(['city', 'hotel', 'reviewer', 'Sentences'], axis=1)
    df2 = df2.explode('Sentences')
    # Remove sentences with more than 25 words
    count = df2['Sentences'].astype(str).str.split().str.len()
    df2 = df2[~(count > 27)]
    df2.reset_index(drop=True, inplace=True)
    df2.rename({'Sentences': 'review'}, axis=1, inplace=True)
    # returns all sentences to filter each
    return df2


def sentiment(df, keywords):
    # Sentiment Analysis
    df['polarity'] = df['lemmatize'].apply(lambda x: TextBlob(x).sentiment[0])
    # Get reviews that has words from most commonly used words (keywords)
    # This excludes words from least commonly used words
    df['aspect_terms'] = df['review'].apply(lambda x: " ".join(
        word for word in x.split() if word in keywords))
    df.replace('', np.nan, inplace=True)  # Replace all empty string of cells with NaN or Null
    # cp = df[df.aspect_terms.notnull()]  # Get all rows that are not Null
    df = df[df['aspect_terms'].notna()]  # Drop rows with no aspect_terms
    df = df[df['polarity'] != 0]  # Drop rows with zero polarity
    # Label rows with positive or negative
    df['P_sentiment'] = df.apply(lambda x: positives(x), axis=1)
    df['N_sentiment'] = df.apply(lambda x: negatives(x), axis=1)
    df.replace('', np.nan, inplace=True)
    # Sort alphabetically
    df = df.sort_values(['aspect_terms']).round(decimals=3)
    df.reset_index(drop=True, inplace=True)
    return df


def positives(x):
    if x['polarity'] > 0:
        return 'Positive'
    return ''


def negatives(x):
    if x['polarity'] < -0:
        return 'Negative'
    return ''


def KeysandRares(df, hotel_name, city):
    keys = pd.Series(" ".join(df['cleanreview']).split()).value_counts()[:5]  # 5 most common words
    # rares = pd.Series(" ".join(df['cleanreview']).split()
    #                   ).value_counts()[-5]  # 5 least common words
    engine = create_engine('sqlite:///keywords/' + city + '_keywords.db')
    keys.to_sql(name=hotel_name, con=engine, if_exists='append')
    return keys
