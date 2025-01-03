from common import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def filter_stop_words(review):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(review)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return " ".join(filtered_tokens)

def main():
    MOVIE_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\PROCESSED DATA\\REVIEWS"
    
    all_paths = get_all_paths(MOVIE_PATH)
    
    # TF-IDF 계산기 초기화
    tfidf_vectorizer = TfidfVectorizer()
    
    tfidf_results = []

    for path in all_paths:
        name = get_file_name(path) 
        movie_reviews = read_csv(path)
        movie_reviews = get_df_ready(movie_reviews)
        
        processed_reviews = []
        for review in movie_reviews:
            review_text = review['review']
            review_text = filter_stop_words(review_text)
            processed_reviews.append(review_text)
        
        tfidf_matrix = tfidf_vectorizer.fit_transform(processed_reviews)
        feature_names = tfidf_vectorizer.get_feature_names_out()
        
        for doc_id, row in enumerate(tfidf_matrix):
            for col_id, tfidf_value in zip(row.indices, row.data):
                print(feature_names[col_id])
                print(tfidf_value)
if __name__ == "__main__":
    main()
