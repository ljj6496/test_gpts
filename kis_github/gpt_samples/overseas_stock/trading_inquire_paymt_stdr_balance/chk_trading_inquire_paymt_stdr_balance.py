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
import trading_inquire_paymt_stdr_balance

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'pdno': '상품번호',
    'prdt_name': '상품명',
    'cblc_qty13': '잔고수량13',
    'ord_psbl_qty1': '주문가능수량1',
    'avg_unpr3': '평균단가3',
    'ovrs_now_pric1': '해외현재가격1',
    'frcr_pchs_amt': '외화매입금액',
    'frcr_evlu_amt2': '외화평가금액2',
    'evlu_pfls_amt2': '평가손익금액2',
    'bass_exrt': '기준환율',
    'oprt_dtl_dtime': '조작상세일시',
    'buy_crcy_cd': '매수통화코드',
    'thdt_sll_ccld_qty1': '당일매도체결수량1',
    'thdt_buy_ccld_qty1': '당일매수체결수량1',
    'evlu_pfls_rt1': '평가손익율1',
    'tr_mket_name': '거래시장명',
    'natn_kor_name': '국가한글명',
    'std_pdno': '표준상품번호',
    'mgge_qty': '담보수량',
    'loan_rmnd': '대출잔액',
    'prdt_type_cd': '상품유형코드',
    'ovrs_excg_cd': '해외거래소코드',
    'scts_dvsn_name': '유가증권구분명',
    'ldng_cblc_qty': '대여잔고수량',
    'crcy_cd': '통화코드',
    'crcy_cd_name': '통화코드명',
    'frcr_dncl_amt_2': '외화예수금액2',
    'frst_bltn_exrt': '최초고시환율',
    'frcr_evlu_amt2': '외화평가금액2',
    'pchs_amt_smtl_amt': '매입금액합계금액',
    'tot_evlu_pfls_amt': '총평가손익금액',
    'evlu_erng_rt1': '평가수익율1',
    'tot_dncl_amt': '총예수금액',
    'wcrc_evlu_amt_smtl': '원화평가금액합계',
    'tot_asst_amt2': '총자산금액2',
    'frcr_cblc_wcrc_evlu_amt_smtl': '외화잔고원화평가금액합계',
    'tot_loan_amt': '총대출금액',
    'tot_ldng_evlu_amt': '총대여평가금액'
}

def main():
    """
    [해외주식] 주문/계좌
    해외주식 결제기준잔고[해외주식-064]

    해외주식 결제기준잔고 테스트 함수
    
    Parameters:
        - cano (str): 종합계좌번호 ()
        - acnt_prdt_cd (str): 계좌상품코드 ()
        - bass_dt (str): 기준일자 ()
        - wcrc_frcr_dvsn_cd (str): 원화외화구분코드 (01(원화기준),02(외화기준))
        - inqr_dvsn_cd (str): 조회구분코드 (00(전체), 01(일반), 02(미니스탁))

    Returns:
        - DataFrame: 해외주식 결제기준잔고 결과
    
    Example:
        >>> df1, df2, df3 = get_trading_inquire_paymt_stdr_balance(cano=trenv.my_acct, acnt_prdt_cd="01", bass_dt="20250630", wcrc_frcr_dvsn_cd="01", inqr_dvsn_cd="00")
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

        # 해외주식 결제기준잔고 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        cano = trenv.my_acct  # 계좌번호 (자동 설정)
        acnt_prdt_cd = "01"  # 계좌상품코드
        bass_dt = "20250630"  # 기준일자
        wcrc_frcr_dvsn_cd = "01"  # 원화외화구분코드
        inqr_dvsn_cd = "00"  # 조회구분코드

        
        # API 호출
        logger.info("API 호출 시작: 해외주식 결제기준잔고")
        result1, result2, result3 = trading_inquire_paymt_stdr_balance.get_trading_inquire_paymt_stdr_balance(
            cano=cano,  # 종합계좌번호
            acnt_prdt_cd=acnt_prdt_cd,  # 계좌상품코드
            bass_dt=bass_dt,  # 기준일자
            wcrc_frcr_dvsn_cd=wcrc_frcr_dvsn_cd,  # 원화외화구분코드
            inqr_dvsn_cd=inqr_dvsn_cd,  # 조회구분코드
        )
        
        # 결과 확인
        results = [result1, result2, result3]
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

        # output3 결과 처리
        logger.info("=== output3 조회 ===")
        if not result3.empty:
            logger.info("사용 가능한 컬럼: %s", result3.columns.tolist())
            
            # 통합 컬럼명 한글 변환 (필요한 컬럼만 자동 매핑됨)
            result3 = result3.rename(columns=COLUMN_MAPPING)
            logger.info("output3 결과:")
            print(result3)
        else:
            logger.info("output3 데이터가 없습니다.")

        
    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        raise

if __name__ == "__main__":
    main()
