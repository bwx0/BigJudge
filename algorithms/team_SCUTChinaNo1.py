from collections import Counter

from classes import *
from itertools import combinations, product
from typing import List, Dict, Tuple, Optional
from collections import Counter


class Algorithm:

    def getStrength(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        return ranks.index(card[0]) * 4 + suits.index(card[1])

    def getCard(self, strength: int) -> str:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        rank = ranks[strength // 4]
        suit = suits[strength % 4]
        return rank + suit

    def getCard_rank(self, strength: int) -> str:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        rank = ranks[strength // 4]
        return rank

    def is_flush(self, suits):

        return len(set(suits)) == 1

    def is_straight(self, ranks):

        rank_values = [self.rank_to_value(rank) for rank in ranks]
        rank_values.sort()

        return rank_values == list(range(min(rank_values), min(rank_values) + len(rank_values)))

    def rank_to_value(self, rank):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        return ranks.index(rank) + 1

    def extract_three_of_a_kind(self, rank_count):

        for rank, count in rank_count.items():
            if count == 3:
                return self.rank_to_value(rank)
        return None

    def extract_four_of_a_kind(self, rank_count):

        for rank, count in rank_count.items():
            if count == 4:
                return self.rank_to_value(rank)
        return None

    def is_any_player_hand_less_than(self, state, hand_size_threshold: int) -> bool:
        for i, player in enumerate(state.players):
            if i != state.myPlayerNum:
                if player.handSize < hand_size_threshold:
                    return True
        return False

    def getAction(self, state: MatchState):
        action = []
        myData = state.myData

        find_winning_path = True
        if find_winning_path:
            hand_count = [p.handSize for i, p in enumerate(state.players) if i != state.myPlayerNum]

            wa = WinningPathFinder.find(myHand=state.myHand, othersHand=self.getRemainingCards(state), toBeat=state.toBeat,
                                        hand_cnt=hand_count)

            if wa is not None and ("3D" not in state.myHand or "3D" in wa):
                # print("Found", wa)
                return wa, myData

        original_card_num = len(state.myHand)
        if state.toBeat:
            card_num = len(state.toBeat.cards)
        else:
            card_num = 0

        myHand_ranks = []
        myHand_suits = []

        for card in state.myHand:
            rank = card[:-1]
            suit = card[-1]
            myHand_ranks.append(rank)
            myHand_suits.append(suit)

        single_card_all = []
        double_card_all = []
        triple_card_all = []
        fifth_card_straight_all = []
        fifth_card_flush_all = []
        fifth_card_straight_flush_all = []
        fifth_card_full_house_all = []
        fifth_card_four_all = []

        card_pools_all = {
            1: single_card_all,
            2: double_card_all,
            3: triple_card_all,
            4: fifth_card_straight_all,
            5: fifth_card_flush_all,
            6: fifth_card_straight_flush_all,
            7: fifth_card_full_house_all,
            8: fifth_card_four_all
        }

        card_pools_all = allHandOperator(state.myHand, myHand_ranks, myHand_suits, card_pools_all).allHand()

        is_3d_exist = 1
        single_card = []
        double_card = []
        triple_card = []

        card_pools_best = {
            1: single_card,
            2: double_card,
            3: triple_card,
            4: fifth_card_straight_all,
            5: fifth_card_flush_all,
            6: fifth_card_full_house_all,
            7: fifth_card_four_all,
            8: fifth_card_straight_flush_all,
        }

        card_pools_best = bestHandOperator(state.myHand, myHand_ranks, myHand_suits, card_pools_best).bestHand()

        split_threshold = 8
        no_card_threshold = 3
        difference_threshold = 28
        large_card_threshold = 28
        my_no_card_threshold = 6
        opponent_no_card_threshold = 6

        if state.toBeat is None and original_card_num == 13:
            action = []

            target_strength = 0
            found = False

            for pool_key, pool_cards in card_pools_best.items():
                for card_group in pool_cards:
                    if target_strength in card_group:
                        action.extend([self.getCard(card) for card in card_group])
                        found = True
                        break
                if found:
                    break

        elif state.toBeat is None:
            action = []
            # found = False

            for pool_key in range(8, 0, -1):
                if card_pools_best[pool_key]:
                    if (pool_key <= 3):
                        action.extend([self.getCard(card) for card in card_pools_best[pool_key][0]])
                        break
                    else:
                        action.extend(
                            [self.getCard(card) for card in card_pools_best[pool_key][len(card_pools_best[pool_key]) - 1]])
                        break

            # for pool_key in range(8, 0, -1):
            #     if card_pools_best[pool_key]:
            #         if (pool_key <= 3):
            #             if original_card_num <= my_no_card_threshold or self.is_any_player_hand_less_than(state, opponent_no_card_threshold):
            #                 card_pools_length = len(card_pools_best[pool_key])
            #                 card_set_length = len(card_pools_best[pool_key][0])
            #                 if card_pools_best[pool_key][card_pools_length - 1][card_set_length - 1] >= large_card_threshold:
            #                     action.extend([self.getCard(card) for card in card_pools_best[pool_key][card_pools_length - 1]])
            #                     found = True
            #                     break
            #             else:
            #                 action.extend([self.getCard(card) for card in card_pools_best[pool_key][0]])
            #                 found = True
            #                 break
            #         else:
            #             action.extend([self.getCard(card) for card in
            #                            card_pools_best[pool_key][len(card_pools_best[pool_key]) - 1]])
            #             found = True
            #             break
            #
            # if not found:
            #     for pool_key in range(3, 0, -1):
            #         if card_pools_best[pool_key]:
            #             if original_card_num <= my_no_card_threshold or self.is_any_player_hand_less_than(state, opponent_no_card_threshold):
            #                 card_pools_length = len(card_pools_best[pool_key])
            #                 action.extend([self.getCard(card) for card in card_pools_best[pool_key][card_pools_length - 1]])
            #                 break
            #             else:
            #                 action.extend([self.getCard(card) for card in card_pools_best[pool_key][0]])
            #                 break



        elif card_num == 1:
            cardToBeat_strength = self.getStrength(state.toBeat.cards[0])
            found = False

            for single in single_card:
                if single[0] > cardToBeat_strength:
                    if len(single_card) == 1:
                        action.extend([self.getCard(single[0])])
                        found = True
                        break

                    strength_diff = single[0] - cardToBeat_strength

                    if strength_diff <= difference_threshold:
                        action.extend([self.getCard(single[0])])
                        found = True
                        break

                    elif strength_diff > difference_threshold and state.players[
                        state.toBeat.playerNum].handSize <= no_card_threshold:
                        action.extend([self.getCard(single[0])])
                        found = True
                        break

            if not found:
                if state.players[state.toBeat.playerNum].handSize <= split_threshold:
                    for single in single_card_all:
                        if single[0] > cardToBeat_strength:

                            strength_diff = single[0] - cardToBeat_strength

                            if strength_diff <= difference_threshold:
                                action.extend([self.getCard(single[0])])
                                break

                            elif strength_diff > difference_threshold and state.players[
                                state.toBeat.playerNum].handSize <= no_card_threshold:
                                action.extend([self.getCard(single[0])])
                                break

        elif card_num == 2:
            sorted_cards = sorted(state.toBeat.cards)
            cardToBeat_strength = self.getStrength(sorted_cards[1])

            found = False

            for double in double_card:
                if double[1] > cardToBeat_strength:
                    if len(double_card) == 1:
                        action.extend([self.getCard(double[0]), self.getCard(double[1])])
                        found = True
                        break

                    strength_diff = double[1] - cardToBeat_strength

                    if strength_diff <= difference_threshold:
                        action.extend([self.getCard(double[0]), self.getCard(double[1])])
                        found = True
                        break

                    elif strength_diff > difference_threshold and state.players[
                        state.toBeat.playerNum].handSize <= no_card_threshold:
                        action.extend([self.getCard(double[0]), self.getCard(double[1])])
                        found = True
                        break

            if not found:
                if state.players[state.toBeat.playerNum].handSize <= split_threshold:
                    for double in double_card_all:
                        if double[1] > cardToBeat_strength:

                            strength_diff = double[1] - cardToBeat_strength

                            if strength_diff <= difference_threshold:
                                action.extend([self.getCard(double[0]), self.getCard(double[1])])
                                break

                            elif strength_diff > difference_threshold and state.players[
                                state.toBeat.playerNum].handSize <= no_card_threshold:
                                action.extend([self.getCard(double[0]), self.getCard(double[1])])
                                break

        elif card_num == 3:
            cardToBeat_strength = self.getStrength(state.toBeat.cards[0])
            found = False

            for triple in triple_card:
                if triple[0] > cardToBeat_strength:
                    if len(triple_card) == 1:
                        action.extend([self.getCard(triple[0]), self.getCard(triple[1]), self.getCard(triple[2])])
                        found = True
                        break

                    strength_diff = triple[0] - cardToBeat_strength

                    if strength_diff <= difference_threshold:
                        action.extend([self.getCard(triple[0]), self.getCard(triple[1]), self.getCard(triple[2])])
                        found = True
                        break

                    elif strength_diff > difference_threshold and state.players[
                        state.toBeat.playerNum].handSize <= no_card_threshold:
                        action.extend([self.getCard(triple[0]), self.getCard(triple[1]), self.getCard(triple[2])])
                        found = True
                        break

            if not found:
                if state.players[state.toBeat.playerNum].handSize <= split_threshold:
                    for triple in triple_card_all:
                        if triple[0] > cardToBeat_strength:

                            strength_diff = triple[0] - cardToBeat_strength

                            if strength_diff <= difference_threshold:
                                action.extend(
                                    [self.getCard(triple[0]), self.getCard(triple[1]), self.getCard(triple[2])])
                                break

                            elif strength_diff > difference_threshold and state.players[
                                state.toBeat.playerNum].handSize <= no_card_threshold:
                                action.extend(
                                    [self.getCard(triple[0]), self.getCard(triple[1]), self.getCard(triple[2])])
                                break

        elif card_num == 5:
            cardToBeat = state.toBeat.cards
            cardToBeat_strength = [self.getStrength(card) for card in cardToBeat]
            cardToBeat_strength.sort()
            cardToBeat_ranks = []
            cardToBeat_suits = []
            for card in cardToBeat:
                rank = card[:-1]
                suit = card[-1]
                cardToBeat_ranks.append(rank)
                cardToBeat_suits.append(suit)
            rank_count = Counter(cardToBeat_ranks)
            if 4 in rank_count.values():
                cardToBeat_type = 4
            elif 3 in rank_count.values():
                cardToBeat_type = 3
            elif self.is_flush(cardToBeat_suits):
                if self.is_straight(cardToBeat_ranks):
                    cardToBeat_type = 5
                else:
                    cardToBeat_type = 2
            else:
                cardToBeat_type = 1

            found = False

            if cardToBeat_type == 1:
                for card in card_pools_best[4]:
                    if card[4] > cardToBeat_strength[4]:
                        action.extend([self.getCard(strength) for strength in card])
                        found = True
                        break
                if not found:
                    for card_pool in [card_pools_best[5], card_pools_best[6], card_pools_best[7],
                                      card_pools_best[8]]:
                        if len(card_pool) == 1:
                            action.extend([self.getCard(strength) for strength in card_pool[0]])
                            break
                        elif len(card_pool) == 2:
                            action.extend([self.getCard(strength) for strength in card_pool[1]])
                            break
            elif cardToBeat_type == 2:
                for card_set in card_pools_best[5]:
                    ranks = []
                    for card in card_set:
                        ranks.append(self.getCard_rank(card))
                    rank_values = [self.rank_to_value(rank) for rank in ranks]
                    rank_values.sort(reverse=True)
                    cardToBeat_ranks_values = [self.rank_to_value(rank) for rank in cardToBeat_ranks]
                    cardToBeat_ranks_values.sort(reverse=True)
                    if rank_values > cardToBeat_ranks_values:
                        action.extend([self.getCard(strength) for strength in card_set])
                        found = True
                        break
                    elif rank_values == cardToBeat_ranks_values:
                        if card_set[0] > cardToBeat_strength[0]:
                            action.extend([self.getCard(strength) for strength in card_set])
                            found = True
                            break
                if not found:
                    for card_pool in [card_pools_best[6], card_pools_best[7],
                                      card_pools_best[8]]:
                        if len(card_pool) == 1:
                            action.extend([self.getCard(strength) for strength in card_pool[0]])
                            break
                        elif len(card_pool) == 2:
                            action.extend([self.getCard(strength) for strength in card_pool[1]])
                            break
            elif cardToBeat_type == 3:
                for card_set in card_pools_best[6]:
                    ranks = []
                    for card in card_set:
                        ranks.append(self.getCard_rank(card))
                    card_rank_count = Counter(ranks)
                    card_three_of_a_kind = self.extract_three_of_a_kind(card_rank_count)
                    cardToBeat_three_of_a_kind = self.extract_three_of_a_kind(rank_count)
                    if card_three_of_a_kind > cardToBeat_three_of_a_kind:
                        action.extend([self.getCard(strength) for strength in card_set])
                        found = True
                        break
                if not found:
                    for card_pool in [card_pools_best[7], card_pools_best[8]]:
                        if len(card_pool) == 1:
                            action.extend([self.getCard(strength) for strength in card_pool[0]])
                            break
                        elif len(card_pool) == 2:
                            action.extend([self.getCard(strength) for strength in card_pool[1]])
                            break
            elif cardToBeat_type == 4:
                for card_set in card_pools_best[7]:
                    ranks = []
                    for card in card_set:
                        ranks.append(self.getCard_rank(card))
                    card_rank_count = Counter(ranks)
                    card_four_of_a_kind = self.extract_four_of_a_kind(card_rank_count)
                    cardToBeat_four_of_a_kind = self.extract_four_of_a_kind(rank_count)
                    if card_four_of_a_kind > cardToBeat_four_of_a_kind:
                        action.extend([self.getCard(strength) for strength in card_set])
                        found = True
                        break
                if not found:
                    card_pool = card_pools_best[8]
                    if len(card_pool) == 1:
                        action.extend([self.getCard(strength) for strength in card_pool[0]])
                    elif len(card_pool) == 2:
                        action.extend([self.getCard(strength) for strength in card_pool[1]])
            else:
                for card in card_pools_best[8]:
                    if card[4] > cardToBeat_strength[4]:
                        action.extend([self.getCard(strength) for strength in card])
                        break

        return action, myData

    def getRemainingCards(self, state: MatchState):
        result = all_cards.copy()
        for card in state.myHand:
            result.remove(card)
        for tricks in state.matchHistory[-1].gameHistory:
            for trick in tricks:
                for card in trick.cards:
                    result.remove(card)
        return result


class allHandOperator:
    def __init__(self, myHand: List[str], ranks: List[str], suits: List[str],
                 card_pools_all: Dict[int, List[List[int]]]):
        self.card_pools_all = card_pools_all
        self.ranks = ranks
        self.suits = suits
        self.myHand = myHand
        self.rank_counter = Counter(self.ranks)
        self.suit_counter = Counter(self.suits)

    def getStrength(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        return ranks.index(card[0]) * 4 + suits.index(card[1])

    def getCard(self, strength: int) -> str:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        rank = ranks[strength // 4]
        suit = suits[strength % 4]
        return rank + suit

    def getStrength_straght(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        return ranks.index(card[0])

    def getCard_straght(self, index: int) -> str:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        return ranks[index]

    def compare_flush(self, flush1: List[int], flush2: List[int]) -> int:
        rank_order = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11,
                      '2': 12}

        suit_order = {'D': 0, 'C': 1, 'H': 2, 'S': 3}
        flush1_original = [self.getCard(card) for card in flush1]
        flush2_original = [self.getCard(card) for card in flush2]
        sorted_flush1 = sorted(flush1_original, key=lambda card: (rank_order[card[0]], suit_order[card[1]]),
                               reverse=True)
        sorted_flush2 = sorted(flush2_original, key=lambda card: (rank_order[card[0]], suit_order[card[1]]),
                               reverse=True)

        for card1, card2 in zip(sorted_flush1, sorted_flush2):
            if rank_order[card1[0]] > rank_order[card2[0]]:
                return 1
            elif rank_order[card1[0]] < rank_order[card2[0]]:
                return -1
            if suit_order[card1[1]] > suit_order[card2[1]]:
                return 1
            elif suit_order[card1[1]] < suit_order[card2[1]]:
                return -1

        return 0

    def listCombo(self, index_of_type: int, r: int, rank: str):
        pair_strength = [self.getStrength(card) for card in self.myHand if card[0] == rank]
        pair_strength.sort()
        for combo in combinations(pair_strength, r):
            self.card_pools_all[index_of_type].append(list(combo))

    def remove_cards(self, cards_to_remove: List[str]):
        for card in cards_to_remove:
            if card in self.myHand:
                self.myHand.remove(card)
                self.ranks.remove(card[0])
                self.suits.remove(card[1])
        self.rank_counter = Counter(self.ranks)
        self.suit_counter = Counter(self.suits)

    def add_cards(self, cards_to_add: List[str]):
        for card in cards_to_add:
            self.myHand.append(card)
            self.ranks.append(card[0])
            self.suits.append(card[1])
        self.rank_counter = Counter(self.ranks)
        self.suit_counter = Counter(self.suits)

    def allHand(self) -> Dict[int, List[List[int]]]:
        self.card_pools_all[1].extend([[self.getStrength(card)] for card in self.myHand])
        self.card_pools_all[1].sort()

        sorted_rank_counter = sorted(self.rank_counter.items(), key=lambda x: self.getStrength_straght(x))
        self.rank_counter = Counter(dict(sorted_rank_counter))
        for rank, count in self.rank_counter.items():
            if count == 2:
                self.listCombo(2, 2, rank)
            elif count == 3:
                self.listCombo(2, 2, rank)
                self.listCombo(3, 3, rank)
            elif count == 4:
                self.listCombo(2, 2, rank)
                self.listCombo(3, 3, rank)

        count_for_five = 0

        for suit, count in self.suit_counter.items():
            if count >= 5:
                suit_cards = [card for card in self.myHand if card[1] == suit]
                suit_ranks_sorted = sorted(suit_cards, key=lambda x: self.getStrength(x))
                for i in range(len(suit_ranks_sorted) - 1, 3, -1):
                    straight_flush = suit_ranks_sorted[i - 4:i + 1]
                    if all(self.getStrength(straight_flush[j]) + 4 == self.getStrength(straight_flush[j + 1]) for j in
                           range(4)):
                        self.card_pools_all[6].append([self.getStrength(card) for card in straight_flush])
                        count_for_five += 1
                        self.remove_cards(straight_flush)
                        if count_for_five >= 2:
                            if self.card_pools_all[6][0][4] < self.card_pools_all[6][1][4]:
                                self.card_pools_all[6][0], self.card_pools_all[6][1] = self.card_pools_all[6][1], \
                                    self.card_pools_all[6][0]
                            return self.card_pools_all

        count_for_four = 0
        for rank, count in self.rank_counter.items():
            if count == 4:
                four_cards = [card for card in self.myHand if card[0] == rank]
                four_cards = sorted(four_cards, key=lambda x: self.getStrength(x))
                self.card_pools_all[8].append(
                    [self.getStrength(card) for card in four_cards])
                count_for_four += 1
                if count_for_four == 2:
                    if self.card_pools_all[8][0][3] < self.card_pools_all[8][1][3]:
                        self.card_pools_all[8][0], self.card_pools_all[8][1] = self.card_pools_all[8][1], \
                            self.card_pools_all[8][0]
                elif count_for_four == 3:
                    if self.card_pools_all[8][1][3] > self.card_pools_all[8][2][3]:
                        del self.card_pools_all[8][2]
                    else:
                        del self.card_pools_all[8][1]

        if count_for_four == 1:
            self.remove_cards([self.getCard(card) for card in self.card_pools_all[8][0]])
        elif count_for_four >= 2:
            self.remove_cards([self.getCard(card) for card in self.card_pools_all[8][0]] +
                              [self.getCard(card) for card in self.card_pools_all[8][1]])

        for i in range(len(self.card_pools_all[8])):
            single_card_candidates = [card for card in self.myHand if self.rank_counter[card[0]] == 1]
            if self.rank_counter:
                if single_card_candidates:
                    single_card = min(single_card_candidates, key=lambda x: self.getStrength(x))
                else:
                    min_count = min(self.rank_counter.values())

                    smallest_group_cards = [card for card in self.myHand if self.rank_counter[card[0]] == min_count]

                    single_card = min(smallest_group_cards, key=lambda x: self.getStrength(x))
                self.card_pools_all[8][i].extend([self.getStrength(single_card)])
                count_for_five += 1
                self.remove_cards([self.getCard(card) for card in self.card_pools_all[8][i]])

            else:
                if len(self.card_pools_all[8]) == 1:
                    self.add_cards([self.getCard(card) for card in self.card_pools_all[8][0]])
                    del self.card_pools_all[8][0]
                elif i == 0:
                    self.card_pools_all[8][i].extend([self.card_pools_all[8][i + 1][0]])
                    self.add_cards([self.getCard(card) for card in self.card_pools_all[8][i + 1][-3:]])
                    del self.card_pools_all[8][i + 1]
                    count_for_five += 1
                    break
                else:
                    self.add_cards([self.getCard(card) for card in self.card_pools_all[8][i]])
                    del self.card_pools_all[8][i]
                    break
        if count_for_five >= 2:
            return self.card_pools_all

        count_for_three = 0
        for rank, count in self.rank_counter.items():
            if count == 3:
                triple_cards = [card for card in self.myHand if card[0] == rank]
                triple_cards = sorted(triple_cards, key=lambda x: self.getStrength(x))
                self.card_pools_all[7].append(
                    [self.getStrength(card) for card in triple_cards])
                count_for_three += 1
                if count_for_three == 2:
                    if self.card_pools_all[7][0][2] < self.card_pools_all[7][1][2]:
                        self.card_pools_all[7][0], self.card_pools_all[7][1] = self.card_pools_all[7][1], \
                            self.card_pools_all[7][0]
                elif count_for_three >= 3:
                    if self.card_pools_all[7][1][2] > self.card_pools_all[7][2][2]:
                        del self.card_pools_all[7][2]
                    else:
                        del self.card_pools_all[7][1]

        if count_for_three == 1:
            self.remove_cards([self.getCard(card) for card in self.card_pools_all[7][0]])
        elif count_for_three >= 2:
            self.remove_cards([self.getCard(card) for card in self.card_pools_all[7][0]] +
                              [self.getCard(card) for card in self.card_pools_all[7][1]])

        for i in range(len(self.card_pools_all[7])):
            smallest_pair_rank = [rank2 for rank2, count2 in self.rank_counter.items() if count2 >= 2]
            if smallest_pair_rank:
                smallest_pair_rank = self.getCard_straght(
                    min([self.getStrength_straght(card) for card in smallest_pair_rank]))

            pair_cards = sorted([card for card in self.myHand if card[0] == smallest_pair_rank],
                                key=lambda x: self.getStrength(x))[:2]
            if pair_cards:
                self.card_pools_all[7][i].extend([self.getStrength(card) for card in pair_cards])
                count_for_five += 1
                self.remove_cards(pair_cards)

            elif count_for_three == 1:
                self.add_cards([self.getCard(card) for card in self.card_pools_all[7][0]])
                del self.card_pools_all[7][0]
            elif count_for_three >= 2:
                if len(self.card_pools_all[7][0]) == 5:
                    self.add_cards([self.getCard(card) for card in self.card_pools_all[7][1]])
                else:
                    self.card_pools_all[7][0].extend([card for card in self.card_pools_all[7][1][:2]])
                    self.add_cards([self.getCard(self.card_pools_all[7][1][2])])
                del self.card_pools_all[7][1]
                break

        if count_for_five >= 2:
            return self.card_pools_all

        count_for_flush = 0
        for suit, count in self.suit_counter.items():
            if count >= 5:
                flush_cards = [card for card in self.myHand if card[1] == suit]
                flush_cards_sorted = sorted(flush_cards, key=lambda x: self.getStrength(x))
                self.card_pools_all[5].append(sorted([self.getStrength(card) for card in flush_cards_sorted])[-5:])
                count_for_flush += 1
                count_for_five += 1
                self.remove_cards(flush_cards_sorted[-5:])
                if count_for_five >= 2 and count_for_flush == 2:
                    if self.compare_flush(self.card_pools_all[5][0], self.card_pools_all[5][1]) == -1:
                        self.card_pools_all[5][0], self.card_pools_all[5][1] = self.card_pools_all[5][1], \
                            self.card_pools_all[5][0]
                    return self.card_pools_all
                else:
                    return self.card_pools_all

        isFindStraight = True
        while isFindStraight:
            remaining_strength_sorted = sorted(self.myHand, key=lambda x: self.getStrength(x))

            seen_ranks = set()

            unique_rank_cards = []
            for card in remaining_strength_sorted:
                if card[0] not in seen_ranks:
                    unique_rank_cards.append(card)
                    seen_ranks.add(card[0])
            cnt = 0
            for i in range(len(unique_rank_cards) - 1, 3, -1):
                straight = [self.getStrength_straght(card) for card in unique_rank_cards[i - 4:i + 1]]
                if all(straight[j] + 1 == straight[j + 1] for j in range(4)):
                    full_straight_cards = []
                    for card in unique_rank_cards[i - 4:i + 1]:
                        same_rank_cards = [orig_card for orig_card in self.myHand if orig_card[0] == card[0]]
                        full_straight_cards.append(max(same_rank_cards, key=lambda x: self.getStrength(x)))
                    self.card_pools_all[4].append([self.getStrength(card) for card in full_straight_cards])
                    self.remove_cards(full_straight_cards)
                    cnt += 1
                    if count_for_five >= 2:
                        return self.card_pools_all
                    break
            if cnt == 0: isFindStraight = False

        return self.card_pools_all


class bestHandOperator:
    def __init__(self, myHand: List[str], ranks: List[str], suits: List[str],
                 card_pools_best: Dict[int, List[List[int]]]):
        self.card_pools_best = card_pools_best
        self.ranks = ranks
        self.suits = suits
        self.myHand = myHand
        self.rank_counter = Counter(self.ranks)
        self.suit_counter = Counter(self.suits)

    # Calculates the relative strength of a single card as a number to be used with Python's key comparison mechanism
    def getStrength(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        return ranks.index(card[0]) * 4 + suits.index(card[1])

    def getCard(self, strength: int) -> str:
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        rank = ranks[strength // 4]
        suit = suits[strength % 4]
        return rank + suit

    def remove_best_hand_cards(self):
        for idx in range(4, 9):
            if idx in self.card_pools_best:
                for card_group in self.card_pools_best[idx]:
                    for card in card_group:
                        if card in self.myHand:
                            self.myHand.remove(self.getCard(card))
        self.ranks = []
        self.suits = []
        for card in self.myHand:
            rank = card[:-1]
            suit = card[-1]
            self.ranks.append(rank)
            self.suits.append(suit)
        self.rank_counter = Counter(self.ranks)
        self.suit_counter = Counter(self.suits)

    def remove_cards(self, cards_to_remove: List[str]):
        for card in cards_to_remove:
            if card in self.myHand:
                self.myHand.remove(card)
                self.ranks.remove(card[0])
                self.suits.remove(card[1])
        self.rank_counter = Counter(self.ranks)
        self.suit_counter = Counter(self.suits)

    def listCombo(self, index_of_type: int, rank: str):
        pair_strength = [self.getStrength(card) for card in self.myHand if card[0] == rank]
        pair_strength.sort()
        self.card_pools_best[index_of_type].append(pair_strength)
        self.remove_cards([card for card in self.myHand if card[0] == rank])

    def getStrength_straght(self, card: str):
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        return ranks.index(card[0])

    def bestHand(self) -> Dict[int, List[List[int]]]:

        self.myHand = sorted(self.myHand, key=lambda x: self.getStrength(x))
        self.remove_best_hand_cards()

        sorted_rank_counter = sorted(self.rank_counter.items(), key=lambda x: self.getStrength_straght(x))
        self.rank_counter = Counter(dict(sorted_rank_counter))

        for rank, count in self.rank_counter.items():
            if count == 3:
                self.listCombo(3, rank)
            elif count == 2:
                self.listCombo(2, rank)
            elif count == 4:
                count_4 = [self.getStrength(card) for card in self.myHand if card[0] == rank]
                count_4.sort()
                self.card_pools_best[3].append(count_4[:3])
                self.card_pools_best[1].append([count_4[3]])
                self.remove_cards([card for card in self.myHand if card[0] == rank])
            else:
                self.listCombo(1, rank)

        return self.card_pools_best


class DLX:
    def __init__(self, w):
        self.W = w
        self.H = 0
        self.ncnt = 0
        self.L = []
        self.R = []
        self.U = []
        self.D = []
        self.cnt = [0] * (self.W + 1)
        self.col = []
        self.row = []
        self.ans = [0]
        self.__init()

    def __init(self):
        self.L = list(range(-1, self.W))
        self.R = list(range(1, self.W + 2))
        self.U = list(range(self.W + 1))
        self.D = list(range(self.W + 1))
        self.col = [0] * (self.W + 1)
        self.row = [0] * (self.W + 1)
        self.R[self.W] = 0
        self.L[0] = self.W
        self.ncnt = self.W + 1

    # 1-based index
    def add_row(self, col_idx: List[int]):
        if len(col_idx) == 0:
            return
        self.H += 1
        first = self.ncnt
        for c in col_idx:
            self.L.append(self.ncnt - 1)
            self.R.append(self.ncnt + 1)
            self.D.append(c)
            self.U.append(self.U[c])
            self.D[self.U[c]] = self.ncnt
            self.U[c] = self.ncnt
            self.col.append(c)
            self.row.append(self.H)
            self.cnt[c] += 1
            self.ncnt += 1
            self.ans.append(0)
        self.L[first] = self.ncnt - 1
        self.R[self.ncnt - 1] = first

    def add_row_01(self, lst: List[int]):
        self.add_row([i for i, v in enumerate(lst, start=1) if v > 0])

    # 0-based index
    def add_row_0b(self, lst: List[int]):
        self.add_row([i + 1 for i in lst])

    def __remove(self, c):
        self.R[self.L[c]] = self.R[c]
        self.L[self.R[c]] = self.L[c]
        i = self.D[c]
        while i != c:
            j = self.L[i]
            while j != i:
                self.D[self.U[j]] = self.D[j]
                self.U[self.D[j]] = self.U[j]
                self.cnt[self.col[j]] -= 1
                j = self.L[j]
            i = self.D[i]

    def __restore(self, c):
        self.R[self.L[c]] = c
        self.L[self.R[c]] = c
        i = self.D[c]
        while i != c:
            j = self.L[i]
            while j != i:
                self.D[self.U[j]] = j
                self.U[self.D[j]] = j
                self.cnt[self.col[j]] += 1
                j = self.L[j]
            i = self.D[i]

    def __dance(self, depth=0):
        if self.R[0] == 0:
            return True
        c = self.R[0]
        i = self.R[0]
        while i != 0:
            if self.cnt[i] < self.cnt[c]:
                c = i
            i = self.R[i]
        self.__remove(c)
        i = self.D[c]
        while i != c:
            self.ans[self.ans[0] + 1] = self.row[i]
            self.ans[0] += 1
            j = self.R[i]
            while j != i:
                self.__remove(self.col[j])
                j = self.R[j]
            if self.__dance(depth + 1):
                return True
            j = self.L[i]
            while j != i:
                self.__restore(self.col[j])
                j = self.L[j]
            self.ans[0] -= 1
            i = self.D[i]
        self.__restore(c)
        return False

    def run(self):
        self.__dance()
        return sorted(self.ans[1:self.ans[0] + 1])


RANKS = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
SUITS = ['D', 'C', 'H', 'S']
all_cards = [rank + suit for rank in RANKS for suit in SUITS]


def get_strength(card: str) -> int:
    return RANKS.index(card[0]) * 4 + SUITS.index(card[1])


def get_strength_by_value(rank: int, suit: int) -> int:
    return rank * 4 + suit


def get_card_by_value(rank: int, suit: int) -> str:
    return RANKS[rank] + SUITS[suit]


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


class TrickType:
    PASS: 'TrickType' = 0
    SINGLE: 'TrickType' = 1
    PAIR: 'TrickType' = 2
    TRIPLET: 'TrickType' = 3
    STRAIGHT: 'TrickType' = 4
    FLUSH: 'TrickType' = 5
    FULL_HOUSE: 'TrickType' = 6
    FOUR_OF_A_KIND: 'TrickType' = 7
    STRAIGHT_FLUSH: 'TrickType' = 8
    PLACEHOLDER_5CARDS: 'TrickType' = 9

    def __init__(self, value: int):
        self.value = value


# Enum workaround
TrickType.PASS = TrickType(TrickType.PASS)
TrickType.SINGLE = TrickType(TrickType.SINGLE)
TrickType.PAIR = TrickType(TrickType.PAIR)
TrickType.TRIPLET = TrickType(TrickType.TRIPLET)
TrickType.STRAIGHT = TrickType(TrickType.STRAIGHT)
TrickType.FLUSH = TrickType(TrickType.FLUSH)
TrickType.FULL_HOUSE = TrickType(TrickType.FULL_HOUSE)
TrickType.FOUR_OF_A_KIND = TrickType(TrickType.FOUR_OF_A_KIND)
TrickType.STRAIGHT_FLUSH = TrickType(TrickType.STRAIGHT_FLUSH)
TrickType.PLACEHOLDER_5CARDS = TrickType(TrickType.PLACEHOLDER_5CARDS)


class ComboFinder:
    _5_CARDS_TRICKS = [
        TrickType.STRAIGHT,
        TrickType.FLUSH,
        TrickType.FULL_HOUSE,
        TrickType.FOUR_OF_A_KIND,
        TrickType.STRAIGHT_FLUSH
    ]

    @staticmethod
    def typed_strength(trick_type: TrickType, strength: int) -> int:
        return trick_type.value * 10 ** 20 + strength

    # Copied from Big2Judge
    @staticmethod
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

    @staticmethod
    def get_typed_trick_strength(action: List[str]):
        is_valid, strength, trick_type, reason = ComboFinder.validate_trick_and_get_strength(action)
        if not is_valid:
            raise Exception()
        return ComboFinder.typed_strength(trick_type, strength)

    @staticmethod
    def group_cards(cards: List[str]) -> Tuple[Dict[int, List[int]], Dict[int, List[int]]]:
        rank_group: Dict[int, List[int]] = {i: [] for i in range(13)}
        suit_group: Dict[int, List[int]] = {i: [] for i in range(4)}

        for card in cards:
            rank = RANKS.index(card[0])
            suit = SUITS.index(card[1])
            rank_group[rank].append(suit)
            suit_group[suit].append(rank)

        for i in range(13):
            rank_group[i].sort()

        for i in range(4):
            suit_group[i].sort()

        return rank_group, suit_group

    @staticmethod
    def find_best_combo_slow(cards: List[str]) -> Dict[TrickType, int]:
        """
        List all possible combinations
        Note: STRAIGHT and FLUSH are overridden by STRAIGHT_FLUSH if STRAIGHT_FLUSH is present
        :param cards:
        :return:
        """
        result: Dict[TrickType, int] = {
            TrickType.SINGLE: 0,
            TrickType.PAIR: 0,
            TrickType.TRIPLET: 0,
            TrickType.STRAIGHT: 0,
            TrickType.FLUSH: 0,
            TrickType.FULL_HOUSE: 0,
            TrickType.FOUR_OF_A_KIND: 0,
            TrickType.STRAIGHT_FLUSH: 0,
            TrickType.PLACEHOLDER_5CARDS: 0
        }

        cards.sort(key=get_strength)

        for clen in [1, 2, 3, 5]:
            for comb in combinations(cards, clen):
                comb = list(comb)
                is_valid, strength, trick_type, reason = ComboFinder.validate_trick_and_get_strength(comb)
                if not is_valid or trick_type == TrickType.PASS:
                    continue
                result[trick_type] = max(result[trick_type], strength)

        if result[TrickType.STRAIGHT_FLUSH] > 0:
            result[TrickType.STRAIGHT] = result[TrickType.STRAIGHT_FLUSH]
            result[TrickType.FLUSH] = result[TrickType.STRAIGHT_FLUSH]

        # Typed strength
        result[TrickType.SINGLE] = ComboFinder.typed_strength(TrickType.SINGLE, result[TrickType.SINGLE])
        result[TrickType.PAIR] = ComboFinder.typed_strength(TrickType.PAIR, result[TrickType.PAIR])
        result[TrickType.TRIPLET] = ComboFinder.typed_strength(TrickType.TRIPLET, result[TrickType.TRIPLET])
        for trick_type in ComboFinder._5_CARDS_TRICKS:
            result[TrickType.PLACEHOLDER_5CARDS] = max(
                result[TrickType.PLACEHOLDER_5CARDS],
                ComboFinder.typed_strength(trick_type, result[trick_type])
            )

        return result

    @staticmethod
    def find_best_combo(cards: List[str]) -> Dict[TrickType, int]:
        """
        Note: STRAIGHT and FLUSH are overridden by STRAIGHT_FLUSH if STRAIGHT_FLUSH is present
        :param cards:
        :return: {Trick type, highest strength}
        """
        result: Dict[TrickType, int] = {
            TrickType.SINGLE: 0,
            TrickType.PAIR: 0,
            TrickType.TRIPLET: 0,
            TrickType.STRAIGHT: 0,
            TrickType.FLUSH: 0,
            TrickType.FULL_HOUSE: 0,
            TrickType.FOUR_OF_A_KIND: 0,
            TrickType.STRAIGHT_FLUSH: 0,
            TrickType.PLACEHOLDER_5CARDS: 0
        }

        rank_group, suit_group = ComboFinder.group_cards(cards)
        rank_group_lens = [0] * 13
        for i in range(13):
            rank_group_lens[i] = len(rank_group[i])

        # single
        for card in cards:
            result[TrickType.SINGLE] = max(result[TrickType.SINGLE], get_strength(card))

        # pair
        for rank in reversed(range(13)):
            if len(rank_group[rank]) >= 2:
                result[TrickType.PAIR] = get_strength_by_value(rank, rank_group[rank][-1])
                break

        # triplet
        for rank in reversed(range(13)):
            if len(rank_group[rank]) >= 3:
                result[TrickType.TRIPLET] = get_strength_by_value(rank, rank_group[rank][-1])
                break

        # straight
        for rank in reversed(range(4, 13)):
            if min(rank_group_lens[rank - 4:rank + 1]) > 0:
                result[TrickType.STRAIGHT] = get_strength_by_value(rank, rank_group[rank][-1])
                break

        # flush
        for suit in reversed(range(4)):
            if len(suit_group[suit]) < 5:
                continue
            cards = [get_card_by_value(rank, suit) for rank in suit_group[suit][-5:]]
            is_valid, strength, trick_type, reason = ComboFinder.validate_trick_and_get_strength(cards)
            assert is_valid
            result[TrickType.FLUSH] = max(result[TrickType.FLUSH], strength)

        # full house
        for rank3 in reversed(range(13)):
            len_r = rank_group_lens[rank3]
            if len_r < 3:
                continue

            tmp = rank_group_lens[rank3]
            rank_group_lens[rank3] = 0  # exclude current triple
            max_lens = max(rank_group_lens)
            rank_group_lens[rank3] = tmp

            if max_lens >= 2:
                result[TrickType.FULL_HOUSE] = get_strength_by_value(rank3, rank_group[rank3][-1])
                break

        # four of a kind
        for rank4 in reversed(range(13)):
            len_r = rank_group_lens[rank4]
            if len_r < 4:
                continue

            tmp = rank_group_lens[rank4]
            rank_group_lens[rank4] = 0  # exclude current 4 cards of a kind
            max_lens = max(rank_group_lens)
            rank_group_lens[rank4] = tmp

            if max_lens >= 1:
                result[TrickType.FOUR_OF_A_KIND] = get_strength_by_value(rank4, rank_group[rank4][-1])
                break

        # straight flush
        for suit in reversed(range(4)):
            for rank5 in reversed(range(4, 13)):
                if all(r in suit_group[suit] for r in range(rank5 - 4, rank5 + 1)):
                    result[TrickType.STRAIGHT_FLUSH] = max(result[TrickType.STRAIGHT_FLUSH],
                                                           get_strength_by_value(rank5, suit))
                    break

        # 5 cards
        if result[TrickType.STRAIGHT_FLUSH] > 0:
            result[TrickType.STRAIGHT] = result[TrickType.STRAIGHT_FLUSH]
            result[TrickType.FLUSH] = result[TrickType.STRAIGHT_FLUSH]

        # Typed strength
        result[TrickType.SINGLE] = ComboFinder.typed_strength(TrickType.SINGLE, result[TrickType.SINGLE])
        result[TrickType.PAIR] = ComboFinder.typed_strength(TrickType.PAIR, result[TrickType.PAIR])
        result[TrickType.TRIPLET] = ComboFinder.typed_strength(TrickType.TRIPLET, result[TrickType.TRIPLET])
        for trick_type in ComboFinder._5_CARDS_TRICKS:
            result[TrickType.PLACEHOLDER_5CARDS] = max(
                result[TrickType.PLACEHOLDER_5CARDS],
                ComboFinder.typed_strength(trick_type, result[trick_type])
            )

        return result

    @staticmethod
    def list_combos(cards: List[str]) -> Dict[TrickType, List[List[str]]]:
        """
        Note: STRAIGHT and FLUSH are overridden by STRAIGHT_FLUSH if STRAIGHT_FLUSH is present
        :param cards:
        :return: {Trick type, highest strength}
        """
        result: Dict[TrickType, List[List[str]]] = {
            TrickType.SINGLE: [],
            TrickType.PAIR: [],
            TrickType.TRIPLET: [],
            TrickType.STRAIGHT: [],
            TrickType.FLUSH: [],
            TrickType.FULL_HOUSE: [],
            TrickType.FOUR_OF_A_KIND: [],
            TrickType.STRAIGHT_FLUSH: [],
            TrickType.PLACEHOLDER_5CARDS: []
        }

        cards.sort(key=get_strength)

        rank_group, suit_group = ComboFinder.group_cards(cards)
        rank_group_lens = [0] * 13
        for i in range(13):
            rank_group_lens[i] = len(rank_group[i])

        # single
        for card in cards:
            result[TrickType.SINGLE].append([card])

        # pair
        for rank in reversed(range(13)):
            if len(rank_group[rank]) < 2:
                continue
            for comb in combinations(rank_group[rank], 2):
                result[TrickType.PAIR].append([get_card_by_value(rank, comb[0]), get_card_by_value(rank, comb[1])])

        # triplet
        for rank in reversed(range(13)):
            if len(rank_group[rank]) < 3:
                continue
            for comb in combinations(rank_group[rank], 3):
                result[TrickType.TRIPLET].append([get_card_by_value(rank, comb[0]),
                                                  get_card_by_value(rank, comb[1]),
                                                  get_card_by_value(rank, comb[2])])

        # straight
        for rank in reversed(range(4, 13)):
            for suits in product(rank_group[rank - 4], rank_group[rank - 3], rank_group[rank - 2], rank_group[rank - 1],
                                 rank_group[rank - 0]):
                s1, s2, s3, s4, s5 = suits
                result[TrickType.STRAIGHT].append([
                    get_card_by_value(rank - 4, s1),
                    get_card_by_value(rank - 3, s2),
                    get_card_by_value(rank - 2, s3),
                    get_card_by_value(rank - 1, s4),
                    get_card_by_value(rank - 0, s5)
                ])

        # flush
        for suit in reversed(range(4)):
            if len(suit_group[suit]) < 5:
                continue
            for cmb in combinations(suit_group[suit], 5):
                result[TrickType.FLUSH].append([get_card_by_value(cmb[0], suit),
                                                get_card_by_value(cmb[1], suit),
                                                get_card_by_value(cmb[2], suit),
                                                get_card_by_value(cmb[3], suit),
                                                get_card_by_value(cmb[4], suit)])

        # full house
        for rank3 in reversed(range(13)):
            len_r3 = rank_group_lens[rank3]
            if len_r3 < 3:
                continue

            for rank2 in reversed(range(13)):
                if rank2 == rank3 or rank_group_lens[rank2] < 2:
                    continue
                for scmb3 in combinations(rank_group[rank3], 3):
                    for scmb2 in combinations(rank_group[rank2], 2):
                        result[TrickType.FULL_HOUSE].append([get_card_by_value(rank3, scmb3[0]),
                                                             get_card_by_value(rank3, scmb3[1]),
                                                             get_card_by_value(rank3, scmb3[2]),
                                                             get_card_by_value(rank2, scmb2[0]),
                                                             get_card_by_value(rank2, scmb2[1])])

        # four of a kind
        for rank4 in reversed(range(13)):
            len_r = rank_group_lens[rank4]
            if len_r < 4:
                continue

            for rank1 in reversed(range(13)):
                if rank1 == rank4 or rank_group_lens[rank1] < 1:
                    continue
                for s1 in rank_group[rank1]:
                    result[TrickType.FOUR_OF_A_KIND].append([get_card_by_value(rank4, rank_group[rank4][0]),
                                                             get_card_by_value(rank4, rank_group[rank4][1]),
                                                             get_card_by_value(rank4, rank_group[rank4][2]),
                                                             get_card_by_value(rank4, rank_group[rank4][3]),
                                                             get_card_by_value(rank1, s1)])

        # straight flush
        for suit in reversed(range(4)):
            for rank5 in reversed(range(4, 13)):
                if all(r in suit_group[suit] for r in range(rank5 - 4, rank5 + 1)):
                    result[TrickType.STRAIGHT_FLUSH].append([get_card_by_value(rank5 - 4, suit),
                                                             get_card_by_value(rank5 - 3, suit),
                                                             get_card_by_value(rank5 - 2, suit),
                                                             get_card_by_value(rank5 - 1, suit),
                                                             get_card_by_value(rank5 - 0, suit)])

        # 5 cards
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.STRAIGHT])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.FLUSH])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.FULL_HOUSE])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.FOUR_OF_A_KIND])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.STRAIGHT_FLUSH])

        return result

    @staticmethod
    def list_combos_slow(cards: List[str]) -> Dict[TrickType, List[List[str]]]:
        """
        List all possible combinations
        Note: STRAIGHT and FLUSH are overridden by STRAIGHT_FLUSH if STRAIGHT_FLUSH is present
        :param cards:
        :return:
        """
        result: Dict[TrickType, List[List[str]]] = {
            TrickType.SINGLE: [],
            TrickType.PAIR: [],
            TrickType.TRIPLET: [],
            TrickType.STRAIGHT: [],
            TrickType.FLUSH: [],
            TrickType.FULL_HOUSE: [],
            TrickType.FOUR_OF_A_KIND: [],
            TrickType.STRAIGHT_FLUSH: [],
            TrickType.PLACEHOLDER_5CARDS: []
        }

        cards.sort(key=get_strength)

        for clen in [1, 2, 3, 5]:
            for comb in combinations(cards, clen):
                comb = list(comb)
                is_valid, strength, trick_type, reason = ComboFinder.validate_trick_and_get_strength(comb)
                if not is_valid or trick_type == TrickType.PASS:
                    continue
                result[trick_type].append(comb)

        # 5 cards
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.STRAIGHT])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.FLUSH])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.FULL_HOUSE])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.FOUR_OF_A_KIND])
        result[TrickType.PLACEHOLDER_5CARDS].extend(result[TrickType.STRAIGHT_FLUSH])

        result[TrickType.STRAIGHT].extend(result[TrickType.STRAIGHT_FLUSH])
        result[TrickType.FLUSH].extend(result[TrickType.STRAIGHT_FLUSH])

        return result

    @staticmethod
    def find_combo_strength_percentile(cards: List[str], percentile: Tuple[float, float, float, float]) -> Dict[
        TrickType, int]:
        assert len(percentile) == 4 and all([0 <= p <= 1 for p in percentile])

        result: Dict[TrickType, int] = {
            TrickType.SINGLE: 0,
            TrickType.PAIR: 0,
            TrickType.TRIPLET: 0,
            TrickType.STRAIGHT: 0,
            TrickType.FLUSH: 0,
            TrickType.FULL_HOUSE: 0,
            TrickType.FOUR_OF_A_KIND: 0,
            TrickType.STRAIGHT_FLUSH: 0,
            TrickType.PLACEHOLDER_5CARDS: 0
        }

        combos = ComboFinder.list_combos(cards)
        for trick_type, combos in combos.items():
            p_idx = trick_type.value - 1 if trick_type.value <= 3 else 3  # 1->0, 2->1, 3->2, 5->3
            strengths = [ComboFinder.get_typed_trick_strength(c) for c in combos] + [-1]
            strengths.sort()
            idx = int(percentile[p_idx] * (len(strengths) - 1))
            result[trick_type] = strengths[idx]

        return result


