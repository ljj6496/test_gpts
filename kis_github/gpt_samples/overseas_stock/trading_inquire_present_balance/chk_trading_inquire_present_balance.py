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
import trading_inquire_present_balance

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMN_MAPPING = {
    'cblc_qty13': '잔고수량13',
    'thdt_buy_ccld_qty1': '당일매수체결수량1',
    'thdt_sll_ccld_qty1': '당일매도체결수량1',
    'ccld_qty_smtl1': '체결수량합계1',
    'ord_psbl_qty1': '주문가능수량1',
    'frcr_pchs_amt': '외화매입금액',
    'frcr_evlu_amt2': '외화평가금액2',
    'evlu_pfls_amt2': '평가손익금액2',
    'evlu_pfls_rt1': '평가손익율1',
    'pdno': '상품번호',
    'bass_exrt': '기준환율',
    'buy_crcy_cd': '매수통화코드',
    'ovrs_now_pric1': '해외현재가격1',
    'avg_unpr3': '평균단가3',
    'tr_mket_name': '거래시장명',
    'natn_kor_name': '국가한글명',
    'pchs_rmnd_wcrc_amt': '매입잔액원화금액',
    'thdt_buy_ccld_frcr_amt': '당일매수체결외화금액',
    'thdt_sll_ccld_frcr_amt': '당일매도체결외화금액',
    'unit_amt': '단위금액',
    'std_pdno': '표준상품번호',
    'prdt_type_cd': '상품유형코드',
    'loan_rmnd': '대출잔액',
    'loan_dt': '대출일자',
    'loan_expd_dt': '대출만기일자',
    'ovrs_excg_cd': '해외거래소코드',
    'item_lnkg_excg_cd': '종목연동거래소코드',
    'crcy_cd': '통화코드',
    'frcr_buy_amt_smtl': '외화매수금액합계',
    'frcr_sll_amt_smtl': '외화매도금액합계',
    'frcr_dncl_amt_2': '외화예수금액2',
    'frst_bltn_exrt': '최초고시환율',
    'frcr_buy_mgn_amt': '외화매수증거금액',
    'frcr_etc_mgna': '외화기타증거금',
    'frcr_drwg_psbl_amt_1': '외화출금가능금액1',
    'frcr_evlu_amt2': '출금가능원화금액',
    'acpl_cstd_crcy_yn': '현지보관통화여부',
    'nxdy_frcr_drwg_psbl_amt': '익일외화출금가능금액',
    'output3': '응답상세3',
    'pchs_amt_smtl': '매입금액합계',
    'evlu_amt_smtl': '평가금액합계',
    'evlu_pfls_amt_smtl': '평가손익금액합계',
    'dncl_amt': '예수금액',
    'cma_evlu_amt': 'CMA평가금액',
    'tot_dncl_amt': '총예수금액',
    'etc_mgna': '기타증거금',
    'wdrw_psbl_tot_amt': '인출가능총금액',
    'frcr_evlu_tota': '외화평가총액',
    'evlu_erng_rt1': '평가수익율1',
    'pchs_amt_smtl_amt': '매입금액합계금액',
    'evlu_amt_smtl_amt': '평가금액합계금액',
    'tot_evlu_pfls_amt': '총평가손익금액',
    'tot_asst_amt': '총자산금액',
    'buy_mgn_amt': '매수증거금액',
    'mgna_tota': '증거금총액',
    'frcr_use_psbl_amt': '외화사용가능금액',
    'ustl_sll_amt_smtl': '미결제매도금액합계',
    'ustl_buy_amt_smtl': '미결제매수금액합계',
    'tot_frcr_cblc_smtl': '총외화잔고합계',
    'tot_loan_amt': '총대출금액'
}

def main():
    """
    [해외주식] 주문/계좌
    해외주식 체결기준현재잔고[v1_해외주식-008]

    해외주식 체결기준현재잔고 테스트 함수
    
    Parameters:
        - cano (str): 종합계좌번호 (계좌번호 체계(8-2)의 앞 8자리)
        - acnt_prdt_cd (str): 계좌상품코드 (계좌번호 체계(8-2)의 뒤 2자리)
        - wcrc_frcr_dvsn_cd (str): 원화외화구분코드 (01 : 원화  02 : 외화)
        - natn_cd (str): 국가코드 (000 전체 840 미국 344 홍콩 156 중국 392 일본 704 베트남)
        - tr_mket_cd (str): 거래시장코드 ([Request body NATN_CD 000 설정] 00 : 전체  [Request body NATN_CD 840 설정] 00 : 전체 01 : 나스닥(NASD) 02 : 뉴욕거래소(NYSE) 03 : 미국(PINK SHEETS) 04 : 미국(OTCBB) 05 : 아멕스(AMEX)  [Request body NATN_CD 156 설정] 00 : 전체 01 : 상해B 02 : 심천B 03 : 상해A 04 : 심천A  [Request body NATN_CD 392 설정] 01 : 일본  [Request body NATN_CD 704 설정] 01 : 하노이거래 02 : 호치민거래소  [Request body NATN_CD 344 설정] 01 : 홍콩 02 : 홍콩CNY 03 : 홍콩USD)
        - inqr_dvsn_cd (str): 조회구분코드 (00 : 전체  01 : 일반해외주식  02 : 미니스탁)
        - env_dv (str): 실전모의구분 (real:실전, demo:모의)

    Returns:
        - DataFrame: 해외주식 체결기준현재잔고 결과
    
    Example:
        >>> df1, df2, df3 = get_trading_inquire_present_balance(cano=trenv.my_acct, acnt_prdt_cd="01", wcrc_frcr_dvsn_cd="02", natn_cd="000", tr_mket_cd="00", inqr_dvsn_cd="00", env_dv="real")  # 실전투자
        >>> df1, df2, df3 = get_trading_inquire_present_balance(cano=trenv.my_acct, acnt_prdt_cd="01", wcrc_frcr_dvsn_cd="02", natn_cd="000", tr_mket_cd="00", inqr_dvsn_cd="00", env_dv="demo")  # 모의투자
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
        trenv = ka.getTREnv()

        # 해외주식 체결기준현재잔고 파라미터 설정
        logger.info("API 파라미터 설정 중...")
        cano = trenv.my_acct  # 계좌번호 (자동 설정)
        acnt_prdt_cd = "01"  # 계좌상품코드
        wcrc_frcr_dvsn_cd = "02"  # 원화외화구분코드
        natn_cd = "000"  # 국가코드
        tr_mket_cd = "00"  # 거래시장코드
        inqr_dvsn_cd = "00"  # 조회구분코드

        
        # API 호출
        logger.info("API 호출 시작: 해외주식 체결기준현재잔고 (%s)", "실전투자" if env_dv == "real" else "모의투자")
        result1, result2, result3 = trading_inquire_present_balance.get_trading_inquire_present_balance(
            cano=cano,  # 종합계좌번호
            acnt_prdt_cd=acnt_prdt_cd,  # 계좌상품코드
            wcrc_frcr_dvsn_cd=wcrc_frcr_dvsn_cd,  # 원화외화구분코드
            natn_cd=natn_cd,  # 국가코드
            tr_mket_cd=tr_mket_cd,  # 거래시장코드
            inqr_dvsn_cd=inqr_dvsn_cd,  # 조회구분코드
            env_dv=env_dv,  # 실전모의구분
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
