# -*- coding: utf-8 -*-
"""
Created on 2025-07-01

@author: LaivData jjlee with cursor
"""

import logging
import kis_auth as kis
import pandas as pd
import time
from typing import Optional

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_trading_inquire_psamount(
    cano: str,  # 종합계좌번호
    acnt_prdt_cd: str,  # 계좌상품코드
    ovrs_futr_fx_pdno: str,  # 해외선물FX상품번호
    sll_buy_dvsn_cd: str,  # 매도매수구분코드
    fm_ord_pric: str,  # FM주문가격
    ecis_rsvn_ord_yn: str,  # 행사예약주문여부
    tr_cont: str = "",
    dataframe: Optional[pd.DataFrame] = None,
    depth: int = 0,
    max_depth: int = 10
) -> Optional[pd.DataFrame]:
    """
    [해외선물옵션] 주문/계좌 
    해외선물옵션 주문가능조회[v1_해외선물-006]
    해외선물옵션 주문가능조회 API를 호출하여 DataFrame으로 반환합니다.
    
    Args:
        cano (str): 계좌번호 체계(8-2)의 앞 8자리
        acnt_prdt_cd (str): 계좌번호 체계(8-2)의 뒤 2자리
        ovrs_futr_fx_pdno (str): 해외선물FX상품번호
        sll_buy_dvsn_cd (str): 01 : 매도 / 02 : 매수
        fm_ord_pric (str): FM주문가격
        ecis_rsvn_ord_yn (str): 행사예약주문여부
        tr_cont (str): 연속 거래 여부
        dataframe (Optional[pd.DataFrame]): 누적 데이터프레임
        depth (int): 현재 재귀 깊이
        max_depth (int): 최대 재귀 깊이 (기본값: 10)
        
    Returns:
        Optional[pd.DataFrame]: 해외선물옵션 주문가능조회 데이터
        
    Example:
        >>> df = get_trading_inquire_psamount(
        ...     cano="80012345",
        ...     acnt_prdt_cd="08",
        ...     ovrs_futr_fx_pdno="6AU22",
        ...     sll_buy_dvsn_cd="02",
        ...     fm_ord_pric="",
        ...     ecis_rsvn_ord_yn=""
        ... )
        >>> print(df)
    """
    # [필수 파라미터 검증]
    if not cano:
        logger.error("cano is required. (e.g. '80012345')")
        raise ValueError("cano is required. (e.g. '80012345')")
    if not acnt_prdt_cd:
        logger.error("acnt_prdt_cd is required. (e.g. '08')")
        raise ValueError("acnt_prdt_cd is required. (e.g. '08')")
    if not ovrs_futr_fx_pdno:
        logger.error("ovrs_futr_fx_pdno is required. (e.g. '6AU22')")
        raise ValueError("ovrs_futr_fx_pdno is required. (e.g. '6AU22')")
    if sll_buy_dvsn_cd not in ["01", "02"]:
        logger.error("sll_buy_dvsn_cd is required. (e.g. '01' or '02')")
        raise ValueError("sll_buy_dvsn_cd is required. (e.g. '01' or '02')")

    
    # 최대 재귀 깊이 체크
    if depth >= max_depth:
        logger.warning("Maximum recursion depth (%d) reached. Stopping further requests.", max_depth)
        return dataframe if dataframe is not None else pd.DataFrame()
    
    url = "/uapi/overseas-futureoption/v1/trading/inquire-psamount"
    tr_id = "OTFM3304R"

    params = {
        "CANO": cano,
        "ACNT_PRDT_CD": acnt_prdt_cd,
        "OVRS_FUTR_FX_PDNO": ovrs_futr_fx_pdno,
        "SLL_BUY_DVSN_CD": sll_buy_dvsn_cd,
        "FM_ORD_PRIC": fm_ord_pric,
        "ECIS_RSVN_ORD_YN": ecis_rsvn_ord_yn,
    }

    res = kis._url_fetch(url, tr_id, tr_cont, params)

    if res.isOK():
        if hasattr(res.getBody(), 'output'):
            output_data = res.getBody().output
            if not isinstance(output_data, list):
                output_data = [output_data]
            current_data = pd.DataFrame(output_data)
        else:
            current_data = pd.DataFrame()
            
        if dataframe is not None:
            dataframe = pd.concat([dataframe, current_data], ignore_index=True)
        else:
            dataframe = current_data
            
        tr_cont = res.getHeader().tr_cont
        
        if tr_cont == "M":
            logger.info("Calling next page...")
            time.sleep(0.1)
            return get_trading_inquire_psamount(
                cano,
                acnt_prdt_cd,
                ovrs_futr_fx_pdno,
                sll_buy_dvsn_cd,
                fm_ord_pric,
                ecis_rsvn_ord_yn,
                dataframe, "N", depth + 1, max_depth
            )
        else:
            logger.info("Data fetch complete.")
            return dataframe
    else:
        logger.error("API call failed: %s - %s", res.getErrorCode(), res.getErrorMessage())
        res.printError(url)
        return pd.DataFrame()