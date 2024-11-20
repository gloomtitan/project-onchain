import requests

# Helius RPC endpoint with your API key
HELIUS_RPC_ENDPOINT = (
    "https://mainnet.helius-rpc.com/?api-key=a9b51e58-4867-4519-950f-3b4769e73873"
)

# SPL Token Program ID
SPL_TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"


def get_all_token_holders(mint_address):
    """
    Fetch all main wallet addresses holding a specific token.

    Parameters:
        mint_address (str): The mint address of the token.

    Returns:
        list: A list of unique wallet addresses holding the token.
    """
    headers = {"Content-Type": "application/json"}

    # Create the filter for the token mint
    filters = [
        {
            "memcmp": {
                "offset": 0,  # Mint address starts at offset 0 in token account data
                "bytes": mint_address,  # Use the base58 mint address directly
            }
        },
        {"dataSize": 165},  # Size of a token account
    ]

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [
            SPL_TOKEN_PROGRAM_ID,
            {"encoding": "jsonParsed", "filters": filters},
        ],
    }

    try:
        response = requests.post(
            HELIUS_RPC_ENDPOINT, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Extract owner addresses from the token accounts
        holders = []
        if "result" in data:
            for account in data["result"]:
                owner_address = account["account"]["data"]["parsed"]["info"]["owner"]
                holders.append(owner_address)

        # Remove duplicates (since multiple token accounts may belong to the same owner)
        unique_holders = list(set(holders))
        return unique_holders

    except requests.exceptions.RequestException as e:
        print(f"Error fetching token holders: {e}")
        return []


def save_holders_to_file(holders, filename):
    """
    Save wallet addresses to a text file, each on a new line.

    Parameters:
        holders (list): List of wallet addresses.
        filename (str): Name of the output file.
    """
    try:
        with open(filename, "w") as f:
            for holder in holders:
                f.write(holder + "\n")
        print(f"Saved {len(holders)} unique token holders to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


# Example Usage
if __name__ == "__main__":
    GOAT_MINT_ADDRESS = "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"  # Replace with your token's mint address
    token_holders = get_all_token_holders(GOAT_MINT_ADDRESS)
    print(f"Found {len(token_holders)} unique token holders.")

    # Save the holders to a file with each address on a new line
    save_holders_to_file(token_holders, "goat_wallets.txt")
