import requests
import json

offer_address = "EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA" # should be replaced with hamster address
ask_address = 'EQCM3B12QK1e4yZSf8GtBRT0aLMNyEsBc_DhVfRRtOEffLez' # should be replaced with USDT address EQDHZDgZjMT8gJazbGj_mzSZDv4QcngZAx57Zx6M1HWJPk5I
units = 1 # how many tokens i want to swap
url = 'https://api.ston.fi/v1/swap/simulate'
params = {
    'offer_address': offer_address,
    'ask_address': ask_address,
    'units': units,
    'slippage_tolerance': 0.1
}

response = requests.post(url, params=params, headers={'accept': 'application/json'})

if response.status_code == 200:
    data = response.json()
    
    print(json.dumps(data, indent=4))
    
    offer_address = data['offer_address']
    ask_address = data['ask_address']
    offer_jetton_wallet = data['offer_jetton_wallet']
    ask_jetton_wallet = data['ask_jetton_wallet']
    router_address = data['router_address']
    pool_address = data['pool_address']
    offer_units = data['offer_units']
    ask_units = data['ask_units']
    slippage_tolerance = data['slippage_tolerance']
    min_ask_units = data['min_ask_units']
    swap_rate = data['swap_rate']
    price_impact = data['price_impact']
    fee_address = data['fee_address']
    fee_units = data['fee_units']
    fee_percent = data['fee_percent']
    
    # execute_swap(offer_address, ask_address, offer_units, slippage_tolerance)

else:
    print(f"Failed to simulate swap. Status code: {response.status_code}")
    print(f"Response: {response.text}")

def execute_swap(offer_address, ask_address, offer_units, slippage_tolerance):
    pass
