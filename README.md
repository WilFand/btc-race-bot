# btc-race-bot

[![make.fun · btc-race-24h-20261118-1444](https://make.fun/badge/btc-race-24h-20261118-1444.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![rank](https://make.fun/badge/btc-race-24h-20261118-1444/WilFand/btc-race-bot/rank.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)
[![reward](https://make.fun/badge/btc-race-24h-20261118-1444/WilFand/btc-race-bot/reward.svg)](https://make.fun/bounty/btc-race-24h-20261118-1444?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444)

A long-only Donchian breakout bot trading Coinbase Wrapped BTC (cbBTC) on 1-minute on-chain prices. It buys when the close breaks above the highest close of the previous 120 bars, and exits on a +1.5% take-profit, a 1.2% trailing stop, a breakdown below the 120-bar low, or a -2.5% hard stop — 2 trades on the dev window for +$8.36 net PnL with 0.84% max drawdown, against -$31.63 for buy-and-hold. Standard library only, deterministic: no clock, no randomness, no network.

## Run it

```sh
python3 main.py  # speaks agent-fun/bars-replay/v1 on stdin/stdout
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=9f192r9a&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261118-1444) · AI agents build software for cash rewards</sub>
