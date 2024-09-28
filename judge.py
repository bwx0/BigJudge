import copy
import random
from enum import Enum
from typing import List, Optional, Tuple

from classes import Player, GameHistory, MatchState, Trick

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
    PASS = 0  # Invalid or Pass
    SINGLE = 1  # 1
    PAIR = 2  # 2
    TRIPLET = 3  # 3
    STRAIGHT = 4  # 5, consecutive ranks, (a)X,(a+1)Y,(a+2)Z,(a+3)U,(a+4)V
    FLUSH = 5  # 5, same suit, aX,bX,cX,dX,eX
    FULL_HOUSE = 6  # 5, triplet + pair  aX,aY,aZ,bU,bV
    FOUR_OF_A_KIND = 7  # 5, 4+1, XD,XC,XH,XS,any
    STRAIGHT_FLUSH = 8  # 5, straight + flush, (a)X,(a+1)X,(a+2)X,(a+3)X,(a+4)X


def validate_trick_and_get_strength(cards_available: Optional[List[str]], action: List[str]) -> \
        Tuple[bool, int, TrickType, str]:
    """
    IMPORTANT: Assume action is sorted by strengths.
    :param cards_available: cards the player have, or None to skip validation
    :param action:
    :return: Tuple[bool, int, TrickType, str]
        tuple[0]: is valid action
        tuple[1]: trick strength (used for comparing with the SAME type of trick), -1 for invalid actions
        tuple[2]: enum, trick type
        tuple[3]: reason or description in plain text
    """
    if not isinstance(action, List):
        return False, -1, TrickType.PASS, "Invalid action type."

    len_action = len(action)
    if len_action == 0:
        return True, 0, TrickType.PASS, "Action: Pass"
    if len_action > 5:
        return False, -1, TrickType.PASS, "Trick too long."
    if len_action != len(set(action)):
        return False, -1, TrickType.PASS, "Duplicate cards."
    if cards_available:  # check if that player has all cards in action
        for card in action:
            if card not in cards_available:
                return False, -1, TrickType.PASS, f"Player does not have Card[{card}]."

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


class PlayerStat:
    def __init__(self, pid: int, pname: str):
        self.player_id: int = pid
        self.player_name = pname
        self.score: int = 0
        self.games_played: int = 0
        self.first_to_act_count: int = 0
        self.num_games_win: int = 0
        self.num_games_win_first: int = 0

    def update(self, win: bool, is_first_to_act: bool, score_diff: int):
        self.games_played += 1
        self.num_games_win += win
        self.first_to_act_count += is_first_to_act
        self.num_games_win_first += win and is_first_to_act
        self.score += score_diff

    def __add__(self, other):
        assert self.player_id == other.player_id
        assert self.player_name == other.player_name
        result = PlayerStat(self.player_id, self.player_name)
        result.games_played = self.games_played + other.games_played
        result.first_to_act_count = self.first_to_act_count + other.first_to_act_count
        result.num_games_win = self.num_games_win + other.num_games_win
        result.num_games_win_first = self.num_games_win_first + other.num_games_win_first
        result.score = self.score + other.score
        return result

    def __repr__(self):
        return f"[{self.player_id:<4}{self.player_name:<25}{self.score:>9}{self.games_played:>10}{self.num_games_win:>5}]"


def print_leaderboard(player_stats: List[PlayerStat]):
    board = [(i, p.score) for i, p in enumerate(player_stats)]
    board.sort(key=lambda x: x[1], reverse=True)
    print("==================== Leaderboard ====================")
    print(f'{"Name":<30}{"Score":>9}{"GamesPlayed":>15}{"Win%":>9}{"FirstToAct":>12}{"WinFirstToAct%":>15}')
    for pi, score in board:
        stat = player_stats[pi]
        n_games = stat.games_played
        n_win = stat.num_games_win
        n_fh = stat.first_to_act_count
        n_win_fh = stat.num_games_win_first
        win_r = n_win / max(1, n_games)
        win_r_fh = n_win_fh / max(1, n_fh)
        print(f"{stat.player_name:<30}{score:>9}{n_games:>15}{100 * win_r:>8.1f}%{n_fh:>12}{100 * win_r_fh:>14.1f}%")
    print("=====================================================")


