import pandas as pd
from urllib.parse import urljoin
import re

def read_csv(name):
    """csv 파일을 읽고 반환"""
    print("csv 파일 읽기 시작")
    df = pd.read_csv(name)
    print("csv 파일 읽기 완료")
    return df

def get_df_ready(df):
    """데이터프레임을 딕셔너리 리스트로 변환"""
    print("데이터프레임을 딕셔너리 리스트로 변환 시작")
    data = df.to_dict('records')
    print("데이터프레임을 딕셔너리 리스트로 변환 완료")
    return data

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

