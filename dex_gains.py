import requests, json, datetime

# Bitquery API key:
API_KEY        = "BQYxxxxxxxxxxxxxxxxxHBy"                     # Change this (Register at https://bitquery.io/ to get your own API key)

# Target's wallet address we want to scan:
trader_wallet  = "0x000000000000000000000000000000000000dead"  # Change this

# Token contract (Base Currency):
token_contract = "0x000000000000000000000000000000000000dead"  # Change this





# WBNB contract  (Quote Currency):
wbnb_contract    = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"  # Wrapped BNB contract address on BSC

BASE_URL = "https://graphql.bitquery.io/"

query = """
  query getGains($base: String, $quote: String, $trader: String){ 
    ethereum(network: bsc) {
    dexTrades(
      baseCurrency: {is: $base}
      quoteCurrency: {is: $quote}
      txSender: {is: $trader}
    ) {
      sellAmount(in: USD)
      buyAmount(in: USD)
    }
  }
}
"""

if __name__ == "__main__":
  params = {
    "base"   : token_contract,
    "quote"  : wbnb_contract,
    "trader" : trader_wallet
  }
  json_body = {"query"     : query, "variables" : params}
  headers   = {"X-API-KEY" : API_KEY}
  response  = requests.post(BASE_URL, json = json_body, headers = headers)

  if response.status_code == 200:
    jsonResp = response.json()
    sold = jsonResp['data']['ethereum']['dexTrades'][0]['sellAmount']
    bought = jsonResp['data']['ethereum']['dexTrades'][0]['buyAmount']
    gains = sold - bought

    timeNow = datetime.datetime.now()
    timeStampStr = timeNow.strftime("[%d-%b-%Y %H:%M:%S]")
    print(timeStampStr,"   Trader: ", trader_wallet, "  Token: ", token_contract)
    print("Bought for: ", "{:,.2f}".format(bought), "USD ; Sold for: ", "{:,.2f}".format(sold), "USD ; Gains of: ", "{:,.2f}".format(gains), "USD")

  else:
    error = (f"Query failed and return code is {response.status_code}. {query}")
    raise Exception(error)

