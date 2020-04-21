import pandas as pd
import numpy as np
from nltk import sent_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob, Word

# Reads each line in txt and append them in array
with open('Lexicon/other_stopwords.txt') as f:
    other_stopwords = [line.strip() for line in f]
with open('Lexicon/positive-words.txt') as f:
    pos_words = [line.strip() for line in f]
with open('Lexicon/negative-words.txt') as f:
    neg_words = [line.strip() for line in f]


def filter_review(df, hotel_name):
    other_stopwords.append(hotel_name)
    df = div_sentences(df)  # Seperates sentences of a content review
    # Lowercase each words from the reviews
    df['lowercase'] = df['review'].apply(lambda x: " ".join(word.lower() for word in x.split()))
    # Remove all punctuation marks
    df['punctuation'] = df['lowercase'].str.replace('[^\w\s]', ' ')
    # Remove all stopwords (such as 'i', 'we', 'they', 'us', etc in nltk.stopwords)
    stop_words = stopwords.words('english')
    df['no_stopwords'] = df['punctuation'].apply(lambda x: " ".join(
        word for word in x.split() if word not in stop_words and word not in other_stopwords))
    # Lemmatization
    df['lemmatize'] = df['no_stopwords'].apply(
        lambda x: " ".join(Word(word).lemmatize() for word in x.split()))
    # if there are still unnecessary common words, custom stopwords will be added
    df['cleanreview'] = df['no_stopwords'].apply(lambda x: " ".join(
        word for word in x.split() if word not in pos_words and word not in neg_words))
    # Get the most common word used in each reviews. # 5 most used words
    keywords = pd.Series(" ".join(df['cleanreview']).split()).value_counts()[:5]
    with open('keywords/' + hotel_name + "_keywords.txt", "w") as keys:
        keys.write(str(keywords))
    # Get the Sentimental Analysis
    df = sentiment(df, keywords)
    # Drop unnecessary columns
    df.drop(['lowercase', 'punctuation', 'no_stopwords',
             'lemmatize', 'cleanreview'], axis=1, inplace=True)

    return df


def div_sentences(df):
    # Seperating the sentences from a review
    df['Sentences'] = df['review'].apply(lambda x: sent_tokenize(str(x)))
    df2 = df.filter(['hotel', 'reviewer', 'Sentences'], axis=1)
    # df2 = pd.DataFrame({'reviewer': df.reviewer.repeat(
    # df.Sentences.str.len()), 'review': np.concatenate(df.Sentences.values)})
    df2 = df2.explode('Sentences')
    df2.reset_index(drop=True, inplace=True)
    df2.rename({'Sentences': 'review'}, axis=1, inplace=True)
    # returns all sentences to filter each
    return df2


def sentiment(df, keywords):
    # Sentiment Analysis
    df['polarity'] = df['lemmatize'].apply(lambda x: TextBlob(x).sentiment[0])
    # Get reviews that has a word from most commonly used words (keywords)
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
    if x['polarity'] < 0:
        return 'Negative'
    return ''

# def Sentimental(x):
#     if x['polarity'] > 0:
#         return 'Positive'
#     else:
#         return 'Negative'
