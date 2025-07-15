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
from quotation_opt_detail import get_quotation_opt_detail

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [해외선물옵션] 기본시세 > 해외옵션종목상세 [해외선물-034]
##############################################################################################

def main():
    """
    해외옵션종목상세 조회 테스트 함수
    
    이 함수는 해외옵션종목상세 API를 호출하여 결과를 출력합니다.
    
    Returns:
        None
    """

    # pandas 출력 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
    pd.set_option('display.width', None)  # 출력 너비 제한 해제
    pd.set_option('display.max_rows', None)  # 모든 행 표시
    
    # 인증 토큰 발급
    kis.auth()
    
    # case1: SRS_CD: C5500
    logging.info("=== case1 조회 ===")
    try:
        result = get_quotation_opt_detail(srs_cd="C5500")
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    logging.info("사용 가능한 컬럼: %s", result.columns.tolist())
    
    # 컬럼명 한글 변환
    column_mapping = {
        'exch_cd': '거래소코드',
        'clas_cd': '품목종류',
        'crc_cd': '거래통화',
        'sttl_price': '전일종가',
        'sttl_date': '정산일',
        'trst_mgn': '증거금',
        'disp_digit': '가격표시진법',
        'tick_sz': '틱사이즈',
        'tick_val': '틱가치',
        'mrkt_open_date': '장개시일자',
        'mrkt_open_time': '장개시시각',
        'mrkt_close_date': '장마감일자',
        'mrkt_close_time': '장마감시각',
        'trd_fr_date': '상장일',
        'expr_date': '만기일',
        'trd_to_date': '최종거래일',
        'remn_cnt': '잔존일수',
        'stat_tp': '매매여부',
        'ctrt_size': '계약크기',
        'stl_tp': '최종결제구분',
        'frst_noti_date': '최초식별일'
    }
    
    result = result.rename(columns=column_mapping)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시 (메타데이터에 number 자료형 명시된 필드 없음)
    numeric_columns = []
    
    for col in numeric_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result)

if __name__ == "__main__":
    main() 