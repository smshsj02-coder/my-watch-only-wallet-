import requests

# 1. 조회하고 싶은 비트코인 주소를 입력하세요
address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh" 

def get_wallet_info(addr):
    # 잔액 조회를 위한 mempool API
    balance_url = f"https://mempool.space/api/address/{addr}"
    # 시세 조회를 위한 CoinGecko API
    price_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    
    try:
        # 잔액 가져오기
        b_resp = requests.get(balance_url)
        # 가격 가져오기
        p_resp = requests.get(price_url)
        
        if b_resp.status_code == 200 and p_resp.status_code == 200:
            b_data = b_resp.json()
            p_data = p_resp.json()
            
            # 잔액 계산
            confirmed = b_data['chain_stats']['funded_txo_sum'] - b_data['chain_stats']['spent_txo_sum']
            btc_balance = confirmed / 100_000_000
            
            # 현재 시세 및 가치 계산
            current_price = p_data['bitcoin']['usd']
            usd_value = btc_balance * current_price
            
            print(f"\n" + "="*30)
            print(f"   비트코인 워치온리 지갑")
            print(f"="*30)
            print(f"주소: {addr}")
            print(f"현재 잔액: {btc_balance:.8f} BTC")
            print(f"현재 시세: ${current_price:,.2f}")
            print(f"보유 가치: ${usd_value:,.2f}")
            print(f"="*30 + "\n")
        else:
            print("데이터를 가져오는 데 실패했습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

get_wallet_info(address)