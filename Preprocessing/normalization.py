from common import *
from imdb import IMDb
from tqdm import tqdm

def get_movie_id(ID_list):
    imdb = IMDb()
    
    for key in tqdm(ID_list, desc="영화 ID 추출 중"):
        result =imdb.search_movie(key)
        if result:
            movie = result[0]
            
            imdb.update(movie)
            
            ID_list[key] = movie.get("imdbID")
            
    return ID_list
            
def update_reviews_with_id(movie_reviews_df, ID_list):
    print("리뷰 데이터에 영화 ID 추가 중...")
    
    for review in movie_reviews_df:
        movie_name = review["movie_name"]
        if movie_name in ID_list:
            review["movie_id"] = ID_list[movie_name]
    
    return movie_reviews_df

def main():
    print("Normalization")
    
    MOVIE_DETAILS_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\RAW DATA\\movie_details.csv"
    MOVIE_REVIEWS_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\RAW DATA\\movie_reviews.csv"
     
    movie_details_df = read_csv(MOVIE_DETAILS_PATH)
    movie_reviews_df = read_csv(MOVIE_REVIEWS_PATH)
    
    movie_details_df = get_df_ready(movie_details_df)
    movie_reviews_df = get_df_ready(movie_reviews_df)
    
    ID_list = {}
    for review in movie_reviews_df:
        ID_list[review["movie_name"]] = ""
    
    ID_list = get_movie_id(ID_list)
    
    # ID를 리뷰 데이터에 추가
    movie_reviews_df = update_reviews_with_id(movie_reviews_df, ID_list)
    
    # 결과 저장
    fieldnames = list(movie_reviews_df[0].keys()) if movie_reviews_df else []
    save_csv_df("movie_reviews_with_id.csv", fieldnames, movie_reviews_df)

    
if __name__ == "__main__":
    main()