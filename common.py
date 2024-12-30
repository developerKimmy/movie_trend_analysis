import pandas as pd
import csv
from urllib.parse import urljoin
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def read_csv(name):
    """csv 파일을 읽고 반환"""
    print("csv 파일 읽기 시작")
    df = pd.read_csv(name)
    print("csv 파일 읽기 완료")
    return df

def get_all_paths(PATH):
    """폴더 내의 모든 파일 경로를 반환"""
    print("폴더 내의 모든 파일 경로 반환 시작")
    paths = [os.path.join(PATH, file) for file in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, file))]
    print("폴더 내의 모든 파일 경로 반환 완료")
    return paths

def get_file_name(path):
    """파일 경로에서 파일 이름을 반환"""
    print("파일 경로에서 파일 이름 반환 시작")
    file_name, file_extension = os.path.basename(path).split(".")
    
    file_name_data = {
        "file_name": file_name,
        "file_extension": file_extension
    }
    print("파일 경로에서 파일 이름 반환 완료")
    return file_name_data

def get_df_ready(df):
    """데이터프레임을 딕셔너리 리스트로 변환"""
    print("데이터프레임을 딕셔너리 리스트로 변환 시작")
    data = df.to_dict('records')
    print("데이터프레임을 딕셔너리 리스트로 변환 완료")
    return data

def save_csv_df(file_name, fieldnames, data):
    try:
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"데이터가 {file_name} 파일로 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"CSV 저장 중 오류 발생: {e}")

def get_joined_url(url, href):
    """기본 URL과 상대 경로를 결합"""
    print("기본 URL과 상대 경로를 결합 시작")
    url = urljoin(url, href)
    print("기본 URL과 상대 경로를 결합 완료")
    return url

def get_text_cleaned(text):
    """텍스트에서 특수문자와 숫자 제거"""
    print("텍스트에서 특수문자와 숫자 제거 시작")
    text = re.sub(r'[^\w\s]', '', text)  # 특수문자 제거
    text = re.sub(r'\d+', '', text)  # 숫자 제거
    print("텍스트에서 특수문자와 숫자 제거 완료")
    return text

def init_driver():
    """Chrome WebDriver 초기화"""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def get_BeautifulSoup_ready(url, driver):
    """웹 페이지 파싱을 위한 BeautifulSoup 객체 생성"""
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'html.parser')

def reload_soup(driver):
    """현재 페이지의 BeautifulSoup 객체 새로 생성"""
    return BeautifulSoup(driver.page_source, 'html.parser')

def wait_for_element(driver, element_class):
    """지정된 클래스 이름을 가진 요소가 나타날 때까지 대기"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, element_class))
    )

