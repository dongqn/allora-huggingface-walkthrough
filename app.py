import json
from flask import Flask, Response
import requests
import random

# create our Flask app
app = Flask(__name__)

# Load config.json to extract any necessary configuration (if needed)
with open('/root/allora-huggingface-walkthrough/config.json') as config_file:
    config_data = json.load(config_file)

# Function to get block height of Dogecoin from Upshot API
def get_block_height():
    url = "https://api.upshot.xyz/v2/block-height/dogecoin"  # URL for Dogecoin's block height
    headers = {
        "accept": "application/json",
        "Authorization": "UP-0d9ed54694abdac60fd23b74"  # Replace with your Upshot API key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        block_height = data.get('blockHeight')  # Adjust according to the actual API structure
        return block_height
    else:
        return None

# Map token symbol for Dogecoin
def get_simple_price(token):
    token_map = {
        'DOGE': 'dogecoin'
    }
    token = token.upper()
    return token_map.get(token, None)

# Endpoint for price inference based on Dogecoin's block height
@app.route("/inference/dogecoin")
def get_inference():
    try:
        value_percent = 5  # Percentage for price prediction range
        print(f"Prediction percentage: {value_percent}%")

        # Get block height from Upshot API for Dogecoin
        block_height = get_block_height()
        if not block_height:
            return "Failed to fetch Dogecoin block height", 400

        # Get the simple price ID for Dogecoin from CoinGecko
        current_token = get_simple_price("DOGE")
        if not current_token:
            return "Unsupported token: DOGE", 400

        # Call the CoinGecko API to get the current price for Dogecoin
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={current_token}&vs_currencies=usd"
        price_response = requests.get(price_url)

        if price_response.status_code == 200:
            price_data = price_response.json()
            current_price = price_data[current_token]["usd"]

            # Apply percentage to calculate price range for prediction
            price1 = current_price + current_price * (value_percent / 100)
            price2 = current_price - current_price * (value_percent / 100)

            # Generate a random price within the calculated range
            predicted_price = round(random.uniform(price1, price2), 7)
            return f"Predicted price for Dogecoin at block height {block_height}: {predicted_price}", 200
        else:
            return f"Failed to fetch price for Dogecoin: {price_response.status_code}", 400

    except Exception as e:
        return str(e), 400

# run our Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8800, debug=True)
