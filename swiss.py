import random
from typing import List, Tuple
from collections import defaultdict


class STPlayer:
    def __init__(self, player_id: int, name: str, alg: any) -> None:
        self.player_id = player_id
        self.name: str = name
        self.score: int = 0
        self.alg = alg

    def __repr__(self) -> str:
        return f"{self.name} (Score: {self.score})"


def print_swiss_leaderboard(players: List[STPlayer]):
    print("============= Swiss Tournament Leaderboard =============")
    print(f'{"Name":<30}{"Score":>9}')
    for player in sorted(players, key=lambda p: p.score, reverse=True):
        print(f"{player.name:<30}{player.score:>9}")
    print("========================================================")


class SwissTournament:
    def __init__(self, players: List[STPlayer]) -> None:
        self.players: List[STPlayer] = players

    def pair_players(self) -> List[List[STPlayer]]:
        """Pairs players based on their current scores."""
        lb = sorted(self.players, key=lambda x: x.score, reverse=True)
        paired_players: List[List[STPlayer]] = []
        for i in range(0, len(lb), 4):
            paired_players.append(lb[i:i + 4])
        return paired_players
