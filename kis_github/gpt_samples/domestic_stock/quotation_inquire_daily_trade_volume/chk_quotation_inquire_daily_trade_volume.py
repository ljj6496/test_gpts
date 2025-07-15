"""
Created on 20250126
@author: LaivData SJPark with cursor
"""
import os
import sys
import logging

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import kis_auth as kis
from quotation_inquire_daily_trade_volume import get_quotation_inquire_daily_trade_volume

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [국내주식] 시세분석 > 종목별일별매수매도체결량 [v1_국내주식-056]
##############################################################################################

def main():
    """
    종목별일별매수매도체결량 조회 테스트 함수
    
    이 함수는 종목별일별매수매도체결량 API를 호출하여 결과를 출력합니다.
    테스트 데이터로 삼성전자(005930)를 사용합니다.
    
    Returns:
        None
    """

    # pandas 출력 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
    pd.set_option('display.width', None)  # 출력 너비 제한 해제
    pd.set_option('display.max_rows', None)  # 모든 행 표시
    
    # 인증 토큰 발급
    kis.auth()
    
    # case1 테스트
    logging.info("=== case1 테스트 ===")
    try:
        result1, result2 = get_quotation_inquire_daily_trade_volume(
            fid_cond_mrkt_div_code="J",
            fid_input_iscd="005930",
            fid_period_div_code="D"
        )
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    # output1 처리
    logging.info("=== output1 결과 ===")
    logging.info("사용 가능한 컬럼: %s", result1.columns.tolist())
    
    # 컬럼명 한글 변환
    column_mapping1 = {
        'shnu_cnqn_smtn': '매수 체결량 합계',
        'seln_cnqn_smtn': '매도 체결량 합계'
    }
    
    result1 = result1.rename(columns=column_mapping1)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시 (메타데이터에 number 자료형이 명시되지 않았으므로 없음)
    numeric_columns = []
    
    for col in numeric_columns:
        if col in result1.columns:
            result1[col] = pd.to_numeric(result1[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result1)
    
    # output2 처리
    logging.info("=== output2 결과 ===")
    logging.info("사용 가능한 컬럼: %s", result2.columns.tolist())
    
    # 컬럼명 한글 변환
    column_mapping2 = {
        'stck_bsop_date': '주식 영업 일자',
        'total_seln_qty': '총 매도 수량',
        'total_shnu_qty': '총 매수 수량'
    }
    
    result2 = result2.rename(columns=column_mapping2)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시 (메타데이터에 number 자료형이 명시되지 않았으므로 없음)
    numeric_columns = []
    
    for col in numeric_columns:
        if col in result2.columns:
            result2[col] = pd.to_numeric(result2[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result2)

if __name__ == "__main__":
    main() 