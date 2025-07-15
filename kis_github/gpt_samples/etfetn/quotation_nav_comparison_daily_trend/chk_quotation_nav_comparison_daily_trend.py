"""
Created on 20250601 
@author: LaivData SJPark with cursor
"""
import os
import sys
import logging

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import kis_auth as kis
from quotation_nav_comparison_daily_trend import get_quotation_nav_comparison_daily_trend

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [국내주식] 기본시세 > NAV 비교추이(일)[v1_국내주식-071]
##############################################################################################

def main():
    """
    NAV 비교추이(일) 조회 테스트 함수
    
    이 함수는 NAV 비교추이(일) API를 호출하여 결과를 출력합니다.
    테스트 데이터로 KODEX 200 ETF(069500)를 사용합니다.
    
    Returns:
        None
    """

    # pandas 출력 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
    pd.set_option('display.width', None)  # 출력 너비 제한 해제
    pd.set_option('display.max_rows', None)  # 모든 행 표시
    
    # 인증 토큰 발급
    kis.auth()
    
    # case1 조회
    logging.info("=== case1 조회 ===")
    try:
        result = get_quotation_nav_comparison_daily_trend(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="069500",
            fid_input_date_1="20240101",
            fid_input_date_2="20240220"
        )
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    logging.info("사용 가능한 컬럼: %s", result.columns.tolist())
    
    # 컬럼명 한글 변환 및 데이터 출력
    column_mapping = {
        'stck_bsop_date': '주식 영업 일자',
        'stck_clpr': '주식 종가',
        'prdy_vrss': '전일 대비',
        'prdy_vrss_sign': '전일 대비 부호',
        'prdy_ctrt': '전일 대비율',
        'acml_vol': '누적 거래량',
        'cntg_vol': '체결 거래량',
        'dprt': '괴리율',
        'nav_vrss_prpr': 'NAV 대비 현재가',
        'nav': 'NAV',
        'nav_prdy_vrss_sign': 'NAV 전일 대비 부호',
        'nav_prdy_vrss': 'NAV 전일 대비',
        'nav_prdy_ctrt': 'NAV 전일 대비율'
    }
    
    result = result.rename(columns=column_mapping)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시
    numeric_columns = ['전일 대비', '전일 대비율', 'NAV 전일 대비율']
    
    for col in numeric_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result)

if __name__ == "__main__":
    main() 