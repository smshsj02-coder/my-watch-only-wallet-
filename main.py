import requests

# 조회하고 싶은 비트코인 주소를 입력하세요
address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh" 

def get_balance(addr):
    url = f"https://mempool.space/api/address/{addr}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # 확정 잔액 계산 (Satoshi -> BTC)
            confirmed = data['chain_stats']['funded_txo_sum'] - data['chain_stats']['spent_txo_sum']
            print(f"\n============================")
            print(f"주소: {addr}")
            print(f"현재 잔액: {confirmed / 100_000_000} BTC")
            print(f"============================\n")
        else:
            print("데이터를 가져오지 못했습니다. 주소를 확인하세요.")
    except Exception as e:
        print(f"오류 발생: {e}")

get_balance(address)