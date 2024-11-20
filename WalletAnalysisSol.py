import requests
import random
import json
from concurrent.futures import ThreadPoolExecutor

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


def select_random_wallets(input_file, output_file, count):
    """
    Select a random subset of wallet addresses from an input file and save to an output file.

    Parameters:
        input_file (str): Path to the input file containing wallet addresses.
        output_file (str): Path to the output file to save selected wallets.
        count (int): Number of wallets to select.

    Returns:
        None
    """
    try:
        with open(input_file, "r") as f:
            holders = [line.strip() for line in f if line.strip()]
        total_holders = len(holders)
        print(f"Total wallets available in {input_file}: {total_holders}")

        if total_holders == 0:
            print("No wallets found in the input file.")
            return

        if total_holders < count:
            print(
                f"Requested {count} wallets, but only {total_holders} available. Selecting all."
            )
            selected_wallets = holders
        else:
            selected_wallets = random.sample(holders, count)

        with open(output_file, "w") as f:
            for wallet in selected_wallets:
                f.write(wallet + "\n")
        print(f"Saved {len(selected_wallets)} random wallets to {output_file}")

    except FileNotFoundError:
        print(f"Input file {input_file} not found.")
    except IOError as e:
        print(f"Error reading from file {input_file} or writing to {output_file}: {e}")


def get_all_transaction_signatures(wallet_address):
    """
    Fetch all transaction signatures for a specific wallet address.

    Parameters:
        wallet_address (str): The wallet address.

    Returns:
        list: A list of all transaction signatures.
    """
    headers = {"Content-Type": "application/json"}
    all_signatures = []
    before = None  # For pagination

    while True:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                wallet_address,
                {"before": before, "limit": 1000},  # Maximum allowed limit
            ],
        }

        try:
            response = requests.post(HELIUS_RPC_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            # Extract transaction signatures
            if "result" in data:
                signatures = [entry["signature"] for entry in data["result"]]
                all_signatures.extend(signatures)

                # Stop if no more signatures
                if len(signatures) == 0:
                    break

                # Update 'before' for the next batch
                before = signatures[-1]
            else:
                break

        except requests.exceptions.RequestException as e:
            print(f"Error fetching transaction signatures for {wallet_address}: {e}")
            break

    return all_signatures


def fetch_wallet_transactions(wallets):
    """
    Fetch all transactions for a list of wallets using multithreading.

    Parameters:
        wallets (list): List of wallet addresses.

    Returns:
        dict: A dictionary mapping wallets to their transaction signatures.
    """
    wallet_transactions = {}

    def process_wallet(wallet):
        print(f"Fetching all transactions for wallet: {wallet}")
        wallet_transactions[wallet] = get_all_transaction_signatures(wallet)

    # Use ThreadPoolExecutor to process wallets concurrently
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process_wallet, wallets)

    return wallet_transactions


def save_to_file(data, output_file):
    """
    Save wallet transactions to a JSON file.

    Parameters:
        data (dict): Wallet transactions mapping.
        output_file (str): File to save the JSON data.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Saved wallet transactions to {output_file}")
    except IOError as e:
        print(f"Error saving to file {output_file}: {e}")


if __name__ == "__main__":
    # Load wallets from file
    input_file = "random_wallets_goat.txt"  # File containing selected wallets
    output_file = "Wallet_Transactions.txt"  # Output file for transactions

    try:
        with open(input_file, "r") as f:
            wallets = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(wallets)} wallets from {input_file}.")

        # Fetch transactions for all wallets using multithreading
        wallet_transactions = fetch_wallet_transactions(wallets)

        # Save results to file
        save_to_file(wallet_transactions, output_file)

    except FileNotFoundError:
        print(f"Input file {input_file} not found.")
    except IOError as e:
        print(f"Error processing files: {e}")
# Example Usage


""" if __name__ == "__main__":
    # Replace with your token's mint address (base58 encoded)
    GOAT_MINT_ADDRESS = (
        "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump"  # Example mint address
    )

    # Uncomment the following lines if you want to fetch and save all holders

    token_holders = get_all_token_holders(GOAT_MINT_ADDRESS)
    print(f"Found {len(token_holders)} unique token holders.")

    # Save the holders to a file with each address on a new line
    all_holders_file = "goat_wallets.txt"
    save_holders_to_file(token_holders, all_holders_file)


    # Randomly select wallets from an existing file
  
    input_file = "goat_wallets.txt"  # Ensure this file exists with wallet addresses
    output_file = "random_wallets_goat.txt"
    TARGET_COUNT = 1111

    select_random_wallets(input_file, output_file, TARGET_COUNT)

    # Fetch wallet transactions and save to Wallet_Transactions.txt
    input_file = "random_wallets_goat.txt"  # File containing selected wallets
    output_file = "Wallet_Transactions.txt"
    save_wallet_transactions(input_file, output_file)
    #Error fetching transaction signatures for 6B14N3ipKBRPYBp99XpbG9MbtcRFdNXjGHYAp92VgJhT: 429 Client Error: Too Many Requests for url: https://mainnet.helius-rpc.com/?api-key=a9b51e58-4867-4519-950f-3b4769e73873

 """