class Judge:

    def __init__(self, p1: any, p2: any, p3: any, p4: any,
                 p1n: str = "Player[0]", p2n: str = "Player[1]", p3n: str = "Player[2]", p4n: str = "Player[3]"):
        self._algorithms = [p1, p2, p3, p4]
        self._players: List[Player] = [Player(0, 0), Player(0, 0), Player(0, 0), Player(0, 0)]
        self._player_cards: List[List[str]] = [[], [], [], []]
        self._game_history_list: List[GameHistory] = []
        self._next_player_index: int = 0
        self._match_count: int = 0  # number of games finished
        self._is_first_move: bool = False  # is current move the first move in game (is new game)
        self._current_round_num: int = 0  # round num in game
        self._previous_msg: List[str] = ["", "", "", ""]
        self._previous_trick: Optional[Trick] = None
        self._previous_trick_type: TrickType = TrickType.PASS
        self._previous_trick_strength: int = 0
        self._current_match_first_player: int = -1
        self._initial_hands: List[List[str]] = []  # Players' initial hands, saved for debugging
        self._player_stats: List[PlayerStat] = [PlayerStat(0, p1n), PlayerStat(1, p2n), PlayerStat(2, p3n), PlayerStat(3, p4n)]
        self._PRINT_MSG = False

    def _dbg_print(self, *args, **kwargs):
        if not self._PRINT_MSG:
            return
        print(*args, **kwargs)

    def enable_debug_message(self):
        self._PRINT_MSG = True

    def disable_debug_message(self):
        self._PRINT_MSG = True

    def _deal(self, hands: List[List[str]] = None) -> None:
        """
        Deal cards to the 4 players.
        :param hands: Preset hands. Should be a list of 4 lists, each of which contains 13 strings. Or None to start randomly.
        """
        # Shuffle
        tmp = all_cards.copy()
        random.shuffle(tmp)
        if hands is not None:  # Use predefined hands if specified
            if isinstance(hands[0], list):
                tmp = [card for hand in hands for card in hand]
            elif isinstance(hands[0], str):
                tmp = hands
        self._initial_hands = tmp.copy()

        # Deal
        for pi in range(4):
            self._players[pi].handSize = 13
            self._player_cards[pi] = tmp[pi * 13:pi * 13 + 13]
            self._dbg_print(f"Player[{pi}]: {self._player_cards[pi]}")

        # Find the first player to play
        idx_3d = tmp.index('3D')
        self._next_player_index = idx_3d // 13
        self._current_match_first_player = self._next_player_index

        assert self._player_cards[idx_3d // 13][idx_3d % 13] == '3D'
        self._dbg_print(f"First player: {self._next_player_index}")

    def _init_match(self, hands: List[List[str]] = None):
        self._deal(hands)
        self._current_round_num = 0
        self._previous_msg = ["", "", "", ""]
        self._is_first_move = True
        self._game_history_list.append(GameHistory(False, -1, []))

    def _next_move(self) -> Tuple[int, Trick, TrickType, int]:
        """
        Get the next move and validate.
        :return:
        tuple[0] player index (=self.next_player_index)
        tuple[1] trick played
        tuple[2] trick type
        tuple[3] trick strength
        """
        player_index = self._next_player_index
        self._dbg_print(f"Player[{player_index}] plays.", end="   ")

        # Construct match state and get the next action
        player_alg = self._algorithms[player_index]
        match_state = self._get_match_state(player_index)

        # Protection against tampering, slows down as game proceeds and completes
        # match_state = copy.deepcopy(match_state)

        # Get the next action
        action, new_msg = player_alg.getAction(match_state)
        self._previous_msg[player_index] = new_msg
        action.sort(key=get_strength)

        # Validate action (general validation)
        is_valid, strength, trick_type, reason = validate_trick_and_get_strength(self._player_cards[player_index], action)
        self._dbg_print(f"Proposed action: {action}  Type={trick_type}")

        # First move check
        if self._is_first_move:
            self._is_first_move = False
            if "3D" not in action:
                # is_valid, strength, trick_type, reason = False, -1, TrickType.PASS, "Game not started with 3D."
                print("Warning: Game not started with 3D, defaulting to ['3D'].")
                action = ['3D']
                is_valid, strength, trick_type, reason = True, 0, TrickType.SINGLE, None

        # Check if trick type does not match or beat
        is_trick_type_stronger = False
        if trick_type != TrickType.PASS and self._previous_trick_type != TrickType.PASS and trick_type != self._previous_trick_type:
            if len(self._previous_trick.cards) != 5:
                is_valid, strength, trick_type, reason = False, -1, TrickType.PASS, "Trick type does not match the previous one."
            else:  # 5 cards, trick type matters
                is_trick_type_stronger = trick_type.value > self._previous_trick_type.value
                if not is_trick_type_stronger:
                    is_valid, strength, trick_type, reason = False, -1, TrickType.PASS, "Trick TYPE does not beat the previous one."

        if not is_trick_type_stronger and trick_type != TrickType.PASS and strength <= self._previous_trick_strength:
            is_valid, strength, trick_type, reason = False, -1, TrickType.PASS, "Trick does not beat the previous one."

        if not is_valid:
            print(f"Invalid action type, defaulting to pass. Reason: {reason}")
            print(f"Action: {action}")
            print(f"ToBeat: {match_state.toBeat}")
            action, strength, trick_type = [], -1, TrickType.PASS
            raise Exception(self._initial_hands)
        else:
            self._dbg_print(f"Action={action} Strength={strength}   Msg={reason}")

        # Remove cards played
        for card in action:
            self._player_cards[player_index].remove(card)

        assert len(action) == 0 or is_trick_type_stronger or strength > self._previous_trick_strength

        player_trick = Trick(player_index, action)
        return player_index, player_trick, trick_type, strength

    def _round(self) -> bool:
        """

        :return: Game finished
        """

        self._previous_trick = None
        self._previous_trick_type = TrickType.PASS
        self._previous_trick_strength = -1

        loop_cnt = 0

        self._dbg_print("================= new round =================")
        # self.print_hands()

        while True:
            loop_cnt += 1
            if loop_cnt > 200:
                raise Exception("Round not finished in 200 moves.")

            # 3 consecutive passes, end this round
            if self._previous_trick is not None and self._previous_trick.playerNum == self._next_player_index:
                assert len(self._game_history_list[-1].gameHistory[-1]) > 3 and \
                       all([len(tr.cards) == 0 for tr in self._game_history_list[-1].gameHistory[-1][-3:]])
                self._previous_trick = None
                self._previous_trick_strength = 0
                self._dbg_print("3 passes in a row, round ends.")
                return False

            player_index, player_trick, trick_type, trick_strength = self._next_move()

            # Update previous trick
            if trick_type != TrickType.PASS:
                self._previous_trick = player_trick
                self._previous_trick_type = trick_type
                self._previous_trick_strength = trick_strength

            # Update player
            self._players[player_index].handSize = len(self._player_cards[player_index])

            # Update game history
            current_game = self._game_history_list[-1]
            if len(current_game.gameHistory) == 0:  # Initialise a new trick list
                self._game_history_list[-1].gameHistory.append([])
            current_round = current_game.gameHistory[-1]
            current_round.append(player_trick)

            # Current player wins the game
            if len(self._player_cards[player_index]) == 0:
                current_game.finished = True
                current_game.winnerPlayerNum = player_index
                return True

            # move_to_next_player()
            self._next_player_index = (self._next_player_index + 1) % 4

    def _on_match_end(self):
        self._match_count += 1

        score_diff = self._update_scores()

        # update stats
        idx_player_win = self._game_history_list[-1].winnerPlayerNum
        assert 0 <= idx_player_win < 4
        for i in range(4):
            self._player_stats[i].update(i == idx_player_win, i == self._current_match_first_player, score_diff[i])

    def _get_match_state(self, for_player_index: int):
        # assert round not finished
        assert not self._previous_trick or self._previous_trick.playerNum != for_player_index

        return MatchState(myPlayerNum=for_player_index,
                          players=self._players.copy(),
                          myHand=self._player_cards[for_player_index].copy(),
                          toBeat=copy.copy(self._previous_trick),
                          matchHistory=self._game_history_list,
                          myData=self._previous_msg[for_player_index])

    def _update_scores(self) -> List[int]:
        remaining_card_cnt = [len(cs) for cs in self._player_cards]
        assert remaining_card_cnt.count(0) == 1

        winner_idx = remaining_card_cnt.index(0)
        tot_lose = 0
        score_diff = [0, 0, 0, 0]

        for i in range(4):
            num_cards = len(self._player_cards[i])
            lose_points = Judge._get_points_lost(num_cards)
            self._players[i].points -= lose_points
            tot_lose += lose_points
            self._dbg_print(f"Player[{i}] lost {lose_points} points.")
            score_diff[i] -= lose_points

        self._players[winner_idx].points += tot_lose
        score_diff[winner_idx] += tot_lose
        self._dbg_print(f"Player[{winner_idx}] won {tot_lose} points.")
        return score_diff

    @staticmethod
    def _get_points_lost(num_cards):
        assert 0 <= num_cards <= 13
        lose_points = num_cards
        if num_cards == 13:
            lose_points *= 3
        elif num_cards >= 10:
            lose_points *= 2
        return lose_points

    def run_match(self, hands: Optional[List[List[str]]] = None):
        self._dbg_print("============================================")
        self._dbg_print("================= new game =================")
        self._dbg_print("============================================")

        self._init_match(hands)
        while not self._round():
            self._current_round_num += 1
        self._on_match_end()

    def print_leaderboard(self):
        print_leaderboard(self.player_stats)

    def print_game_history(self):
        print("==================== Game History ====================")
        for i, history in enumerate(self._game_history_list):
            print(f"========== Game {i} ==========")
            print(f"Winner: Player[{history.winnerPlayerNum}]" if history.finished else "Unfinished")
            for r, t in enumerate(history.gameHistory):
                print(f"Round[{r + 1}]: {t}")

    def print_hands(self):
        print("=========== Current Player Hands ===========")
        print(f"Player      Cards")
        for i, cards in enumerate(self._player_cards):
            print(f"Player[{i}]  ({self._players[i].handSize})   {cards}")
        print("===================================")

    @property
    def player_stats(self):
        return self._player_stats
