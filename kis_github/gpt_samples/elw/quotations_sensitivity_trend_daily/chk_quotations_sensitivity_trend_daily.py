# -*- coding: utf-8 -*-
"""
Created on 2025-06-18

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import quotations_sensitivity_trend_daily

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'stck_bsop_date': '주식영업일자',
    'elw_prpr': 'ELW현재가',
    'prdy_vrss': '전일대비',
    'prdy_vrss_sign': '전일대비부호',
    'prdy_ctrt': '전일대비율',
    'hts_thpr': 'HTS이론가',
    'delta_val': '델타값',
    'gama': '감마',
    'theta': '세타',
    'vega': '베가',
    'rho': '로우'
}

def main():
    """
    [국내주식] ELW시세
    ELW 민감도 추이(일별)[국내주식-176]

    ELW 민감도 추이(일별) 테스트 함수
    
    Parameters:
        - fid_cond_mrkt_div_code (str): 조건시장분류코드 (시장구분코드 (W))
        - fid_input_iscd (str): 입력종목코드 (ex)(58J438(KBJ438삼성전자풋))
    Returns:
        - DataFrame: ELW 민감도 추이(일별) 결과
    
    Example:
        >>> df = get_quotations_sensitivity_trend_daily(fid_cond_mrkt_div_code="W", fid_input_iscd="58J438")
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

        # ELW 민감도 추이(일별) 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        fid_cond_mrkt_div_code = "W"  # 조건시장분류코드
        fid_input_iscd = "58J438"  # 입력종목코드
        
        # API 호출
        logger.info("API 호출 시작: ELW 민감도 추이(일별)")
        result = quotations_sensitivity_trend_daily.get_quotations_sensitivity_trend_daily(
            fid_cond_mrkt_div_code=fid_cond_mrkt_div_code,  # 조건시장분류코드
            fid_input_iscd=fid_input_iscd,  # 입력종목코드
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
        logger.info("=== ELW 민감도 추이(일별) 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
