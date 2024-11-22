from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


HELIUS_RPC_ENDPOINT = os.getenv("HELIUS_RPC_ENDPOINT")
SPL_TOKEN_PROGRAM_ID = os.getenv("SPL_TOKEN_PROGRAM_ID")
API_KEY = os.getenv("API_KEY")
# gets all wallet addresses in scope of one token
def get_all_token_holders(mint_address):
    headers = {"Content-Type": "application/json"}
    filters = [
        {"memcmp": {"offset": 0, "bytes": mint_address}},
        {"dataSize": 165},
    ]
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [SPL_TOKEN_PROGRAM_ID, {"encoding": "jsonParsed", "filters": filters}],
    }
    try:
        response = requests.post(
            HELIUS_RPC_ENDPOINT, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()
        data = response.json()
        holders = [
            account["account"]["data"]["parsed"]["info"]["owner"]
            for account in data.get("result", [])
        ]
        return list(set(holders))  # Remove duplicates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token holders: {e}")
        return []


# saves each token holder to a file
def save_holders_to_file(holders, filename):
    try:
        with open(filename, "w") as f:
            for holder in holders:
                f.write(holder + "\n")
        print(f"Saved {len(holders)} unique token holders to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

import requests
import json

def get_transaction_history(walletId):
    url = f"https://api.helius.xyz/v0/addresses/{walletId}/transactions?api-key={API_KEY}"
    
    # Send GET request
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "type": "BUY_ITEM,SELL_ITEM",
            "commitment": "finalized"
        }
    )
    
    # Get the raw response text
    raw_data = response.text
    
    # Remove the leading '[' and trailing ']' from the JSON array
    cleaned_data = raw_data.strip()[1:-1]
    
    # Convert cleaned string back to JSON
    data = json.loads(f"[{cleaned_data}]")  # Adding brackets back for valid JSON array

    filteredData = {
        walletId: {
            "description": data.get("description"),
            "type": data.get("type"),
            "fee": data.get("fee"),
            "feePayer": data.get("feePayer"),
            "signature": data.get("signature"),
            "timestamp": data.get("timestamp"),
            "tokenTransfers": data.get("tokenTransfers"),
            "accountData": data.get("accountData"),
        }
    }
    # Write the cleaned JSON to a file
    with open("walletData.json", "w") as f:
        json.dump(data, f, indent=4)
    
    print("Cleaned and converted JSON saved to walletData.json")



def main():
    # mint_address = "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"  # Replace with actual mint
    # print("Fetching token holders...")
    # token_holders = get_all_token_holders(mint_address)
    # print(f"Found {len(token_holders)} unique token holders.")
    # save_holders_to_file(token_holders, "goat_wallets.txt")

    get_transaction_history("4kfaWFh13XurM75WjTdgox8ZZ5vcQzGAZdaNiz7m55mZ");






if __name__ == "__main__":
    main()
