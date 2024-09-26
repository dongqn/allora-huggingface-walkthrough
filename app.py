from flask import Flask, Response
import requests
import json
import random

# create our Flask app
app = Flask(__name__)

def get_simple_price(token):
    token_map = {
        'ETH': 'ethereum',
        'SOL': 'solana',
        'BTC': 'bitcoin',
        'BNB': 'binancecoin',
        'ARB': 'arbitrum'
    }
    token = token.upper()
    if token in token_map:
        return token_map[token]
    else:
        # If the token is not recognized, use the block height to infer it
        meme_token = get_token_symbol_from_block_height(token)
        return meme_token

def get_token_symbol_from_block_height(block_height):
    url = f'https://api.upshot.xyz/v2/nft/ethereum/blocks/{block_height}'
    headers = {
        "accept": "application/json",
        "x-api-key": "UP-0d9ed54694abdac60fd23b74"  # Thay thế bằng API key thật của bạn
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Extract token symbol or relevant data from response
        # Modify this based on the actual structure of the upshot.xyz response
        return data.get('tokenSymbol', 'Unknown Token')  # Example key from the API response

    raise ValueError(f"Failed to fetch block data from upshot.xyz: {response.status_code}")

# define our endpoint
@app.route("/inference/<string:token>")
def get_inference(token):
    try:
        # Fixed value for percent prediction, or calculated based on custom logic
        value_percent = 5  # This can be dynamically determined
        print(value_percent)

        base_url = "https://api.coingecko.com/api/v3/simple/price?ids="
        current_token = get_simple_price(token)
        url = f"{base_url}{current_token}&vs_currencies=usd"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": "<Your Coingecko API key>"  # Replace with your CoinGecko API key
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            # Adjust price prediction logic based on token
            if token == 'BTC':
                price1 = data["bitcoin"]["usd"] + data["bitcoin"]["usd"] * (value_percent / 100)
                price2 = data["bitcoin"]["usd"] - data["bitcoin"]["usd"] * (value_percent / 100)
            elif token == 'ETH':
                price1 = data["ethereum"]["usd"] + data["ethereum"]["usd"] * (value_percent / 100)
                price2 = data["ethereum"]["usd"] - data["ethereum"]["usd"] * (value_percent / 100)
            elif token == 'SOL':
                price1 = data["solana"]["usd"] + data["solana"]["usd"] * (value_percent / 100)
                price2 = data["solana"]["usd"] - data["solana"]["usd"] * (value_percent / 100)
            elif token == 'BNB':
                price1 = data["binancecoin"]["usd"] + data["binancecoin"]["usd"] * (value_percent / 100)
                price2 = data["binancecoin"]["usd"] - data["binancecoin"]["usd"] * (value_percent / 100)
            elif token == 'ARB':
                price1 = data["arbitrum"]["usd"] + data["arbitrum"]["usd"] * (value_percent / 100)
                price2 = data["arbitrum"]["usd"] - data["arbitrum"]["usd"] * (value_percent / 100)
            else:
                price1 = data[current_token]["usd"] + data[current_token]["usd"] * (value_percent / 100)
                price2 = data[current_token]["usd"] - data[current_token]["usd"] * (value_percent / 100)

            # Return the most accurate prediction between price1 and price2
            random_float = str(round(random.uniform(price1, price2), 7))
            return random_float
        else:
            return f"Failed to fetch price for {token}: {response.status_code}", 400

    except Exception as e:
        return str(e), 400


# run our Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8800, debug=True)
