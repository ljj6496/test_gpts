# -*- coding: utf-8 -*-
"""
Created on 2025-07-01

@author: LaivData jjlee with cursor
"""

import sys
sys.path.extend(['../..', '.'])  # kis_auth 파일 경로 추가

import logging
import pandas as pd
import kis_auth as ka
import trading_inquire_psamount

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'cano': '종합계좌번호',
    'acnt_prdt_cd': '계좌상품코드',
    'ovrs_futr_fx_pdno': '해외선물FX상품번호',
    'crcy_cd': '통화코드',
    'sll_buy_dvsn_cd': '매도매수구분코드',
    'fm_ustl_qty': 'FM미결제수량',
    'fm_lqd_psbl_qty': 'FM청산가능수량',
    'fm_new_ord_psbl_qty': 'FM신규주문가능수량',
    'fm_tot_ord_psbl_qty': 'FM총주문가능수량',
    'fm_mkpr_tot_ord_psbl_qty': 'FM시장가총주문가능수량'
}

def main():
    """
    [해외선물옵션] 주문/계좌
    해외선물옵션 주문가능조회[v1_해외선물-006]

    해외선물옵션 주문가능조회 테스트 함수
    
    Parameters:
        - cano (str): 종합계좌번호 (계좌번호 체계(8-2)의 앞 8자리)
        - acnt_prdt_cd (str): 계좌상품코드 (계좌번호 체계(8-2)의 뒤 2자리)
        - ovrs_futr_fx_pdno (str): 해외선물FX상품번호 ()
        - sll_buy_dvsn_cd (str): 매도매수구분코드 (01 : 매도 / 02 : 매수)
        - fm_ord_pric (str): FM주문가격 (N)
        - ecis_rsvn_ord_yn (str): 행사예약주문여부 (N)

    Returns:
        - DataFrame: 해외선물옵션 주문가능조회 결과
    
    Example:
        >>> df = get_trading_inquire_psamount(cano=trenv.my_acct, acnt_prdt_cd="08", ovrs_futr_fx_pdno="6AU22", sll_buy_dvsn_cd="02", fm_ord_pric="", ecis_rsvn_ord_yn="")
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
        trenv = ka.getTREnv()

        # 해외선물옵션 주문가능조회 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        cano = trenv.my_acct  # 계좌번호 (자동 설정)
        acnt_prdt_cd = "08"  # 계좌상품코드
        ovrs_futr_fx_pdno = "6AU22"  # 해외선물FX상품번호
        sll_buy_dvsn_cd = "02"  # 매도매수구분코드
        fm_ord_pric = ""  # FM주문가격
        ecis_rsvn_ord_yn = ""  # 행사예약주문여부

        
        # API 호출
        logger.info("API 호출 시작: 해외선물옵션 주문가능조회")
        result = trading_inquire_psamount.get_trading_inquire_psamount(
            cano=cano,  # 종합계좌번호
            acnt_prdt_cd=acnt_prdt_cd,  # 계좌상품코드
            ovrs_futr_fx_pdno=ovrs_futr_fx_pdno,  # 해외선물FX상품번호
            sll_buy_dvsn_cd=sll_buy_dvsn_cd,  # 매도매수구분코드
            fm_ord_pric=fm_ord_pric,  # FM주문가격
            ecis_rsvn_ord_yn=ecis_rsvn_ord_yn,  # 행사예약주문여부
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
        logger.info("=== 해외선물옵션 주문가능조회 결과 ===")
        logger.info("조회된 데이터 건수: %d", len(result))
        print(result)
        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
