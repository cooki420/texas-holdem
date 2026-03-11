# ♠ Texas Hold'em Simulator

A Texas Hold'em simulator for 10 players written in pure Python with no external dependencies.

Deals 2 hole cards to each player, reveals the board (flop, turn, river), evaluates the best 5-card hand for each player, and declares the winner.

## Usage

Requires Python 3.8+. No external libraries needed.
```bash
python texas_holdem.py
```

## Example Output
```
♠  TEXAS HOLD'EM  ♠

  BTN        9♦   4♣   →  One Pair
  SB         A♠   5♣   →  One Pair
  BB         7♠   9♥   →  One Pair
  UTG        Q♦   A♥   →  Three of a Kind  ◀ WINS
  UTG+1      K♥   4♥   →  Two Pair
  UTG+2      Q♥   J♥   →  Three of a Kind
  MP         6♦  10♥   →  One Pair
  MP+1       9♣   6♠   →  One Pair
  HJ         9♠   5♦   →  One Pair
  CO         3♦   J♣   →  One Pair

  Flop :  Q♣  8♥  2♥
  Turn :  Q♠
  River:  K♦

  🏆  UTG wins with Three of a Kind
      Best hand: Q♦  A♥  Q♣  Q♠  K♦
```

## Features

- 10 players with real positions (BTN, SB, BB, UTG, ...)
- Full board: flop, turn, river
- Best 5-card hand selected from 7 cards for each player
- All 10 hand rankings recognised
- Tiebreaker resolution via kicker
- Colored output (red for hearts and diamonds)

## Roadmap

- [ ] Project 2 — Odds Calculator (Monte Carlo)
- [ ] Project 3 — Hand History Parser
- [ ] Project 4 — Bankroll Tracker
- [ ] Project 5 — GTO Push/Fold Solver
