# -*- coding: utf-8 -*-
"""
Created on 2025-06-26

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import quotations_countries_holiday

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'prdt_type_cd': '상품유형코드',
    'tr_natn_cd': '거래국가코드',
    'natn_eng_abrv_cd': '국가영문약어코드',
    'tr_mket_cd': '거래시장코드',
    'tr_mket_name': '거래시장명',
    'acpl_sttl_dt': '현지결제일자',
    'dmst_sttl_dt': '국내결제일자'
}

def main():
    """
    [해외주식] 기본시세
    해외결제일자조회[해외주식-017]

    해외결제일자조회 테스트 함수
    
    Parameters:
        - trad_dt (str): 기준일자 (기준일자(YYYYMMDD))
        - ctx_area_nk (str): 연속조회키 (공백으로 입력)
        - ctx_area_fk (str): 연속조회검색조건 (공백으로 입력)

    Returns:
        - DataFrame: 해외결제일자조회 결과
    
    Example:
        >>> df = get_quotations_countries_holiday(trad_dt="20250101", ctx_area_nk="", ctx_area_fk="")
    """
    try:
        # pandas 출력 옵션 설정
        pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
        pd.set_option('display.width', None)  # 출력 너비 제한 해제
        pd.set_option('display.max_rows', None)  # 모든 행 표시

        # 토큰 발급
        logger.info("토큰 발급 중...")
        ka.auth()
        logger.info("토큰 발급 완료")

        # 해외결제일자조회 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        trad_dt = "20230512"  # 기준일자
        ctx_area_nk = ""  # 연속조회키
        ctx_area_fk = ""  # 연속조회검색조건

        
        # API 호출
        logger.info("API 호출 시작: 해외결제일자조회")
        result = quotations_countries_holiday.get_quotations_countries_holiday(
            trad_dt=trad_dt,  # 기준일자
            ctx_area_nk=ctx_area_nk,  # 연속조회키
            ctx_area_fk=ctx_area_fk,  # 연속조회검색조건
        )
        
        if result is None or result.empty:
            logger.warning("조회된 데이터가 없습니다.")
            return
        
        # 컬럼명 출력
        logger.info("사용 가능한 컬럼 목록:")
        logger.info(result.columns.tolist())

        # 한글 컬럼명으로 변환
        result = result.rename(columns=COLUMN_MAPPING)
        
        # 결과 출력
        logger.info("=== 해외결제일자조회 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
