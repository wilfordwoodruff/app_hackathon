import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#List of Standard Works to use
books = ['BoM','D&C']

def clean_books(books):
#Makes all text lowercase, removes unnecessary columns, and filters to the books
    df = (pd.read_csv('../data/lds-scriptures.csv')
        .filter(['volume_short_title','book_lds_url','chapter_number','verse_number','scripture_text','verse_short_title'])
        .query("volume_short_title in @books")
        .drop(['volume_short_title','book_lds_url','verse_number','chapter_number'], axis=1)
        .assign(scripture_text=lambda x: x.scripture_text.str.lower())
        .reset_index(drop=True))
      
    return df
            

# included_books = ['OT','NT','BoM','D&C']
vectorizer = TfidfVectorizer()
standard_works = clean_books(books)


def find_standardworks(search_string):


    book_texts = standard_works['scripture_text']
    tfidf_matrix = vectorizer.fit_transform(book_texts)

    tfidf_matrix = vectorizer.fit_transform(book_texts)
    search_vector = vectorizer.transform([search_string])
    similarity_scores = cosine_similarity(search_vector, tfidf_matrix)
    best_match_index = similarity_scores.argmax()
    
    return standard_works['verse_short_title'][best_match_index],similarity_scores[0][best_match_index]


