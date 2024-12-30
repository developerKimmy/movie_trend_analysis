from imdb import IMDb
from common import *

def get_unique_movie_names(movie_list):
    print("영화 이름 추출 시작")
    movie_names = set()
    for movie in movie_list:
        movie_name = movie["name"]
        movie_names.add(movie_name)
    print("영화 이름 추출 완료")
    return movie_names

def get_movie_with_search(movie_name):
    print(f"\n{'='*50}")
    print(f"영화 '{movie_name}' 상세 정보 추출 시작")
    ia = IMDb()
    
    search_results = ia.search_movie(movie_name)
    if not search_results:
        print(f"검색 결과 없음: {movie_name}")
        return None
    
    # 첫 번째 검색 결과만 사용
    movie = search_results[0]
    print(f"영화 이름 : {movie_name}")
    print(f"영화 검색 결과 : {movie}")
    movie_id = movie.movieID
    movie_obj = ia.get_movie(movie_id)
    
    # 원하는 필드만 추출
    movie_detail = {
        "imdbID": movie_obj.get("imdbID", ""),
        "title": movie_obj.get("title", ""),
        "year": movie_obj.get("year", ""),
        "kind": movie_obj.get("kind", ""),
        "genres": movie_obj.get("genres", []),
        "original title": movie_obj.get("original title", ""),\
        "localized title": movie_obj.get("localized title", ""),
        "rating": movie_obj.get("rating", ""),
        "country": movie_obj.get("country", ""),
        "countries": movie_obj.get("countries", [])
    }
    
    print("\n1. 추출된 기본 데이터:")
    print(movie_detail)
    
    # 기본 행 생성 (리스트가 아닌 값들)
    base_row = {k: str(v).strip() if v is not None else '' 
                for k, v in movie_detail.items() 
                if not isinstance(v, list)}
    
    print("\n2. 리스트가 아닌 기본 데이터:")
    print(base_row)
    
    result_rows = [base_row.copy()]
    
    # 리스트 형태의 값들 처리
    print("\n3. 리스트 형태의 데이터 처리:")
    for key, value in movie_detail.items():
        if isinstance(value, list):
            print(f"\n키 '{key}'의 리스트 이터: {value}")
            new_rows = []
            for current_row in result_rows:
                for item in value:
                    new_row = current_row.copy()
                    new_row[key] = str(item).strip()
                    new_rows.append(new_row)
            result_rows = new_rows
            print(f"현재 생성된 행 수: {len(result_rows)}")
    
    print(f"\n4. 최종 생성된 행 수: {len(result_rows)}")
    print(f"첫 번째 행 예시:")
    print(result_rows[0] if result_rows else "없음")
    print(f"{'='*50}\n")
    
    return result_rows

def main():
    print("main 함수 시작")
    
    # 파일 경로 설정
    input_path = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\RAW DATA\\movies.csv"
    
    movie_df = read_csv(input_path)
    movie_list = get_df_ready(movie_df)
    movie_names = get_unique_movie_names(movie_list)
    print(f"영리할 총 영화 수: {len(movie_names)}")
    
    # 성공/실패 데이터를 저장할 리스트
    success_rows = []
    failed_movies = []
    processed_count = 0
    
    for movie_name in movie_names:
        processed_count += 1
        print(f"\n처리 중: {processed_count}/{len(movie_names)} - {movie_name}")
        
        movie_rows = get_movie_with_search(movie_name)
        if movie_rows:
            success_rows.extend(movie_rows)
            print(f"성공 케이스 누적 행 수: {len(success_rows)}")
        else:
            failed_movies.append({"name": movie_name})
            print(f"실패 케이스 누적 수: {len(failed_movies)}")
    
    # 성공 케이스 저장
    if success_rows:
        fieldnames = list(success_rows[0].keys())
        print("\n성공 케이스 최종 필드명:")
        print(fieldnames)
        
        save_csv_df("movie_details.csv", fieldnames, success_rows)
        print(f"\n성공한 영화 데이터 저장 완료:")
        print(f"- 총 행 수: {len(success_rows)}")
    
    # 실패 케이스 저장
    if failed_movies:
        fieldnames = ["name"]
        save_csv_df("failed_movies.csv", fieldnames, failed_movies)
        print(f"\n실패한 영화 데이터 저장 완료:")
        print(f"- 총 개수: {len(failed_movies)}")
    
    # 최종 통계 출력
    print(f"\n처리 완료 통계:")
    print(f"- 전체 영화 수: {len(movie_names)}")
    print(f"- 성공한 영화 데이터 행 수: {len(success_rows)}")
    print(f"- 실패한 영화 수: {len(failed_movies)}")

if __name__ == "__main__":
    main()

