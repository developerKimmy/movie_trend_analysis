from common import *

def get_filtered_by_year(movie_list):
    print("연도별로 구분하기")
    

    '''
    unique_year = set()
    for movie in movie_list:
        unique_year.add(movie["year"])
    print(unique_year)
    
    반환 값 :{1924, 1925, 1926, 1927, 1928, 1931, 1936, 1939, 1940, 1941, 1942, 1944, 1946, 1948, 1949, 1950, 1952, 1953, 1954, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1965, 1966, 1967, 1968, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023, 2024}
    '''
    decade_dict = {f"{year}s": [] for year in range(1920, 2030, 10)}

    for movie in movie_list:
        year = movie['year']
        for decade in range(1920, 2030, 10):
            if decade <= year <= decade + 9:  
                decade_dict[f"{decade}s"].append(movie)
                break  
            
    
    print("연도별로 구분 완료")
    
    return decade_dict

def get_filtered_by_countries(movie_list):
    print("국가별로 구분하기")
    
    unique_countries = set()
    for movie in movie_list:
        unique_countries.add(movie["countries"])

    country_dict = {country: [] for country in unique_countries}
    for movie in movie_list:
        country = movie["countries"]
        country_dict[country].append(movie)  # 직접 country 변수 사용
    
    print("국가별로 구분 완료")
    return country_dict

    
def get_filtered_by_genres(movie_list):
    print("장르별로 구분하기")
    
    unique_genres = set()
    for movie in movie_list:
        unique_genres.add(movie['genres'])
        
    genre_dict = {genre: [] for genre in unique_genres}
    for movie in movie_list:
        genre = movie['genres']
        genre_dict[genre].append(movie)  # 직접 genre 변수 사용
    
    print("장르별로 구분 완료")
    return genre_dict

def export_csv(sub_categories, main_category):
    print("csv로 저장하기")        
    for key, value in sub_categories.items():
        filename = f"C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA\\PROCESSED DATA\\DETAILS\\{main_category}_{key}.csv"
        save_csv_df(filename,['imdbID','title','year','kind','original title','localized title','rating','genres','country','countries'], value)
        print(f"Saved {filename}")
    print("csv로 저장 완료")    
    
def main():
    print("main 함수 호출")
    
    # detail 파일 읽기
    BASE_PATH = "C:\\Users\\Suin Kim\\Desktop\\movie_trend_analysis\\DATA"
    MOVIE_DETAIL_PATH = f"{BASE_PATH}\\RAW DATA\\movie_details.csv"
    df = read_csv(MOVIE_DETAIL_PATH)
    
    movie_list = get_df_ready(df)
    
    year = get_filtered_by_year(movie_list)
    export_csv(year, "year")
    country = get_filtered_by_countries(movie_list)
    export_csv(country, "country")
    genre = get_filtered_by_genres(movie_list)
    export_csv(genre, "genre")
    
    print("main 함수 완료")
    
if __name__ == "__main__":
    main()