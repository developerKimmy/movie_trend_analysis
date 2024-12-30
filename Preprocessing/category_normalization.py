from common import *
import random

def get_unique_genres(movie_list):
    print("고유 장르 추출 시작")
    
    genres = set()
    for movie in movie_list:
        genres.update(movie['genres'])
    
    print(f"고유 장르 추출 완료 : {len(genres)}개")
    return genres

def get_unique_countries(movie_list):
    print("고유 국가 추출 시작")
    
    countries = set()
    for movie in movie_list:
        countries.update(movie['countries'])
    
    print(f"고유 국가 추출 완료 : {len(countries)}개")
    return countries

def get_unique_years(movie_list):
    print("고유 연도 추출 시작")
    
    years = set()
    for movie in movie_list:
        years.add(movie['year'])
    
    print(f"고유 연도 추출 완료 : {len(years)}개")
    return years

def get_unique_codes(category, detail_list):
    print(f"{category} 고유 코드 추출 시작")
    
    CODE_CATEGORY = {
        "genres" : [10000, 20000],
        "countries" : [30000, 40000],
        "year" : [50000, 60000]
    }
    
    # 사용된 코드를 추적하기 위한 set
    used_codes = set()
    category_code = []
    code_range = CODE_CATEGORY[category]
    
    '''
    단순하게 code 만 넣어서는 찾을 수 없잖아.. 
    이름 하고 같이 넣어줘야지 바보야
    '''
    for item in detail_list:
        while True:
            random_code = random.randint(code_range[0], code_range[1])
            if random_code not in used_codes:
                used_codes.add(
                    {
                        "name" : item,
                        "code" : random_code
                    }
                )
                category_code.append(
                    {
                        "name" : item,
                        "code" : random_code
                    }
                )
                break
    
    print(f"{category} 코드 생성 완료: {len(category_code)}개")
    return category_code
    

def main():
    print("카테고리 정규화 시작")
    
    movie_df = read_csv("C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\RAW DATA\\movie_details.csv")
    movie_list = get_df_ready(movie_df)
    
    #장르
    unique_genres = get_unique_genres(movie_list)
    genres_code = get_unique_codes("genres", unique_genres)
    save_csv_df("genres_code.csv", ["genres", "genres_code"], genres_code)
    
    #국가
    unique_countries = get_unique_countries(movie_list)
    countries_code = get_unique_codes("countries", unique_countries)
    save_csv_df("countries_code.csv", ["countries", "countries_code"], countries_code)
    
    #연도
    unique_years = get_unique_years(movie_list)
    years_code = get_unique_codes("year", unique_years)
    save_csv_df("years_code.csv", ["years", "years_code"], years_code)
    
if __name__ == "__main__":
    main()