from common import *
from imdb import IMDb
from tqdm import tqdm
import time

def get_movie_id(movie_list):
    imdb = IMDb()
    
    for movie in tqdm(movie_list, desc="영화 ID 추출 중"):
        try:
            search_results = imdb.search_movie(movie['movie_name'])
            if search_results:
                # 첫 번째 검색 결과 사용
                first_result = search_results[0]
                movie_id = first_result.movieID
                
                # 상세 정보 가져오기
                movie_obj = imdb.get_movie(movie_id)
                movie['movie_id'] = movie_obj.get('imdbID', '')
                movie['movie_title'] = movie_obj.get('title', '')
                
            time.sleep(1)
                
        except Exception as e:
            print(f"\n영화 '{movie['movie_name']}' 처리 중 오류 발생: {str(e)}")
            movie['movie_id'] = ""
            time.sleep(2)
            continue
            
    return movie_list

def get_movie_counts(movie_list, movie_reviews_df):
    print("\n리뷰 카운트 계산 시작")
    
    # 리스트에서 영화별 리뷰 수 계산
    review_counts = {}
    for review in movie_reviews_df:
        movie_name = review['movie_name']
        review_counts[movie_name] = review_counts.get(movie_name, 0) + 1
    
    print("\n영화별 리뷰 수:")
    for name, count in review_counts.items():
        print(f"{name}: {count}개")
    
    # movie_list 업데이트
    for movie in movie_list:
        before_count = movie['review_counts']
        movie['review_counts'] = review_counts.get(movie['movie_name'], 0)
        print(f"\n{movie['movie_name']}: {before_count} -> {movie['review_counts']}")
    
    print("\n리뷰 카운트 계산 완료")
    return movie_list

def main():
    print("Data Normalization 시작")
    
    BASE_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA"
    MOVIE_REVIEWS_PATH = f"{BASE_PATH}\\RAW DATA\\movie_reviews.csv"
    OUTPUT_REVIEWS_PATH = f"{BASE_PATH}\\PROCESSED DATA\\movie_reviews_with_id.csv"
    OUTPUT_MASTER_PATH = f"{BASE_PATH}\\PROCESSED DATA\\master_movie_list.csv"
    
    # 리뷰 데이터 읽기
    movie_reviews_df = read_csv(MOVIE_REVIEWS_PATH)
    movie_reviews_df = get_df_ready(movie_reviews_df)
    
    # 중복 제거된 영화 이름으로 movie_list 생성
    movie_names = set(review['movie_name'] for review in movie_reviews_df)
    movie_list = [{'movie_name': name, 'movie_id': '', 'movie_title': '', 'review_counts': 0} 
                 for name in movie_names]  # movie_title 필드 추가
    
    # ID와 title 추출
    movie_list = get_movie_id(movie_list)
    
    # movie_list를 딕셔너리로 변환 (ID와 title 정보 포함)
    movie_dict = {
        movie['movie_name']: {
        'id': movie['movie_id'],
        'title': movie['movie_title']  # movie_title 사용
    } for movie in movie_list}
    
    # 리뷰 데이터에 ID와 title 추가
    for review in movie_reviews_df:
        movie_info = movie_dict.get(review['movie_name'], {'id': '', 'title': review['movie_name']})
        review['movie_id'] = movie_info['id']
        review['movie_title'] = movie_info['title']
    
    # 원본 리뷰 데이터 저장 (모든 필드 포함)
    fieldnames = ['movie_id', 'movie_name', 'movie_title', 'review']
    save_csv_df(OUTPUT_REVIEWS_PATH, fieldnames, movie_reviews_df)
    
    # 마스터 데이터 생성 및 저장 (모든 필드 포함)
    movie_list = get_movie_counts(movie_list, movie_reviews_df)
    save_csv_df(OUTPUT_MASTER_PATH, ['movie_id', 'movie_name', 'movie_title', 'review_counts'], movie_list)
    
    print("Data Normalization 완료")
    
if __name__ == "__main__":
    main()

    
    
