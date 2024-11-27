-- CreateTable
CREATE TABLE "Wallet" (
    "walletId" BIGINT NOT NULL,
    "win_rate_percent" BIGINT,
    "gain_percent" BIGINT,
    "loss_percent" BIGINT,
    "net_pnl" BIGINT,
    "avg_roi" BIGINT,
    "risk_adjusted_return" BIGINT,
    "new_column" BIGINT,
    "number_of_trades" BIGINT,
    "size_of_trades" BIGINT,
    "trade_frequency" BIGINT,
    "max_drawdown" BIGINT,
    "win_loss_ratio" BIGINT,
    "exposure_to_volatility" BIGINT,
    "total_transaction_fees" BIGINT,
    "avg_fee_per_trade" BIGINT,
    "slippage" BIGINT,
    "token_diversity" BIGINT,
    "wallet_growth" BIGINT,
    "holding_period" BIGINT,
    "trade_times" BIGINT,

    CONSTRAINT "Wallet_pkey" PRIMARY KEY ("walletId")
);

-- CreateTable
CREATE TABLE "Transactions" (
    "signature" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "source" TEXT NOT NULL,
    "fee" BIGINT NOT NULL,
    "feePayer" TEXT NOT NULL,
    "slot" BIGINT NOT NULL,
    "timestamp" BIGINT NOT NULL,
    "walletId" BIGINT NOT NULL,

    CONSTRAINT "Transactions_pkey" PRIMARY KEY ("signature")
);

-- CreateTable
CREATE TABLE "TokenTransfer" (
    "id" BIGSERIAL NOT NULL,
    "fromTokenAccount" TEXT NOT NULL,
    "toTokenAccount" TEXT NOT NULL,
    "fromUserAccount" TEXT NOT NULL,
    "toUserAccount" TEXT NOT NULL,
    "tokenAmount" BIGINT NOT NULL,
    "mint" TEXT NOT NULL,
    "tokenStandard" TEXT NOT NULL,
    "signature" TEXT NOT NULL,

    CONSTRAINT "TokenTransfer_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Transactions" ADD CONSTRAINT "Transactions_walletId_fkey" FOREIGN KEY ("walletId") REFERENCES "Wallet"("walletId") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TokenTransfer" ADD CONSTRAINT "TokenTransfer_signature_fkey" FOREIGN KEY ("signature") REFERENCES "Transactions"("signature") ON DELETE RESTRICT ON UPDATE CASCADE;
