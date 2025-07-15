# -*- coding: utf-8 -*-
"""
Created on 2025-06-30

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

def get_quotations_price_detail(
    auth: str,  # 사용자권한정보
    excd: str,  # 거래소명
    symb: str,  # 종목코드
    tr_cont: str = "",
    dataframe: Optional[pd.DataFrame] = None,
    depth: int = 0,
    max_depth: int = 10
) -> Optional[pd.DataFrame]:
    """
    [해외주식] 기본시세 
    해외주식 현재가상세[v1_해외주식-029]
    해외주식 현재가상세 API를 호출하여 DataFrame으로 반환합니다.
    
    Args:
        auth (str): 사용자권한정보
        excd (str): 거래소명 (예: HKS, NYS, NAS, AMS, TSE, SHS, SZS, SHI, SZI, HSX, HNX, BAY, BAQ, BAA)
        symb (str): 종목코드
        tr_cont (str): 연속 거래 여부
        dataframe (Optional[pd.DataFrame]): 누적 데이터프레임
        depth (int): 현재 재귀 깊이
        max_depth (int): 최대 재귀 깊이 (기본값: 10)
        
    Returns:
        Optional[pd.DataFrame]: 해외주식 현재가상세 데이터
        
    Example:
        >>> df = get_quotations_price_detail(auth="your_auth_token", excd="NAS", symb="TSLA")
        >>> print(df)
    """
    # [필수 파라미터 검증]
    if not excd:
        logger.error("excd is required. (e.g. 'NAS')")
        raise ValueError("excd is required. (e.g. 'NAS')")
    if not symb:
        logger.error("symb is required. (e.g. 'TSLA')")
        raise ValueError("symb is required. (e.g. 'TSLA')")
    
    # 최대 재귀 깊이 체크
    if depth >= max_depth:
        logger.warning("Maximum recursion depth (%d) reached. Stopping further requests.", max_depth)
        return dataframe if dataframe is not None else pd.DataFrame()
    
    url = "/uapi/overseas-price/v1/quotations/price-detail"
    tr_id = "HHDFS76200200"

    params = {
        "AUTH": auth,
        "EXCD": excd,
        "SYMB": symb,
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
            return get_quotations_price_detail(
                auth,
                excd,
                symb,
                "N", dataframe, depth + 1, max_depth
            )
        else:
            logger.info("Data fetch complete.")
            return dataframe
    else:
        logger.error("API call failed: %s - %s", res.getErrorCode(), res.getErrorMessage())
        res.printError(url)
        return pd.DataFrame()