"""
Created on 20250113 
@author: LaivData SJPark with cursor
"""
import os
import sys
import logging

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import kis_auth as kis
from quotation_rights_by_ice import get_quotation_rights_by_ice

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [해외주식] 시세분석 > 해외주식 권리종합 [해외주식-050]
##############################################################################################

def main():
    """
    해외주식 권리종합 조회 테스트 함수
    
    이 함수는 해외주식 권리종합 API를 호출하여 결과를 출력합니다.
    테스트 데이터로 NVDL(US) 종목을 사용합니다.
    
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
        result = get_quotation_rights_by_ice(ncod="US", symb="NVDL")
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    logging.info("사용 가능한 컬럼: %s", result.columns.tolist())
    
    # 컬럼명 한글 변환 및 데이터 출력
    column_mapping = {
        'anno_dt': 'ICE공시일',
        'ca_title': '권리유형',
        'div_lock_dt': '배당락일',
        'pay_dt': '지급일',
        'record_dt': '기준일',
        'validity_dt': '효력일자',
        'local_end_dt': '현지지시마감일',
        'lock_dt': '권리락일',
        'delist_dt': '상장폐지일',
        'redempt_dt': '상환일자',
        'early_redempt_dt': '조기상환일자',
        'effective_dt': '적용일'
    }
    
    result = result.rename(columns=column_mapping)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시
    numeric_columns = []
    
    for col in numeric_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result)

if __name__ == "__main__":
    main() 