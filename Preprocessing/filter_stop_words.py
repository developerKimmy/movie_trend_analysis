from common import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

def filter_stop_words(review):
    # 불용어 목록
    stop_words = set(stopwords.words('english'))
    
    # 텍스트 토큰화
    tokens = word_tokenize(review)
    
    # 불용어 제거
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    return " ".join(filtered_tokens)

    
def main():
    print("메인 함수 시작: 불용어 제거")
    MOVIE_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\RAW DATA\\movie_reviews.csv"
    
    movie_reviews = read_csv(MOVIE_PATH)
    movie_reviews = get_df_ready(movie_reviews)
    
    filtered_list = []
    
    for review in tqdm(movie_reviews, desc="불용어 제거 중"):
        filtered = filter_stop_words(review['review'])
        tmp_review = {
            "movie_name" : review['movie_name'],
            "review": filtered
        }
        filtered_list.append(tmp_review)
    
    
    save_csv_df("filtered_stop_words.csv", ["movie_name", "review"], filtered_list)
    
if __name__ == "__main__":
    main()