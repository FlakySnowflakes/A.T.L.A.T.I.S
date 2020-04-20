import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from textblob import TextBlob, Word

# Reads each line in txt and append them in array
with open('other_stopwords.txt') as f:
    other_stopwords = [line.strip() for line in f]
with open('positive-words.txt') as f:
    pos_words = [line.strip() for line in f]
with open('negative-words.txt') as f:
    neg_words = [line.strip() for line in f]

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
    filter_review(df2)

def filter_review(df):
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
    # Get the most common word used in each reviews. # 7 most used words
    keywords = pd.Series(" ".join(df['lemmatize']).split()).value_counts()[:7]
    print(keywords, '\n')
    # Drop unnecessary columns
    df.drop(['lowercase', 'punctuation', 'no_stopwords',
             'lemmatize'], axis=1, inplace=True)
    with open(hotel_name + '.csv', 'a') as f:
        df.to_csv(f, header=f.tell() == 0, na_rep='NULL')