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

def get_trading_inquire_nccs(
    cano: str,  # 종합계좌번호
    acnt_prdt_cd: str,  # 계좌상품코드
    ovrs_excg_cd: str,  # 해외거래소코드
    sort_sqn: str,  # 정렬순서
    ctx_area_fk200: str,  # 연속조회검색조건200
    ctx_area_nk200: str,  # 연속조회키200
    tr_cont: str = "",
    dataframe: Optional[pd.DataFrame] = None,
    depth: int = 0,
    max_depth: int = 10
) -> Optional[pd.DataFrame]:
    """
    [해외주식] 주문/계좌 
    해외주식 미체결내역[v1_해외주식-005]
    해외주식 미체결내역 API를 호출하여 DataFrame으로 반환합니다.
    
    Args:
        cano (str): 계좌번호 체계(8-2)의 앞 8자리
        acnt_prdt_cd (str): 계좌번호 체계(8-2)의 뒤 2자리
        ovrs_excg_cd (str): NASD : 나스닥 NYSE : 뉴욕  AMEX : 아멕스 SEHK : 홍콩 SHAA : 중국상해 SZAA : 중국심천 TKSE : 일본 HASE : 베트남 하노이 VNSE : 베트남 호치민  * NASD 인 경우만 미국전체로 조회되며 나머지 거래소 코드는 해당 거래소만 조회됨 * 공백 입력 시 다음조회가 불가능하므로, 반드시 거래소코드 입력해야 함
        sort_sqn (str): DS : 정순 그외 : 역순  [header tr_id: TTTS3018R] ""(공란)
        ctx_area_fk200 (str): 공란 : 최초 조회시 이전 조회 Output CTX_AREA_FK200값 : 다음페이지 조회시(2번째부터)
        ctx_area_nk200 (str): 공란 : 최초 조회시 이전 조회 Output CTX_AREA_NK200값 : 다음페이지 조회시(2번째부터)
        tr_cont (str): 연속 거래 여부
        dataframe (Optional[pd.DataFrame]): 누적 데이터프레임
        depth (int): 현재 재귀 깊이
        max_depth (int): 최대 재귀 깊이 (기본값: 10)
        
    Returns:
        Optional[pd.DataFrame]: 해외주식 미체결내역 데이터
        
    Example:
        >>> df = get_trading_inquire_nccs(
        ...     cano="810XXXXX",
        ...     acnt_prdt_cd="01",
        ...     ovrs_excg_cd="NYSE",
        ...     sort_sqn="DS",
        ...     ctx_area_fk200="",
        ...     ctx_area_nk200=""
        ... )
        >>> print(df)
    """
    # [필수 파라미터 검증]
    if not cano:
        logger.error("cano is required. (e.g. '810XXXXX')")
        raise ValueError("cano is required. (e.g. '810XXXXX')")
    if not acnt_prdt_cd:
        logger.error("acnt_prdt_cd is required. (e.g. '01')")
        raise ValueError("acnt_prdt_cd is required. (e.g. '01')")
    if not ovrs_excg_cd:
        logger.error("ovrs_excg_cd is required. (e.g. 'NYSE')")
        raise ValueError("ovrs_excg_cd is required. (e.g. 'NYSE')")
    if not sort_sqn:
        logger.error("sort_sqn is required. (e.g. 'DS')")
        raise ValueError("sort_sqn is required. (e.g. 'DS')")

    # 최대 재귀 깊이 체크
    if depth >= max_depth:
        logger.warning("Maximum recursion depth (%d) reached. Stopping further requests.", max_depth)
        return dataframe if dataframe is not None else pd.DataFrame()
    
    url = "/uapi/overseas-stock/v1/trading/inquire-nccs"
    tr_id = "TTTS3018R"

    params = {
        "CANO": cano,
        "ACNT_PRDT_CD": acnt_prdt_cd,
        "OVRS_EXCG_CD": ovrs_excg_cd,
        "SORT_SQN": sort_sqn,
        "CTX_AREA_FK200": ctx_area_fk200,
        "CTX_AREA_NK200": ctx_area_nk200,
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
            return get_trading_inquire_nccs(
                cano,
                acnt_prdt_cd,
                ovrs_excg_cd,
                sort_sqn,
                ctx_area_fk200,
                ctx_area_nk200,
                "N", dataframe, depth + 1, max_depth
            )
        else:
            logger.info("Data fetch complete.")
            return dataframe
    else:
        logger.error("API call failed: %s - %s", res.getErrorCode(), res.getErrorMessage())
        res.printError(url)
        return pd.DataFrame()