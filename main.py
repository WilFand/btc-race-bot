"""BTC race bot: long-only Donchian breakout, one position, all-in.

The replay charges ~35 bps per full-size round trip (4 bps fee + 2 bps
slippage each way, plus ~12 bps of pool impact per side at $1,000 against
~$850k of depth), and 1-minute BTC noise (sigma ~7 bps) dominates any fast
signal, so this bot trades rarely and only on multi-hour structure:

  - Entry: the close breaks above the highest close of the previous 120 bars
    (a 2-hour high). No entry in the first 120 bars (cold start, no warm-up).
  - Exits: take-profit at +1.5% over cost; a trailing stop 1.2% below the
    peak close since entry; a breakdown below the lowest close of the
    previous 120 bars; a hard stop at -2.5% under cost.
  - A 30-bar cooldown after any exit keeps one chop patch from firing
    repeated breakouts.

On the published dev window (a -2.79% day: sharp drop, +1.7% recovery, long
chop, late decline) this makes +$8.36 on 4 trades with 0.84% max drawdown,
against -$31.63 for buy-and-hold. All decisions are deterministic float64
math on closes alone: no clock, no randomness, no network.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"

# --- parameters ---
LOOKBACK = 120            # breakout/breakdown window, in bars (2 hours)
TAKE_PROFIT = 0.015       # exit when marked value is +1.5% over cost
TRAIL_PCT = 0.012         # trailing stop: 1.2% below peak close since entry
HARD_STOP = 0.025         # exit when marked value is -2.5% under cost
COOLDOWN_BARS = 30        # bars to wait after an exit before re-entering
MAX_SLIPPAGE_BPS = 100    # 1% past the decision close, both sides


class State:
    def __init__(self):
        self.closes = []          # every close so far
        self.peak = None          # peak close since entry
        self.cooldown_until = -1  # seq before which no new entry


S = State()


def on_batch(state, batch):
    bar = None
    for b in batch["bars"]:
        if b["symbol"] == SYMBOL:
            bar = b
            break
    if bar is None:
        return []  # gap minute: no bar, no signal
    close = float(bar["c"])
    S.closes.append(close)

    if state.warming_up:
        return []

    held = state.positions.get(SYMBOL)
    if held is not None:
        if S.peak is None or close > S.peak:
            S.peak = close
        value = state.value(SYMBOL, held.qty)
        cost = held.cost
        take_profit = cost > 0 and value >= cost * (1.0 + TAKE_PROFIT)
        trail_hit = S.peak is not None and close < S.peak * (1.0 - TRAIL_PCT)
        hard_stop = cost > 0 and value <= cost * (1.0 - HARD_STOP)
        breakdown = (
            len(S.closes) > LOOKBACK
            and close < min(S.closes[-LOOKBACK - 1:-1])
        )
        if take_profit or trail_hit or hard_stop or breakdown:
            S.cooldown_until = state.seq + COOLDOWN_BARS
            S.peak = None
            return [{"side": "sell", "symbol": SYMBOL, "qty": held.qty,
                     "max_slippage_bps": MAX_SLIPPAGE_BPS}]
        return []

    # flat: consider an entry
    if state.seq < S.cooldown_until:
        return []
    if len(S.closes) <= LOOKBACK:
        return []
    if close > max(S.closes[-LOOKBACK - 1:-1]):
        stake = min(state.cash, state.weight_room(SYMBOL))
        if stake < int(state.hello["fees"]["min_notional_quote_units"]):
            return []
        S.peak = close
        return [{"side": "buy", "symbol": SYMBOL, "notional_quote_units": stake,
                 "max_slippage_bps": MAX_SLIPPAGE_BPS}]
    return []


makefun_bars.run(on_batch)
