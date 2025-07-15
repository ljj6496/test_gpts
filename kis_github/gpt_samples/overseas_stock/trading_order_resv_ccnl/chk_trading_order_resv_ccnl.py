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
from trading_order_resv_ccnl import get_trading_order_resv_ccnl

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [해외주식] 주문/계좌 > 해외주식 예약주문접수취소[v1_해외주식-004]
##############################################################################################

def main():
    """
    해외주식 예약주문접수취소 조회 테스트 함수
    
    이 함수는 해외주식 예약주문접수취소 API를 호출하여 결과를 출력합니다.
    
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
    logging.info("=== Case1 테스트 ===")
    try:
        result = get_trading_order_resv_ccnl(
            env_dv="real",
            nat_dv="us", 
            cano="81180744",
            acnt_prdt_cd="01",
            rsyn_ord_rcit_dt="20220810",
            ovrs_rsvn_odno="0030008244"
        )
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    logging.info("사용 가능한 컬럼: %s", result.columns.tolist())
    
    # 컬럼명 한글 변환 및 데이터 출력
    column_mapping = {
        'OVRS_RSVN_ODNO': '해외예약주문번호'
    }
    
    result = result.rename(columns=column_mapping)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시 (메타데이터에 number 자료형 없음)
    numeric_columns = []
    
    for col in numeric_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result)

if __name__ == "__main__":
    main() 