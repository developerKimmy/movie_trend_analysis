from common import *

def get_filter_reviews(movie_revie_list, MOVIE_DETAIL_PATH):
    movie_detail_list = read_csv(MOVIE_DETAIL_PATH)
    movie_detail_list = get_df_ready(movie_detail_list)

    
    filtered_review = []
    
    for movie in movie_detail_list:
        for review in movie_revie_list:
            if movie['imdbID'] == review['movie_id']:
                filtered_review.append(review)

    return filtered_review

def main():
    print("main 함수 호출")
    BASE_PATH = 'C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\PROCESSED DATA\\REVIEWS\\'
    MOVIE_DETAIL_PATH = 'C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\PROCESSED DATA\\DETAILS'
    MOVIE_REVIEW_PATH = 'C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\RAW DATA\\movie_reviews_with_id.csv'
    
    movie_review_list = read_csv(MOVIE_REVIEW_PATH)
    movie_review_list = get_df_ready(movie_review_list)
    
    all_paths = get_all_paths(MOVIE_DETAIL_PATH)
    for path in all_paths:
        filtered_review = get_filter_reviews(movie_review_list, path)
        file_name = get_file_name(path)
        save_csv_df(f"{BASE_PATH}{file_name['file_name']}_review.csv", ['movie_id','movie_name','movie_title','review'], filtered_review)
        
if __name__ == "__main__":
    main()