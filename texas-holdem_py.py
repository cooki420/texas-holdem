"""
texas_holdem.py
===============
Texas Hold'em simulator for 10 players.
Deals 2 hole cards to each player, reveals the board (flop, turn, river),
evaluates the best 5-card hand for each player, and declares the winner.

Usage:
    python texas_holdem.py
"""

import random
from collections import Counter
from itertools import combinations

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUITS      = ["♠", "♥", "♦", "♣"]
RANKS      = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VALUE = {r: i + 2 for i, r in enumerate(RANKS)}  # 2→2, A→14

POSITIONS  = ["BTN", "SB", "BB", "UTG", "UTG+1", "UTG+2", "MP", "MP+1", "HJ", "CO"]

HAND_NAMES = {
    0: "High Card",
    1: "One Pair",
    2: "Two Pair",
    3: "Three of a Kind",
    4: "Straight",
    5: "Flush",
    6: "Full House",
    7: "Four of a Kind",
    8: "Straight Flush",
    9: "Royal Flush",
}

# ---------------------------------------------------------------------------
# Deck
# ---------------------------------------------------------------------------

def create_deck():
    return [f"{r}{s}" for s in SUITS for r in RANKS]

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def deal(deck):
    hands = [deck[i*2:(i*2)+2] for i in range(10)]
    rest  = deck[20:]
    flop  = rest[:3]
    turn  = [rest[3]]
    river = [rest[4]]
    return hands, flop, turn, river

# ---------------------------------------------------------------------------
# Card parsing
# ---------------------------------------------------------------------------

def parse_card(card: str):
    """'A♠' → (14, '♠')"""
    suit  = card[-1]
    rank  = card[:-1]
    return RANK_VALUE[rank], suit

# ---------------------------------------------------------------------------
# Hand evaluation
# ---------------------------------------------------------------------------

def _is_straight(vals):
    if vals[0] - vals[4] == 4 and len(set(vals)) == 5:
        return True, vals[0]
    if vals == [14, 5, 4, 3, 2]:  # Wheel: A-2-3-4-5
        return True, 5
    return False, 0

def evaluate_hand(hand_5: list):
    """
    Evaluate a 5-card hand (list of strings like ['A♠','K♠',...]).
    Returns (rank 0-9, tiebreakers).
    """
    parsed   = [parse_card(c) for c in hand_5]
    vals     = sorted([v for v, _ in parsed], reverse=True)
    suits    = [s for _, s in parsed]

    flush             = len(set(suits)) == 1
    straight, st_high = _is_straight(vals)

    counts = Counter(vals)
    groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    gv     = [v for v, _ in groups]
    gc     = [c for _, c in groups]

    if flush and straight and st_high == 14: return 9, [14]
    if flush and straight:                   return 8, [st_high]
    if gc[0] == 4:                           return 7, [gv[0], gv[1]]
    if gc[0] == 3 and gc[1] == 2:           return 6, [gv[0], gv[1]]
    if flush:                                return 5, vals
    if straight:                             return 4, [st_high]
    if gc[0] == 3:                           return 3, [gv[0]] + sorted(gv[1:], reverse=True)
    if gc[0] == 2 and gc[1] == 2:           return 2, [gv[0], gv[1], gv[2]]
    if gc[0] == 2:                           return 1, [gv[0]] + sorted(gv[1:], reverse=True)
    return 0, vals

def best_hand_from_7(cards_7: list):
    """Find the best 5-card combination out of 7 cards (21 combos)."""
    best_rank, best_tb, best_combo = -1, [], []
    for combo in combinations(cards_7, 5):
        rank, tb = evaluate_hand(list(combo))
        if (rank, tb) > (best_rank, best_tb):
            best_rank, best_tb, best_combo = rank, tb, list(combo)
    return best_rank, best_tb, best_combo

# ---------------------------------------------------------------------------
# Winner
# ---------------------------------------------------------------------------

def find_winner(results: list):
    """Returns the winner(s) — handles ties."""
    best_rank = max(r["rank"] for r in results)
    candidates = [r for r in results if r["rank"] == best_rank]
    best_tb   = max(r["tb"] for r in candidates)
    return [r for r in candidates if r["tb"] == best_tb]

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

SUIT_COLOR = {
    "♠": "",      # black (default)
    "♥": RED,     # red
    "♣": GREEN,   # green
    "♦": BLUE,    # blue
}

def color_card(card: str) -> str:
    color = SUIT_COLOR.get(card[-1], "")
    return f"{color}{card}{RESET}" if color else card

def fmt_hand(hand: list) -> str:
    return "  ".join(color_card(c) for c in hand)

def print_results(hands, flop, turn, river, results, winners):
    width = 62
    print("\n" + "─" * width)
    print(f"{BOLD}{CYAN}{'♠  TEXAS HOLD\'EM  ♠':^{width}}{RESET}")
    print("─" * width)
    print()

    for r in results:
        arrow = f"  {GREEN}◀ WINS{RESET}" if r in winners else ""
        print(f"  {BOLD}{r['position']:<10}{RESET} {fmt_hand(r['hand'])}   →  {YELLOW}{HAND_NAMES[r['rank']]}{RESET}{arrow}")

    print()
    print(f"  {'Flop :':<8} {fmt_hand(flop)}")
    print(f"  {'Turn :':<8} {fmt_hand(turn)}")
    print(f"  {'River:':<8} {fmt_hand(river)}")
    print()

    if len(winners) == 1:
        w = winners[0]
        print(f"  {BOLD}🏆  {w['position']} wins with {HAND_NAMES[w['rank']]}{RESET}")
        print(f"      Best hand: {fmt_hand(w['best_combo'])}")
    else:
        names = " and ".join(w["position"] for w in winners)
        print(f"  {BOLD}🤝  Tie between {names} — {HAND_NAMES[winners[0]['rank']]}{RESET}")

    print("─" * width)

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    print(f"\n{BOLD}{CYAN}♠  Texas Hold'em Simulator — 10 Players  ♠{RESET}")

    while True:
        deck              = shuffle_deck(create_deck())
        hands, flop, turn, river = deal(deck)
        board             = flop + turn + river

        results = []
        for i in range(10):
            cards_7 = hands[i] + board
            rank, tb, best_combo = best_hand_from_7(cards_7)
            results.append({
                "position":  POSITIONS[i],
                "hand":      hands[i],
                "rank":      rank,
                "tb":        tb,
                "best_combo": best_combo,
            })

        winners = find_winner(results)
        print_results(hands, flop, turn, river, results, winners)

        answer = input("\nPress Enter for a new hand, or type 'x' to quit: ")
        if answer.strip().lower() == "x":
            print(f"\n{CYAN}See you at the tables! ♠{RESET}\n")
            break

if __name__ == "__main__":
    main()
