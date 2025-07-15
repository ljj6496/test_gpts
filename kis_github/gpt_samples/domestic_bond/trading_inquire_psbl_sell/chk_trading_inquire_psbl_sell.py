# -*- coding: utf-8 -*-
"""
Created on 2025-06-20

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import trading_inquire_psbl_sell

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'pdno': '상품번호',
    'buy_qty': '매수수량',
    'sll_qty': '매도수량',
    'cblc_qty': '잔고수량',
    'nsvg_qty': '비저축수량',
    'ord_psbl_qty': '주문가능수량',
    'pchs_avg_pric': '매입평균가격',
    'pchs_amt': '매입금액',
    'now_pric': '현재가',
    'evlu_amt': '평가금액',
    'evlu_pfls_amt': '평가손익금액',
    'evlu_pfls_rt': '평가손익율'
}

def main():
    """
    [국내주식] 주문/계좌
    매도가능수량조회[국내주식-165]

    매도가능수량조회 테스트 함수
    
    Parameters:
        - cano (str): 종합계좌번호 (종합계좌번호)
        - acnt_prdt_cd (str): 계좌상품코드 (계좌상품코드)
        - pdno (str): 종목번호 (보유종목 코드 ex)000660)
    Returns:
        - DataFrame: 매도가능수량조회 결과
    
    Example:
        >>> df = get_trading_inquire_psbl_sell(cano="12345678", acnt_prdt_cd="01", pdno="000660")
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

        # kis_auth 모듈에서 계좌 정보 가져오기
        trenv = ka.getTREnv()

        # 매도가능수량조회 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        cano = trenv.my_acct # 종합계좌번호
        acnt_prdt_cd = "01"  # 계좌상품코드
        pdno = "005930"  # 종목번호
        
        # API 호출
        logger.info("API 호출 시작: 매도가능수량조회")
        result = trading_inquire_psbl_sell.get_trading_inquire_psbl_sell(
            cano=cano,  # 종합계좌번호
            acnt_prdt_cd=acnt_prdt_cd,  # 계좌상품코드
            pdno=pdno,  # 종목번호
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
        logger.info("=== 매도가능수량조회 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
