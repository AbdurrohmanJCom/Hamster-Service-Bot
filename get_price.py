import requests


def getPrice(token):
    if token == "not":
        url = "https://api.geckoterminal.com/api/v2/networks/ton/tokens/EQAvlWFDxGF2lXm67y4yzC17wYKD9A0guwPkMs1gOsM__NOT"
    else:
        return "TOKEN_NOT_FOUND 400: ADDRESS NEEDED"

    response = requests.get(url)
    data = response.json()

    price_usd = data["data"]["attributes"]["price_usd"]
    return price_usd
