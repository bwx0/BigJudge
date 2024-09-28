import random
from enum import Enum
from typing import Optional
from itertools import combinations

from classes import *


"""
Always plays the strongest combination where possible.
"""

RANKS = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
SUITS = ['D', 'C', 'H', 'S']
all_cards = [rank + suit for rank in RANKS for suit in SUITS]


def get_strength(card: str) -> int:
    return RANKS.index(card[0]) * 4 + SUITS.index(card[1])


def get_card(strength: int) -> str:
    rank = RANKS[strength // 4]
    suit = SUITS[strength % 4]
    return rank + suit


def get_rank(strength: int) -> str:
    rank = RANKS[strength // 4]
    return rank


def get_suit(strength: int) -> str:
    suit = SUITS[strength % 4]
    return suit


class TrickType(Enum):
    PASS = 0
    SINGLE = 1
    PAIR = 2
    TRIPLET = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8


# Copied from Big2Judge
def validate_trick_and_get_strength(action: List[str]):
    if not isinstance(action, List):
        return False, -1, TrickType.PASS, "Invalid action type."

    len_action = len(action)
    if len_action == 0:
        return True, 0, TrickType.PASS, "Action: Pass"
    if len_action > 5:
        return False, -1, TrickType.PASS, "Trick too long."
    if len_action != len(set(action)):
        return False, -1, TrickType.PASS, "Duplicate cards."

    p_ranks: List[str] = [x[0] for x in action]
    p_suits: List[str] = [x[1] for x in action]
    strengths = [get_strength(x) for x in action]

    # 1 card, single
    if len_action == 1:
        return True, strengths[0], TrickType.SINGLE, "Action: Single"

    # 2 cards, pair
    if len_action == 2:
        if p_ranks[0] != p_ranks[1]:
            return False, -1, TrickType.PASS, "Invalid pair."
        return True, max(strengths), TrickType.PAIR, "Action: Pair"

    # 3 cards, triplet
    if len_action == 3:
        if p_ranks[0] != p_ranks[1] or p_ranks[1] != p_ranks[2]:
            return False, -1, TrickType.PASS, "Invalid triplet."
        return True, max(strengths), TrickType.TRIPLET, "Action: Triplet"

    # 4 cards, invalid
    if len_action == 4:
        return False, -1, TrickType.PASS, "Invalid trick with length 4."

    # 5 cards
    if len_action == 5:
        ranks_val: List[int] = [RANKS.index(x) for x in p_ranks]
        suits_val: List[int] = [SUITS.index(x) for x in p_suits]
        n_distinct_ranks = len(set(p_ranks))
        n_distinct_suits = len(set(p_suits))
        is_flush = n_distinct_suits == 1
        is_straight = n_distinct_ranks == 5 and max(ranks_val) - min(ranks_val) == 4

        # straigt flush
        if is_flush and is_straight:
            return True, max(strengths), TrickType.STRAIGHT_FLUSH, "Action: Straight flush"

        # flush
        if is_flush:
            strength = sum([(100 ** i) * v for i, v in enumerate(ranks_val)]) * 100000 + \
                       sum([(10 ** i) * v for i, v in enumerate(suits_val)])
            return True, strength, TrickType.FLUSH, "Action: Flush"

        # straight
        if is_straight:
            return True, max(strengths), TrickType.STRAIGHT, "Action: Straight"

        # four-of-a-kind, full house
        if len_action == 5 and n_distinct_ranks == 2:
            rank_counts = [p_ranks.count(x) for x in p_ranks]
            # full house
            if 3 in rank_counts and 2 in rank_counts:
                strength = max([strengths[i] for i in range(5) if rank_counts[i] == 3])
                return True, strength, TrickType.FULL_HOUSE, "Action: Full house"
            # four-of-a-kind
            if 4 in rank_counts and 1 in rank_counts:
                strength = max([strengths[i] for i in range(5) if rank_counts[i] == 4])
                return True, strength, TrickType.FOUR_OF_A_KIND, "Action: For-of-a-kind"

        # invalid trick
        return False, -1, TrickType.PASS, "Invalid trick."


class Algorithm:

    def getAction(self, state: MatchState):
        action = []  # The cards you are playing for this trick
        myData = state.myData  # Communications from the previous iteration

        # Sort hand from lowest to highest card
        sortedHand = sorted(state.myHand, key=lambda x: get_strength(x))

        if sortedHand[0] == "3D":
            action.append("3D")
        elif state.toBeat is None:
            valid_tricks = []
            for clen in [1, 2, 3, 5]:
                for comb in combinations(sortedHand, clen):
                    comb = list(comb)
                    is_valid, strength, trick_type, reason = validate_trick_and_get_strength(comb)
                    if not is_valid or trick_type == TrickType.PASS:
                        continue
                    score = strength + trick_type.value * 10 ** 20
                    valid_tricks.append((score, comb))
            valid_tricks.sort(key=lambda x: x[0], reverse=True)
            if len(valid_tricks) != 0:
                action = valid_tricks[0][1]
        else:
            t_is_valid, t_strength, t_trick_type, t_reason = validate_trick_and_get_strength(state.toBeat.cards)
            assert t_is_valid
            card_size = len(state.toBeat.cards)

            valid_tricks = []
            for comb in combinations(sortedHand, card_size):
                comb = list(comb)
                is_valid, strength, trick_type, reason = validate_trick_and_get_strength(comb)
                if not is_valid or trick_type == TrickType.PASS:
                    continue
                is_type_stronger = card_size == 5 and trick_type.value > t_trick_type.value
                if is_type_stronger:
                    score = strength + trick_type.value * 10 ** 20
                    valid_tricks.append((score, comb))
                    break
                if trick_type != t_trick_type or t_strength > strength:
                    continue
                score = strength + trick_type.value * 10 ** 20
                valid_tricks.append((score, comb))

            valid_tricks.sort(key=lambda x: x[0], reverse=True)
            if len(valid_tricks) != 0:
                action = valid_tricks[0][1]


        return action, myData
