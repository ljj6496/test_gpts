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

# 로깅 설정
logging.basicConfig(level=logging.INFO)

##############################################################################################
# [국내선물옵션] 주문/계좌 > 선물옵션 총자산현황[v1_국내선물-014]
##############################################################################################

# 상수 정의
API_URL = "/uapi/domestic-futureoption/v1/trading/inquire-deposit"

def get_trading_inquire_deposit(
    cano: str,  # [필수] 종합계좌번호
    acnt_prdt_cd: str  # [필수] 계좌상품코드 (ex. 03)
) -> pd.DataFrame:
    """
    선물옵션 총자산현황 API 입니다.
    
    Args:
        cano (str): [필수] 종합계좌번호
        acnt_prdt_cd (str): [필수] 계좌상품코드 (ex. 03)

    Returns:
        pd.DataFrame: 선물옵션 총자산현황 데이터
        
    Example:
        >>> df = get_trading_inquire_deposit(cano="81180744", acnt_prdt_cd="03")
        >>> print(df)
    """

    if cano == "":
        raise ValueError("cano is required")
    
    if acnt_prdt_cd == "":
        raise ValueError("acnt_prdt_cd is required")

    tr_id = "CTRP6550R"  # 선물옵션 총자산현황

    params = {
        "CANO": cano,  # 종합계좌번호
        "ACNT_PRDT_CD": acnt_prdt_cd  # 계좌상품코드
    }
    
    res = kis._url_fetch(API_URL, tr_id, "", params)
    
    if res.isOK():
        current_data = pd.DataFrame([res.getBody().output])
        logging.info("Data fetch complete.")
        return current_data
    else:
        res.printError(url=API_URL)
        return pd.DataFrame() 