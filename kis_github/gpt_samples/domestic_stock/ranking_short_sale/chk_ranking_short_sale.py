# -*- coding: utf-8 -*-
"""
Created on 2025-06-16

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import ranking_short_sale

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'mksc_shrn_iscd': '유가증권 단축 종목코드',
    'hts_kor_isnm': 'HTS 한글 종목명',
    'stck_prpr': '주식 현재가',
    'prdy_vrss': '전일 대비',
    'prdy_vrss_sign': '전일 대비 부호',
    'prdy_ctrt': '전일 대비율',
    'acml_vol': '누적 거래량',
    'acml_tr_pbmn': '누적 거래 대금',
    'ssts_cntg_qty': '공매도 체결 수량',
    'ssts_vol_rlim': '공매도 거래량 비중',
    'ssts_tr_pbmn': '공매도 거래 대금',
    'ssts_tr_pbmn_rlim': '공매도 거래대금 비중',
    'stnd_date1': '기준 일자1',
    'stnd_date2': '기준 일자2',
    'avrg_prc': '평균가격'
}

def main():
    """
    [국내주식] 순위분석
    국내주식 공매도 상위종목[국내주식-133]

    국내주식 공매도 상위종목 테스트 함수
    
    Parameters:
        - fid_aply_rang_vol (str): FID 적용 범위 거래량 (공백)
        - fid_cond_mrkt_div_code (str): 조건 시장 분류 코드 (시장구분코드 (주식 J))
        - fid_cond_scr_div_code (str): 조건 화면 분류 코드 (Unique key(20482))
        - fid_input_iscd (str): 입력 종목코드 (0000:전체, 0001:코스피, 1001:코스닥, 2001:코스피200, 4001: KRX100, 3003: 코스닥150)
        - fid_period_div_code (str): 조회구분 (일/월) (조회구분 (일/월) D: 일, M:월)
        - fid_input_cnt_1 (str): 조회가간(일수 ('조회가간(일수): 조회구분(D) 0:1일, 1:2일, 2:3일, 3:4일, 4:1주일, 9:2주일, 14:3주일,  조회구분(M) 1:1개월,  2:2개월, 3:3개월')
        - fid_trgt_exls_cls_code (str): 대상 제외 구분 코드 (공백)
        - fid_trgt_cls_code (str): FID 대상 구분 코드 (공백)
        - fid_aply_rang_prc_1 (str): FID 적용 범위 가격1 (가격 ~)
        - fid_aply_rang_prc_2 (str): FID 적용 범위 가격2 (~ 가격)
    Returns:
        - DataFrame: 국내주식 공매도 상위종목 결과
    
    Example:
        >>> df = get_ranking_short_sale(fid_aply_rang_vol="", fid_cond_mrkt_div_code="J", fid_cond_scr_div_code="20482", fid_input_iscd="0000", fid_period_div_code="D", fid_input_cnt_1="0", fid_trgt_exls_cls_code="", fid_trgt_cls_code="", fid_aply_rang_prc_1="0", fid_aply_rang_prc_2="1000000")
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

        # 국내주식 공매도 상위종목 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        fid_aply_rang_vol = ""  # FID 적용 범위 거래량
        fid_cond_mrkt_div_code = "J"  # 조건 시장 분류 코드
        fid_cond_scr_div_code = "20482"  # 조건 화면 분류 코드
        fid_input_iscd = "0000"  # 입력 종목코드
        fid_period_div_code = "D"  # 조회구분 (일/월)
        fid_input_cnt_1 = "0"  # 조회가간(일수
        fid_trgt_exls_cls_code = ""  # 대상 제외 구분 코드
        fid_trgt_cls_code = ""  # FID 대상 구분 코드
        fid_aply_rang_prc_1 = "0"  # FID 적용 범위 가격1
        fid_aply_rang_prc_2 = "1000000"  # FID 적용 범위 가격2
        
        # API 호출
        logger.info("API 호출 시작: 국내주식 공매도 상위종목")
        result = ranking_short_sale.get_ranking_short_sale(
            fid_aply_rang_vol=fid_aply_rang_vol,  # FID 적용 범위 거래량
            fid_cond_mrkt_div_code=fid_cond_mrkt_div_code,  # 조건 시장 분류 코드
            fid_cond_scr_div_code=fid_cond_scr_div_code,  # 조건 화면 분류 코드
            fid_input_iscd=fid_input_iscd,  # 입력 종목코드
            fid_period_div_code=fid_period_div_code,  # 조회구분 (일/월)
            fid_input_cnt_1=fid_input_cnt_1,  # 조회가간(일수
            fid_trgt_exls_cls_code=fid_trgt_exls_cls_code,  # 대상 제외 구분 코드
            fid_trgt_cls_code=fid_trgt_cls_code,  # FID 대상 구분 코드
            fid_aply_rang_prc_1=fid_aply_rang_prc_1,  # FID 적용 범위 가격1
            fid_aply_rang_prc_2=fid_aply_rang_prc_2,  # FID 적용 범위 가격2
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
        logger.info("=== 국내주식 공매도 상위종목 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