class WinningPathFinder:
    risk_zone = {
        tuple(): [],
        (1,): [1],
        (2,): [2],
        (3,): [3],
        (5,): [5],
        (1, 2): [1, 2, 3],
        (1, 3): [1, 3, 4],
        (1, 5): [1, 5, 6],
        (2, 3): [2, 3, 5],
        (2, 5): [2, 5, 7],
        (3, 5): [3, 5, 8],
        (1, 2, 3): [1, 2, 3, 4, 5, 6],
        (1, 2, 5): [1, 2, 3, 5, 6, 7, 8],
        (1, 3, 5): [1, 3, 4, 5, 6, 8, 9],
        (2, 3, 5): [2, 3, 5, 7, 8, 10],
        (1, 2, 3, 5): [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    }

    @staticmethod
    def find(myHand: List[str], othersHand: List[str], toBeat: Trick, hand_cnt: List[int], check_rz: bool = False) -> \
            Optional[List[str]]:
        myHand = sorted(myHand, key=get_strength)
        others_best_combo = ComboFinder.find_combo_strength_percentile(othersHand, (1.0, 1.0, 0.9, 0.35))
        my_combos0: Dict[TrickType, List[List[str]]] = ComboFinder.list_combos(myHand)

        # No opponent has more than x cards
        max_hand_cnt = max(hand_cnt)
        if max_hand_cnt < 5:
            others_best_combo[TrickType.PLACEHOLDER_5CARDS] = 0
        if max_hand_cnt < 3:
            others_best_combo[TrickType.TRIPLET] = 0
        if max_hand_cnt < 2:
            others_best_combo[TrickType.PAIR] = 0

        # Calculate the strength needed to beat toBeat.
        if toBeat is not None:
            to_beat_len = len(toBeat.cards)
            tb_valid, tb_strength, tb_tr_type, _ = ComboFinder.validate_trick_and_get_strength(toBeat.cards)
            assert tb_valid
            tb_t_strength = ComboFinder.typed_strength(tb_tr_type, tb_strength)
            others_best_combo[tb_tr_type] = max(others_best_combo[tb_tr_type], tb_t_strength)
            if to_beat_len == 5:
                others_best_combo[TrickType.PLACEHOLDER_5CARDS] = max(others_best_combo[TrickType.PLACEHOLDER_5CARDS],
                                                                      tb_t_strength)
        else:
            to_beat_len = 0
            tb_strength = 0
            tb_t_strength = 0

        # print(others_best_combo)
        # print(my_combos0)

        my_combos: Dict[TrickType, List[Tuple[List[int], int]]] = {TrickType.SINGLE: [], TrickType.PAIR: [],
                                                                   TrickType.TRIPLET: [], TrickType.PLACEHOLDER_5CARDS: []}
        all_combos: List[List[int]] = []  # Cards are indexed instead of using strings.

        for trick_type in [TrickType.SINGLE, TrickType.PAIR, TrickType.TRIPLET, TrickType.PLACEHOLDER_5CARDS]:
            for lst in my_combos0[trick_type]:
                idx_lst = [myHand.index(e) for e in lst]
                my_combos[trick_type].append((idx_lst, ComboFinder.get_typed_trick_strength(lst)))
                all_combos.append(idx_lst)

        cT = List[Tuple[List[int], int]]  # List[ (cards,strength) ]
        my_combos_1: cT = [(c, s) for c, s in my_combos[TrickType.SINGLE]]
        my_combos_2: cT = [(c, s) for c, s in my_combos[TrickType.PAIR]]
        my_combos_3: cT = [(c, s) for c, s in my_combos[TrickType.TRIPLET]]
        my_combos_5: cT = [(c, s) for c, s in my_combos[TrickType.PLACEHOLDER_5CARDS]]

        my_c_1_ub: List[List[int]] = [c for c, s in my_combos_1 if s > others_best_combo[TrickType.SINGLE]]
        my_c_2_ub: List[List[int]] = [c for c, s in my_combos_2 if s > others_best_combo[TrickType.PAIR]]
        my_c_3_ub: List[List[int]] = [c for c, s in my_combos_3 if s > others_best_combo[TrickType.TRIPLET]]
        my_c_5_ub: List[List[int]] = [c for c, s in my_combos_5 if s > others_best_combo[TrickType.PLACEHOLDER_5CARDS]]

        my_c_1_b: List[List[int]] = [c for c, s in my_combos_1 if s < others_best_combo[TrickType.SINGLE]]
        my_c_2_b: List[List[int]] = [c for c, s in my_combos_2 if s < others_best_combo[TrickType.PAIR]]
        my_c_3_b: List[List[int]] = [c for c, s in my_combos_3 if s < others_best_combo[TrickType.TRIPLET]]
        my_c_5_b: List[List[int]] = [c for c, s in my_combos_5 if s < others_best_combo[TrickType.PLACEHOLDER_5CARDS]]

        assert len(my_c_1_ub) + len(my_c_1_b) == len(my_combos_1)
        assert len(my_c_2_ub) + len(my_c_2_b) == len(my_combos_2)
        assert len(my_c_3_ub) + len(my_c_3_b) == len(my_combos_3)
        assert len(my_c_5_ub) + len(my_c_5_b) == len(my_combos_5)

        my_c_ub = my_c_1_ub + my_c_2_ub + my_c_3_ub + my_c_5_ub

        # print(">", len(my_combos_1), len(my_combos_2), len(my_combos_3), len(my_combos_5))
        # print(len(my_c_1_ub), len(my_c_2_ub), len(my_c_3_ub), len(my_c_5_ub))
        # print(len(my_c_1_b), len(my_c_2_b), len(my_c_3_b), len(my_c_5_b))

        # if len(my_c_1_ub) > 0 or len(my_c_2_ub) > 0 or len(my_c_3_ub) > 0 or len(my_c_5_ub):
        #    print("#" * 100)

        for c1 in my_c_1_b + [[]]:
            for c2 in my_c_2_b + [[]]:
                c12 = list(set(c1 + c2))
                if len(c12) != len(c1) + len(c2):
                    continue
                for c3 in my_c_3_b + [[]]:
                    c123 = list(set(c12 + c3))
                    if len(c123) != len(c12) + len(c3):
                        continue
                    for c5 in my_c_5_b + [[]]:
                        c1235 = set(c123 + c5)
                        if len(c1235) != len(c123) + len(c5):
                            continue

                        has_b1, has_b2, has_b3, has_b5 = len(c1) > 0, len(c2) > 0, len(c3) > 0, len(c5) > 0

                        rzk = tuple([i for i in
                                     [1 if has_b1 else 0, 2 if has_b2 else 0, 3 if has_b3 else 0, 5 if has_b5 else 0]
                                     if i > 0])
                        if check_rz:
                            if any([hc in WinningPathFinder.risk_zone[rzk] for hc in hand_cnt]):
                                # print(f"Risk")
                                continue

                        # c1235 is proposed as our beatable combos
                        # we then identify our unbeatable combos
                        ub_combos = [v for v in my_c_ub if len(set(v) & c1235) == 0]
                        cards_for_ub = list(set(range(len(myHand))) - c1235)  # ub combos can only form with these cards.
                        cards_for_ub_str = [myHand[ei] for ei in cards_for_ub]  # str version
                        assert len(cards_for_ub) + len(c1235) == len(myHand)

                        # Find a solution where unbeatable combos cover the remaining cards
                        dlx = DLX(len(cards_for_ub))
                        for i, ac_idx in enumerate(ub_combos):
                            remapped_ac = [cards_for_ub_str.index(myHand[ei]) for ei in ac_idx]
                            assert all([i >= 0 for i in remapped_ac])
                            dlx.add_row_0b(remapped_ac)
                        ans = dlx.run()

                        # No solution
                        if len(ans) == 0:
                            continue

                        # A list of id_list. index for myHand
                        ub_combos_sol = [ub_combos[xi - 1] for xi in ans]

                        has_ub_of_len = [False, False, False, False, False, False]  # has ub combo of length x
                        for ubc in ub_combos_sol:
                            has_ub_of_len[len(ubc)] = True

                        has_bbb_of_len = [False, has_b1, has_b2, has_b3, False, has_b5]  # has beatable combo of length x

                        risk_count = sum([has_bbb_of_len[x] and not has_ub_of_len[x] for x in range(6)])
                        if risk_count > 1:
                            # print("risk_count " + str(risk_count))
                            continue

                        winning_action = None

                        # Check if we need to beat toBeat
                        if toBeat is not None:
                            # Prefer beatable combos that can beat toBeat
                            my_b_rsp = [None, c1, c2, c3, None, c5][to_beat_len]
                            assert my_b_rsp is not None

                            # Calculate strength
                            my_b_rsp_str = [myHand[ei] for ei in my_b_rsp]  # string version
                            r_valid, r_strength, r_tr_type, _ = ComboFinder.validate_trick_and_get_strength(my_b_rsp_str)
                            assert r_valid
                            r_t_strength = ComboFinder.typed_strength(r_tr_type, tb_strength)

                            # Play beatable combos if possible
                            if r_t_strength > tb_t_strength:
                                winning_action = my_b_rsp_str
                            else:
                                # Otherwise play unbeatable ones
                                for ubc in ub_combos_sol:
                                    if len(ubc) == to_beat_len:
                                        winning_action = [myHand[ei] for ei in ubc]
                                        break
                        else:
                            # No tricks to beat, play beatable combos then unbeatable ones
                            for c in [c1, c2, c3, c5]:
                                if len(c) > 0 and has_ub_of_len[len(c)]:
                                    winning_action = [myHand[ei] for ei in c]
                            if winning_action is None:
                                winning_action = [myHand[ei] for ei in ub_combos_sol[0]]

                        # Found a winning action
                        if winning_action is not None:
                            # print("$" * 1200)
                            # print("MyHand", myHand)
                            # print("ToBeat", toBeat.cards if toBeat is not None else [])
                            # print("Others", othersHand)
                            # print("WinningAction", winning_action)
                            # print(others_best_combo)
                            # print("c1", c1)
                            # print("c2", c2)
                            # print("c3", c3)
                            # print("c5", c5)
                            # for xi in ans:
                            #     print(f"ub[{xi}]", ub_combos[xi - 1])
                            # print(ans)
                            return winning_action

        return None
