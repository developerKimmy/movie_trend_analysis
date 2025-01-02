from common import *
import os

def read_detail_csv(MOVIE_DETAIL_PATH): 
    all_dict = {}
    print("장르별로 detail 파일 들고 오기")
    
    for category in os.listdir(MOVIE_DETAIL_PATH):
        folder_path = os.path.join(MOVIE_DETAIL_PATH, category)
        if os.path.isdir(folder_path):
            print(f"{category} 읽는 중")
            
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(folder_path, file_name)
                    file_name = file_name.replace(".csv","")
                    if file_name not in all_dict:
                        all_dict[file_name] = []
                    
                    # CSV 파일 읽기
                    df = pd.read_csv(file_path)
                    data = get_df_ready(df)
                    all_dict[file_name].append(data)  
    
    return all_dict

def get_filter_reviews(all_detail_dict, MOVIE_REVIEW_PATH):
    print("review 필터 함수 호출")
    reviews = read_csv(MOVIE_REVIEW_PATH)
    reviews_list = get_df_ready(reviews)
    
    filtered_review = {}
    
    for key in all_detail_dict:
        filtered_review[key] = []
        for details in all_detail_dict[key]:
            for detail in details:
                for review in reviews_list:
                    if detail['imdbID'] == review['imdbID']:
                        filtered_review[key].append(review)  # 해당 키에 리뷰 추가
                        break
    
    print(len(reviews_list))
    
    return filtered_review


def export_csv(sub_categories, main_category):
    print("csv로 저장하기")        
    for key, value in sub_categories.items():
        filename = f"{main_category}_{key}"
        
        df = pd.DataFrame(value)  
        df.to_csv(filename, index=False, encoding='utf-8-sig')  
        print(f"Saved {filename}")
    print("csv로 저장 완료")    

def main():
    print("main 함수 호출")
    
    MOVIE_DETAIL_PATH = 'C:\\Users\\Suin Kim\\Desktop\\portfolio\\movies\\categorized\\detail'
    MOVIE_REVIEW_PATH = 'C:\\Users\\Suin Kim\\Desktop\\portfolio\\movies\\review_data\\all_reviews.csv'
    
    all_detail_dict = read_detail_csv(MOVIE_DETAIL_PATH)
    filtered_reviews = get_filter_reviews(all_detail_dict, MOVIE_REVIEW_PATH)
    
    for key in filtered_reviews:
        df = pd.DataFrame(filtered_reviews[key])  
        save_as_csv(key, df)
        
if __name__ == "__main__":
    main()