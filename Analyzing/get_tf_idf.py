from common import *
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk

    
def main():
    MOVIE_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\FILTERED\\filtered_stop_words.csv"
    movie_reviews = read_csv(MOVIE_PATH)
    movie_reviews = get_df_ready(movie_reviews)
    
    
    
if __name__ == "__main__":
    main()
