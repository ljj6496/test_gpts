# -*- coding: utf-8 -*-
"""
Created on 2025-06-30

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import quotations_inquire_daily_chartprice

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'ovrs_nmix_prdy_vrss': '전일 대비',
    'prdy_vrss_sign': '전일 대비 부호',
    'prdy_ctrt': '전일 대비율',
    'ovrs_nmix_prdy_clpr': '전일 종가',
    'acml_vol': '누적 거래량',
    'hts_kor_isnm': 'HTS 한글 종목명',
    'ovrs_nmix_prpr': '현재가',
    'stck_shrn_iscd': '단축 종목코드',
    'prdy_vol': '전일 거래량',
    'ovrs_prod_oprc': '시가',
    'ovrs_prod_hgpr': '최고가',
    'ovrs_prod_lwpr': '최저가',
    'stck_bsop_date': '영업 일자',
    'ovrs_nmix_prpr': '현재가',
    'ovrs_nmix_oprc': '시가',
    'ovrs_nmix_hgpr': '최고가',
    'ovrs_nmix_lwpr': '최저가',
    'acml_vol': '누적 거래량',
    'mod_yn': '변경 여부'
}

def main():
    """
    [해외주식] 기본시세
    해외주식 종목_지수_환율기간별시세(일_주_월_년)[v1_해외주식-012]

    해외주식 종목_지수_환율기간별시세(일_주_월_년) 테스트 함수
    
    Parameters:
        - fid_cond_mrkt_div_code (str): FID 조건 시장 분류 코드 (N: 해외지수, X 환율, I: 국채, S:금선물)
        - fid_input_iscd (str): FID 입력 종목코드 (종목코드 ※ 해외주식 마스터 코드 참조  (포럼 > FAQ > 종목정보 다운로드(해외) > 해외지수)  ※ 해당 API로 미국주식 조회 시, 다우30, 나스닥100, S&P500 종목만 조회 가능합니다. 더 많은 미국주식 종목 시세를 이용할 시에는, 해외주식기간별시세 API 사용 부탁드립니다.)
        - fid_input_date_1 (str): FID 입력 날짜1 (시작일자(YYYYMMDD))
        - fid_input_date_2 (str): FID 입력 날짜2 (종료일자(YYYYMMDD))
        - fid_period_div_code (str): FID 기간 분류 코드 (D:일, W:주, M:월, Y:년)
        - env_dv (str): 실전모의구분 (real:실전, demo:모의)

    Returns:
        - DataFrame: 해외주식 종목_지수_환율기간별시세(일_주_월_년) 결과
    
    Example:
        >>> df1, df2 = get_quotations_inquire_daily_chartprice(fid_cond_mrkt_div_code="N", fid_input_iscd="DJI", fid_input_date_1="20250101", fid_input_date_2="20250131", fid_period_div_code="D", env_dv="real")  # 실전투자
        >>> df1, df2 = get_quotations_inquire_daily_chartprice(fid_cond_mrkt_div_code="N", fid_input_iscd="DJI", fid_input_date_1="20250101", fid_input_date_2="20250131", fid_period_div_code="D", env_dv="demo")  # 모의투자
    """
    try:
        # pandas 출력 옵션 설정
        pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
        pd.set_option('display.width', None)  # 출력 너비 제한 해제
        pd.set_option('display.max_rows', None)  # 모든 행 표시

        # 실전/모의투자 선택 (모의투자 지원 로직)
        env_dv = "real"  # "real": 실전투자, "demo": 모의투자
        logger.info("투자 환경: %s", "실전투자" if env_dv == "real" else "모의투자")

        # 토큰 발급 (모의투자 지원 로직)
        logger.info("토큰 발급 중...")
        if env_dv == "real":
            ka.auth(svr='prod')  # 실전투자용 토큰
        elif env_dv == "demo":
            ka.auth(svr='vps')   # 모의투자용 토큰
        logger.info("토큰 발급 완료")

        # 해외주식 종목_지수_환율기간별시세(일_주_월_년) 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        fid_cond_mrkt_div_code = "N"  # FID 조건 시장 분류 코드
        fid_input_iscd = "QQQ"  # FID 입력 종목코드
        fid_input_date_1 = "20250101"  # FID 입력 날짜1
        fid_input_date_2 = "20250131"  # FID 입력 날짜2
        fid_period_div_code = "D"  # FID 기간 분류 코드

        
        # API 호출
        logger.info("API 호출 시작: 해외주식 종목_지수_환율기간별시세(일_주_월_년) (%s)", "실전투자" if env_dv == "real" else "모의투자")
        result1, result2 = quotations_inquire_daily_chartprice.get_quotations_inquire_daily_chartprice(
            fid_cond_mrkt_div_code=fid_cond_mrkt_div_code,  # FID 조건 시장 분류 코드
            fid_input_iscd=fid_input_iscd,  # FID 입력 종목코드
            fid_input_date_1=fid_input_date_1,  # FID 입력 날짜1
            fid_input_date_2=fid_input_date_2,  # FID 입력 날짜2
            fid_period_div_code=fid_period_div_code,  # FID 기간 분류 코드
            env_dv=env_dv,  # 실전모의구분
        )
        
        # 결과 확인
        results = [result1, result2]
        if all(result is None or result.empty for result in results):
            logger.warning("조회된 데이터가 없습니다.")
            return
        

        # output1 결과 처리
        logger.info("=== output1 조회 ===")
        if not result1.empty:
            logger.info("사용 가능한 컬럼: %s", result1.columns.tolist())
            
            # 통합 컬럼명 한글 변환 (필요한 컬럼만 자동 매핑됨)
            result1 = result1.rename(columns=COLUMN_MAPPING)
            logger.info("output1 결과:")
            print(result1)
        else:
            logger.info("output1 데이터가 없습니다.")

        # output2 결과 처리
        logger.info("=== output2 조회 ===")
        if not result2.empty:
            logger.info("사용 가능한 컬럼: %s", result2.columns.tolist())
            
            # 통합 컬럼명 한글 변환 (필요한 컬럼만 자동 매핑됨)
            result2 = result2.rename(columns=COLUMN_MAPPING)
            logger.info("output2 결과:")
            print(result2)
        else:
            logger.info("output2 데이터가 없습니다.")

        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
