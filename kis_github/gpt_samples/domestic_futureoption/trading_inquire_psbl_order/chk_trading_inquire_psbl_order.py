"""
Created on 20250115 
@author: LaivData SJPark with cursor
"""
import os
import sys
import logging

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import kis_auth as kis
from trading_inquire_psbl_order import get_trading_inquire_psbl_order

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [국내선물옵션] 주문/계좌 > 선물옵션 주문가능[v1_국내선물-005]
##############################################################################################

def main():
    """
    선물옵션 주문가능 조회 테스트 함수
    
    이 함수는 선물옵션 주문가능 API를 호출하여 결과를 출력합니다.
    테스트 데이터로 실전 환경의 선물옵션 계좌를 사용합니다.
    
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
        result = get_trading_inquire_psbl_order(
            env_dv="real",
            cano="81180744",
            acnt_prdt_cd="03",
            pdno="101S03",
            sll_buy_dvsn_cd="02",
            unit_price="1",
            ord_dvsn_cd="01"
        )
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    logging.info("사용 가능한 컬럼: %s", result.columns.tolist())
    
    # 컬럼명 한글 변환 및 데이터 출력
    column_mapping = {
        'tot_psbl_qty': '총가능수량',
        'lqd_psbl_qty1': '청산가능수량1', 
        'ord_psbl_qty': '주문가능수량',
        'bass_idx': '기준지수'
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