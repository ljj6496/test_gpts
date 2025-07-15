# -*- coding: utf-8 -*-
"""
Created on 2025-06-17

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import ranking_hts_top_view

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'output1': '응답상세',
    'mrkt_div_cls_code': '시장구분',
    'mksc_shrn_iscd': '종목코드'
}

def main():
    """
    [국내주식] 순위분석
    HTS조회상위20종목[국내주식-214]

    HTS조회상위20종목 테스트 함수
    
    Parameters:

    Returns:
        - DataFrame: HTS조회상위20종목 결과
    
    Example:
        >>> df = get_ranking_hts_top_view()
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

        # HTS조회상위20종목 파라미터 설정
        logger.info("API 파라미터 설정 중...")

        
        # API 호출
        logger.info("API 호출 시작: HTS조회상위20종목")
        result = ranking_hts_top_view.get_ranking_hts_top_view(

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
        logger.info("=== HTS조회상위20종목 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
