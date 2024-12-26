from common import *

def get_url_list(driver):
    url_list = set() 
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    
    soup = get_BeautifulSoup_ready(url, driver)
    
    try:
        wait_for_element(driver, 'ipc-metadata-list')
        # BeautifulSoup으로 페이지 파싱
        soup = reload_soup(driver)
        
        ul_tag = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 iyTDQy compact-list-view ipc-metadata-list--base')

        if ul_tag:
            links = ul_tag.find_all('li')
            for link in links:
                a_tag = link.find('a')
                href = a_tag.get('href')
                selected_url = urljoin(url, href)
                url_list.add(selected_url)
                
    except Exception as e:
        print(f"오류 발생: {e}")

    return url_list
    
def get_names_from_url(url_list, driver):
    data = []  
    
    for movie_url in url_list:
        url = movie_url
        soup = get_BeautifulSoup_ready(url, driver)
        
        try:
            section_tag = soup.find('section', class_="ipc-page-section ipc-page-section--baseAlt ipc-page-section--tp-none ipc-page-section--bp-xs sc-9a2a0028-2 byEUZE")
            h1_tag = section_tag.find('h1')
            span_tag = h1_tag.find('span', class_="hero__primary-text")
            
            # 영화 이름 추출
            movie = span_tag.get_text()
            
            # 데이터 추가
            item = {"url": url, "name": movie}
            data.append(item)
        
        except AttributeError:
            print(f"URL 처리 중 오류: {url}")
            continue
        
    save_csv_df("movies.csv", ["url", "name"], data)
    
    print("CSV 파일 저장 완료")
    
def main():
    driver = init_driver()
    try:
        url_list = get_url_list(driver)
        get_names_from_url(url_list, driver)
    finally:
        driver.quit()
if __name__ == "__main__":
    main()  
