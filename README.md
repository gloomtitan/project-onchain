# project-onchain
Some basics:
- Primarily for work data from Solana
- workflow can be in the following way
- - Start with a set of random wallets
  - write code to get stats on the wallets
  - - win rate %
    - gain %
    - loss %
    - net pnl
    - avg roi
    - risk adjusted return ... ?
    - number of trades
    - size of trades
    - trade frequency
    - max drawdown
    - win/loss ratio
    - exposure to volatility
    - total transaction fees (gas/mev protection/bribe)
    - avg fee per trade
    - slippage
    - token diversity (types of assets. Can be sorted by mcap and/or category)
    - wallet growth
    - holding period
    - trade times

  - write code to calculate all this and rank all wallets
  - come up with an appropriate grading/scoring system to give wallets (weigh all the parameters according to scale, scope, potential, etc)


How we can go about this:
1. Get random 1000 wallets from any good coin (presumably we will use $GOAT)
2. write code for each parameter, rank them according to decided weightage. Test out how good the returns would be for each wallets over a given time period. Keep growing the data set.
