import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from textblob import TextBlob, Word

def div_sentences(df):
    # Seperating the sentences from a review
    df['Sentences'] = df['review'].apply(lambda x: sent_tokenize(str(x)))
    df2 = df.filter(['hotel', 'reviewer', 'Sentences'], axis=1)
    df2 = pd.DataFrame({'reviewer': df.reviewer.repeat(df.Sentences.str.len()), 'review': np.concatenate(df.Sentences.values)})
    df2.reset_index(drop=True, inplace=True)
    df2.rename({'Sentences': 'review'}, axis=1, inplace=True)
    # returns all sentences to filter each
    print(df2)
