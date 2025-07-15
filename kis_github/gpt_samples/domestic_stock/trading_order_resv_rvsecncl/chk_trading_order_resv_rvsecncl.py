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
from trading_order_resv_rvsecncl import post_trading_order_resv_rvsecncl

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [국내주식] 주문/계좌 > 주식예약주문정정취소[v1_국내주식-018,019]
##############################################################################################

def main():
    """
    주식예약주문정정취소 조회 테스트 함수
    
    이 함수는 주식예약주문정정취소 API를 호출하여 결과를 출력합니다.
    
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
        result = post_trading_order_resv_rvsecncl(
            cano="81180744",
            acnt_prdt_cd="01",
            rsvn_ord_seq="88793",
            rsvn_ord_orgno="001",
            rsvn_ord_ord_dt="20250113",
            ord_type="cancel",
            pdno="005930",
            ord_qty="2",
            ord_unpr="55000",
            sll_buy_dvsn_cd="02",
            ord_dvsn_cd="00",
            ord_objt_cblc_dvsn_cd="10"
        )
    except ValueError as e:
        logging.error("에러 발생: %s" % str(e))
        return
    
    logging.info("사용 가능한 컬럼: %s", result.columns.tolist())
    
    # 컬럼명 한글 변환 및 데이터 출력
    column_mapping = {
        'nrml_prcs_yn': '정상처리여부'
    }
    
    result = result.rename(columns=column_mapping)
    
    # 숫자형 컬럼 소수점 둘째자리까지 표시 (메타데이터에 number 자료형이 명시된 필드만 포함)
    numeric_columns = []
    
    for col in numeric_columns:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce').round(2)
    
    logging.info("결과:")
    print(result)

if __name__ == "__main__":
    main() 