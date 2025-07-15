"""
Created on 2025-07-09
@author: LaivData jjlee with cursor
"""

import logging
import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import kis_auth as kis
from etf_nav_trend import etf_nav_trend

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    국내ETF NAV추이
    
    [참고자료]
실시간시세(웹소켓) 파이썬 샘플코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/blob/main/websocket/python/ws_domestic_overseas_all.py

실시간시세(웹소켓) API 사용방법에 대한 자세한 설명은 한국투자증권 Wikidocs 참고 부탁드립니다.
https://wikidocs.net/book/7847 (국내주식 업데이트 완료, 추후 해외주식·국내선물옵션 업데이트 예정)

종목코드 마스터파일 파이썬 정제코드는 한국투자증권 Github 참고 부탁드립니다.
https://github.com/koreainvestment/open-trading-api/tree/main/stocks_info
    """

    # pandas 출력 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
    pd.set_option('display.width', None)  # 출력 너비 제한 해제
    pd.set_option('display.max_rows', None)  # 모든 행 표시

    # 인증 토큰 발급
    kis.auth()
    kis.auth_ws()

    # 인증(auth_ws()) 이후에 선언
    kws = kis.KISWebSocket(api_url="/tryitout")

    # 조회
    kws.subscribe(request=etf_nav_trend, data=["069500"])

    # 결과 표시
    def on_result(ws, tr_id: str, result: pd.DataFrame, data_map: dict):
        try:
            # 컬럼 매핑
            column_mapping = {
                "rt_cd": "성공 실패 여부",
                "msg_cd": "응답코드",
                "mksc_shrn_iscd": "유가증권단축종목코드",
                "nav": "NAV",
                "nav_prdy_vrss_sign": "NAV전일대비부호",
                "nav_prdy_vrss": "NAV전일대비",
                "nav_prdy_ctrt": "NAV전일대비율",
                "oprc_nav": "NAV시가",
                "hprc_nav": "NAV고가",
                "lprc_nav": "NAV저가"
            }
            result.rename(columns=column_mapping, inplace=True)

            # 숫자형 컬럼 변환
            numeric_columns = ["NAV", "NAV전일대비", "NAV전일대비율", "NAV시가", "NAV고가", "NAV저가"]
            for col in numeric_columns:
                if col in result.columns:
                    result[col] = pd.to_numeric(result[col], errors='coerce')

            logging.info("결과:")
            print(result)
        except Exception as e:
            logging.error(f"결과 처리 중 오류: {e}")
            logging.error(f"받은 데이터: {result}")

    kws.start(on_result=on_result)


if __name__ == "__main__":
    main()