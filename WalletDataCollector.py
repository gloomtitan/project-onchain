import json
import asyncio
from prisma import Prisma

async def populate_wallet_and_transactions(file_path, wallet_id):
    db = Prisma()
    await db.connect()

    try:
        # Load JSON data
        with open(file_path, "r") as file:
            data = json.load(file)

        # Extract wallet information
        wallet_data = {
            "walletId": wallet_id,
            "win_rate_percent": None,
            "gain_percent": None,
            "loss_percent": None,
            "net_pnl": None,
            "avg_roi": None,
            "risk_adjusted_return": None,
            "new_column": None,
            "number_of_trades": None,
            "size_of_trades": None,
            "trade_frequency": None,
            "max_drawdown": None,
            "win_loss_ratio": None,
            "exposure_to_volatility": None,
            "total_transaction_fees": None,
            "avg_fee_per_trade": None,
            "slippage": None,
            "token_diversity": None,
            "wallet_growth": None,
            "holding_period": None,
            "trade_times": None,
        }

        # Check if wallet already exists
        wallet = await db.wallet.find_unique(
            where={"walletId": wallet_id}
        )

        # Create the wallet only if it doesn't exist
        if not wallet:
            wallet = await db.wallet.create(data=wallet_data)

        # Process transactions in the JSON file
        for transaction in data:
            # Skip transactions where tokenTransfers is null or empty
            if not transaction.get("tokenTransfers"):
                continue

            signature = transaction["signature"]
            description = transaction["description"]
            tx_type = transaction["type"]
            source = transaction["source"]
            fee = transaction["fee"]
            fee_payer = transaction["feePayer"]
            slot = transaction["slot"]
            timestamp = transaction["timestamp"]

            # Insert transaction linked to the wallet
            transaction_entry = await db.transactions.create(
                data={
                    "signature": signature,
                    "description": description,
                    "type": tx_type,
                    "source": source,
                    "fee": fee,
                    "feePayer": fee_payer,
                    "slot": slot,
                    "timestamp": timestamp,
                    "walletId": wallet.walletId,
                }
            )

            # Insert token transfers for the transaction
            for token_transfer in transaction["tokenTransfers"]:
                await db.tokentransfer.create(
                    data={
                        "fromTokenAccount": token_transfer.get("fromTokenAccount", ""),
                        "toTokenAccount": token_transfer.get("toTokenAccount", ""),
                        "fromUserAccount": token_transfer.get("fromUserAccount", ""),
                        "toUserAccount": token_transfer.get("toUserAccount", ""),
                        "tokenAmount": token_transfer.get("amount", 0),
                        "mint": token_transfer.get("mint", ""),
                        "tokenStandard": token_transfer.get("tokenStandard", ""),
                        "signature": signature,
                    }
                )

    finally:
        await db.disconnect()

async def readWallet(filepath):
    with open(filepath, 'r') as file:
        for walletId in file:
            walletId =walletId.strip()
            if walletId:
                await populate_wallet_and_transactions("./walletData.json", walletId)


# Run the function
if __name__ == "__main__":
    asyncio.run(readWallet("./walletData.json"))
