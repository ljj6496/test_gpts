# -*- coding: utf-8 -*-
"""
Created on 2025-06-19

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import quotations_udrl_asset_list

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'unas_shrn_iscd': '기초자산단축종목코드',
    'unas_isnm': '기초자산종목명',
    'unas_prpr': '기초자산현재가',
    'unas_prdy_vrss': '기초자산전일대비',
    'unas_prdy_vrss_sign': '기초자산전일대비부호',
    'unas_prdy_ctrt': '기초자산전일대비율'
}

def main():
    """
    [국내주식] ELW시세
    ELW 기초자산 목록조회[국내주식-185]

    ELW 기초자산 목록조회 테스트 함수
    
    Parameters:
        - fid_cond_scr_div_code (str): 조건화면분류코드 (11541(Primary key))
        - fid_rank_sort_cls_code (str): 순위정렬구분코드 (0(종목명순), 1(콜발행종목순), 2(풋발행종목순), 3(전일대비 상승율순), 4(전일대비 하락율순), 5(현재가 크기순), 6(종목코드순))
        - fid_input_iscd (str): 입력종목코드 (00000(전체), 00003(한국투자증권), 00017(KB증권), 00005(미래에셋))
    Returns:
        - DataFrame: ELW 기초자산 목록조회 결과
    
    Example:
        >>> df = get_quotations_udrl_asset_list(fid_cond_scr_div_code="11541", fid_rank_sort_cls_code="0", fid_input_iscd="00000")
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

        # ELW 기초자산 목록조회 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        fid_cond_scr_div_code = "11541"  # 조건화면분류코드
        fid_rank_sort_cls_code = "0"  # 순위정렬구분코드
        fid_input_iscd = "00000"  # 입력종목코드
        
        # API 호출
        logger.info("API 호출 시작: ELW 기초자산 목록조회")
        result = quotations_udrl_asset_list.get_quotations_udrl_asset_list(
            fid_cond_scr_div_code=fid_cond_scr_div_code,  # 조건화면분류코드
            fid_rank_sort_cls_code=fid_rank_sort_cls_code,  # 순위정렬구분코드
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
        logger.info("=== ELW 기초자산 목록조회 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
