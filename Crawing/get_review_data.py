from common import *
import time

def click_button_to_load(driver, button_xpath, pause_time= 10):
    print("모두 보기 버튼 클릭하기")
    try:
        # 버튼이 로드될 때까지 대기
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        # 버튼 클릭
        # button.click()
        driver.execute_script("arguments[0].click();", button)
        time.sleep(pause_time)  # 클릭 후 로딩 시간 대기
    except Exception as e:
        print(f"버튼 클릭 중 오류 발생: {e}")
        
def scroll_to_load_all(driver, pause_time=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # 페이지 끝까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)  # 데이터가 로드될 시간을 줌

        # 새 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # 더 이상 로드되는 데이터가 없으면 종료
            break
        last_height = new_height
        
def is_matched(movie, driver):
    print("동일한 영화가 맞는지 확인하기")
    
    soup = get_BeautifulSoup_ready(movie["url"], driver)
    section_tag = soup.find('section', class_="ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-9a2a0028-2 byEUZE")
    h1_tag = section_tag.find('h1')
    span_tag = h1_tag.find('span', class_="hero__primary-text")
    
    movie_title = span_tag.get_text()
    
    if movie_title == movie['name']:
        return True
    else:
        return False

def get_review_url(movie, driver):
    print("리뷰 링크 구하기")
    
    soup = get_BeautifulSoup_ready(movie["url"], driver)
    section_tag = soup.find('section', attrs={'data-testid': 'UserReviews'})
    title_wrapper = section_tag.find('div', class_ = "ipc-title__wrapper")
    a_tag = title_wrapper.find('a', class_ = "ipc-title-link-wrapper")
    href = a_tag.get('href')
    review_url = get_joined_url(movie['url'], href)
    
    return review_url

def find_inner_div(outer_div):
    inner_div = outer_div.find('div', class_="ipc-html-content-inner-div")
    if not inner_div:
        print("Inner div를 찾을 수 없습니다.")
        return None  # None 반환
    else:
        return inner_div.get_text(strip=True)  # 공백 제거


def get_review_data(review_url, movie_name, driver):
    print("리뷰 데이터 구하기")
    
    review_data = []
    
    button_xpath = "//span[contains(@class, 'ipc-see-more') and contains(@class, 'sc-f09bd1f5-2')]/button[contains(@class, 'ipc-btn--single-padding') and contains(@class, 'ipc-see-more__button')]"
   
    soup = get_BeautifulSoup_ready(review_url, driver)
    click_button_to_load(driver, button_xpath, 5)
    scroll_to_load_all(driver, 30)
    soup = reload_soup(driver)
    
    section_tag = soup.find('section', class_="ipc-page-section ipc-page-section--base ipc-page-section--sp-pageMargin")
    if not section_tag:
        print("Section 태그를 찾을 수 없습니다.")
        return []
   
    article_tags = section_tag.find_all('article', class_="sc-d99cd751-1 kzUfxa user-review-item")
    if not article_tags:
        print("Article 태그를 찾을 수 없습니다.")
        return []
    else:
        print(len(article_tags))
        for article_tag in article_tags:
            outer_div = article_tag.find('div', attrs={'data-testid': 'review-card-parent'})
            if not outer_div:
                print("리뷰 card parent div를 찾을 수 없습니다.")
                continue

            second_div = outer_div.find('div', class_="ipc-list-card__content")
            if not second_div:
                print("Second div를 찾을 수 없습니다.")
                text = find_inner_div(outer_div)
                if text:  # None이 아니면 추가
                    review_data.append(text)
                continue

            third_div = second_div.find('div', attrs={'data-testid': 'review-overflow'})
            if not third_div:
                print("Third div를 찾을 수 없습니다.")
                text = find_inner_div(second_div)
                if text:
                    review_data.append(text)
                continue

            fourth_div = third_div.find('div', class_="ipc-overflowText--children")
            if not fourth_div:
                print("Fourth div를 찾을 수 없습니다.")
                text = find_inner_div(third_div)
                if text:
                    review_data.append(text)
                continue

            fifth_div_list = fourth_div.find_all('div', class_="ipc-html-content ipc-html-content--base")
            if not fifth_div_list:
                print("Fifth div를 찾을 수 없습니다.")
                text = find_inner_div(fourth_div)
                if text:
                    review_data.append(text)
                continue

            for fifth_div in fifth_div_list:
                text = find_inner_div(fifth_div)
                if text:
                    # 리뷰 텍스트를 딕셔너리 형태로 저장
                    review_dict = {
                        "movie_name": movie_name,
                        "review": text
                    }
                    print(f"리뷰 데이터 (반복문 안) : {review_dict}")
                    
                    review_data.append(review_dict)
        print(f"리뷰 데이터 (반복문 밖) : {review_data}")
        return review_data
    
def main():
    driver = init_driver()
    df = read_csv("movies.csv")
    movie_list = get_df_ready(df)
    
    # 모든 리뷰를 저장할 리스트 생성
    all_reviews = []
    
    try:
        for movie in movie_list:
            print(f"현재 처리중인 영화: {movie['name']}")  # 진행상황 확인용
            matched = is_matched(movie, driver)
            if matched == True:
                review_url = get_review_url(movie, driver)
                review_data = get_review_data(review_url, movie['name'], driver)
                # 리뷰 데이터를 누적
                all_reviews.extend(review_data)
                print(f"{movie['name']}의 리뷰 {len(review_data)}개 수집 완료")
    finally:
        # 모든 영화의 리뷰를 한 번에 저장
        if all_reviews:
            print(f"총 {len(all_reviews)}개의 리뷰 저장 시작")
            save_csv_df("movie_reviews.csv", ["movie_name", "review"], all_reviews)
            print("저장 완료")
        driver.quit()
    
if __name__ == "__main__":
    main()
