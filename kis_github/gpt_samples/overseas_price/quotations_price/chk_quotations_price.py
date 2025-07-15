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
import quotations_price

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'rsym': '실시간조회종목코드',
    'zdiv': '소수점자리수',
    'base': '전일종가',
    'pvol': '전일거래량',
    'last': '현재가',
    'sign': '대비기호',
    'diff': '대비',
    'rate': '등락율',
    'tvol': '거래량',
    'tamt': '거래대금',
    'ordy': '매수가능여부'
}

def main():
    """
    [해외주식] 기본시세
    해외주식 현재체결가[v1_해외주식-009]

    해외주식 현재체결가 테스트 함수
    
    Parameters:
        - auth (str): 사용자권한정보 ("" (Null 값 설정))
        - excd (str): 거래소코드 (HKS : 홍콩 NYS : 뉴욕 NAS : 나스닥 AMS : 아멕스 TSE : 도쿄 SHS : 상해 SZS : 심천 SHI : 상해지수 SZI : 심천지수 HSX : 호치민 HNX : 하노이 BAY : 뉴욕(주간) BAQ : 나스닥(주간) BAA : 아멕스(주간))
        - symb (str): 종목코드 ()
        - env_dv (str): 실전모의구분 (real:실전, demo:모의)

    Returns:
        - DataFrame: 해외주식 현재체결가 결과
    
    Example:
        >>> df = get_quotations_price(auth="", excd="NYS", symb="", env_dv="real")  # 실전투자
        >>> df = get_quotations_price(auth="", excd="NYS", symb="", env_dv="demo")  # 모의투자
    """
    try:
        # pandas 출력 옵션 설정
        pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
        pd.set_option('display.width', None)  # 출력 너비 제한 해제
        pd.set_option('display.max_rows', None)  # 모든 행 표시

        # 실전/모의투자 선택 (모의투자 지원 로직)
        env_dv = "demo"  # "real": 실전투자, "demo": 모의투자
        logger.info("투자 환경: %s", "실전투자" if env_dv == "real" else "모의투자")

        # 토큰 발급 (모의투자 지원 로직)
        logger.info("토큰 발급 중...")
        if env_dv == "real":
            ka.auth(svr='prod')  # 실전투자용 토큰
        elif env_dv == "demo":
            ka.auth(svr='vps')   # 모의투자용 토큰
        logger.info("토큰 발급 완료")

        # 해외주식 현재체결가 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        auth = ""  # 사용자권한정보
        excd = "NAS"  # 거래소코드
        symb = "TSLA"  # 종목코드

        # API 호출
        logger.info("API 호출 시작: 해외주식 현재체결가 (%s)", "실전투자" if env_dv == "real" else "모의투자")
        result = quotations_price.get_quotations_price(
            auth=auth,  # 사용자권한정보
            excd=excd,  # 거래소코드
            symb=symb,  # 종목코드
            env_dv=env_dv,  # 실전모의구분
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
        logger.info("=== 해외주식 현재체결가 결과 (%s) ===", "실전투자" if env_dv == "real" else "모의투자")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
