import random
import time
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict

import numpy as np

from judge import Judge, PlayerStat, print_leaderboard

import algorithms
from swiss import SwissTournament, STPlayer, print_swiss_leaderboard

import algorithms.always_high_card
import algorithms.rnd
import algorithms.rnd_1235
import algorithms.rnd_1235_w
import algorithms.rnd_5321
import algorithms.rnd_5321_w
import algorithms.play_weakest
import algorithms.play_strongest

"""
Import your algorithms from anywhere
"""

import algorithms.rnd_5321_w as alg1
import algorithms.always_high_card as alg2
import algorithms.play_weakest as alg3
import algorithms.team_SCUTChinaNo1 as alg4

"""
Add participants to the swiss tournament.
"""
swiss_tourn_players = list()

swiss_tourn_players.append(alg1.Algorithm())
swiss_tourn_players.append(alg2.Algorithm())
swiss_tourn_players.append(alg3.Algorithm())
swiss_tourn_players.append(alg4.Algorithm())
swiss_tourn_players.append(algorithms.always_high_card.Algorithm())
swiss_tourn_players.append(algorithms.always_high_card.Algorithm())
swiss_tourn_players.append(algorithms.rnd.Algorithm())
swiss_tourn_players.append(algorithms.rnd_1235.Algorithm())
swiss_tourn_players.append(algorithms.rnd_1235_w.Algorithm())
swiss_tourn_players.append(algorithms.rnd_5321.Algorithm())
swiss_tourn_players.append(algorithms.rnd_5321_w.Algorithm())
swiss_tourn_players.append(algorithms.play_weakest.Algorithm())
swiss_tourn_players.append(algorithms.play_strongest.Algorithm())

"""
Functions
"""


def run_games(num_games: int):
    """
    Player {num_games} sequentially and print the final score.
    Players are scored following the rules on the event wiki page.
    Run this when you want to debug your algorithm.
    """
    p1 = alg1.Algorithm()
    p2 = alg2.Algorithm()
    p3 = alg3.Algorithm()
    p4 = alg4.Algorithm()

    judge = Judge(p1, p2, p3, p4, p1.__module__, p2.__module__, p3.__module__, p4.__module__)
    judge.enable_debug_message()

    for i in range(num_games):
        start_time = time.time()
        judge.run_match()
        print(f"Game {i} takes {time.time() - start_time}s.")

    judge.print_game_history()
    judge.print_leaderboard()


def _run_worker(cnt):
    p1 = alg1.Algorithm()
    p2 = alg2.Algorithm()
    p3 = alg3.Algorithm()
    p4 = alg4.Algorithm()
    judge = Judge(p1, p2, p3, p4, p1.__module__, p2.__module__, p3.__module__, p4.__module__)
    for i in range(cnt):
        judge.run_match()
    return judge.player_stats


def _run_and_get_points_worker(params) -> List[int]:
    """
    Returns a list of 4 ints, indicating the points each player gets in {games_per_round} rounds.
    """
    ps, games_per_round = params

    pi = [0, 1, 2, 3]  # player index
    random.shuffle(pi)  # shuffle the players

    i1, i2, i3, i4 = pi[0], pi[1], pi[2], pi[3]
    judge = Judge(ps[i1][0], ps[i2][0], ps[i3][0], ps[i4][0], ps[i1][1], ps[i2][1], ps[i3][1], ps[i4][1])
    for i in range(games_per_round):
        judge.run_match()
    stats = judge.player_stats.copy()
    stats.sort(key=lambda x: x.score, reverse=True)

    score = [0, 0, 0, 0]
    for i, stat in enumerate(stats):
        oi = pi[stat.player_id]
        score[oi] = 3 - i

    return score


def run_games_in_parallel(num_games: int):
    """
    Run games in parallel to speed up the process.
    """
    stats: List[PlayerStat] = [None, None, None, None]
    with ProcessPoolExecutor() as executor:
        stats_list = list(executor.map(_run_worker, [1] * num_games))
        for i in range(4):
            stats[i] = sum([x[i] for x in stats_list],
                           start=PlayerStat(stats_list[0][i].player_id, stats_list[0][i].player_name))

    stats.sort(key=lambda x: x.score, reverse=True)
    for i, stat in enumerate(stats):
        print(stat.player_name, stat.score)
    print_leaderboard(stats)


def run_and_get_scores(num_rounds: int = 20, games_per_round: int = 3):
    """
    Play {num_rounds} rounds.
    In each round:
        Play {games_per_round} games.
        At the end of each game: Score each player based on the number of remaining cards,
                                 following the rules on the event wiki page.
        The player with the highest score earns 3 points,
                        the 2nd-highest earns 2 points,
                        the 3rd-highest earns 1 point,
                        the 4-th player earns 0 points.
    """
    p1 = alg1.Algorithm()
    p2 = alg2.Algorithm()
    p3 = alg3.Algorithm()
    p4 = alg4.Algorithm()

    ps = [[p1, p1.__module__, 0], [p2, p2.__module__, 0], [p3, p3.__module__, 0], [p4, p4.__module__, 0]]
    with ProcessPoolExecutor() as executor:
        scores = list(executor.map(_run_and_get_points_worker, [(ps, games_per_round)] * num_rounds))
        tot = np.sum(scores, axis=0)

        lb = list(zip(tot, [p1.__module__, p2.__module__, p3.__module__, p4.__module__]))
        lb.sort(key=lambda x: x[0], reverse=True)

        print("=" * 50)
        print(f"{'Rank':<8}{'Name':<30}{'Score':>8}")
        for i, (score, pn) in enumerate(lb):
            print(f"{i:<8}{pn:<30}{score:>8}")
        print(f"Rounds: {num_rounds}")


def _swiss_round(players_4: List[STPlayer]) -> Dict[int, int]:
    random.shuffle(players_4)
    p1, p2, p3, p4 = players_4[0], players_4[1], players_4[2], players_4[3]
    judge = Judge(p1.alg, p2.alg, p3.alg, p4.alg, p1.player_id, p2.player_id, p3.player_id, p4.player_id)
    for i in range(3):
        judge.run_match()
    rnk = sorted(judge._player_stats, key=lambda x: x.score, reverse=True)
    round_score = dict()
    for k in range(4):
        round_score[rnk[k].player_name] = 3 - k
    return round_score


def run_swiss_tournament(ps: List, num_rounds: int = 20):
    ps = ps.copy()
    if len(ps) % 4 != 0:
        print("Number of players is not a multiple of 4, adding default players.")
        while len(ps) % 4 != 0:
            ps.append(algorithms.always_high_card.Algorithm())

    swiss_players: List[STPlayer] = [STPlayer(i, p.__module__, p) for i, p in enumerate(ps)]

    st = SwissTournament(swiss_players)
    for r in range(num_rounds):
        pairs = st.pair_players()
        print(f"Round {r + 1}")
        print(pairs)
        with ProcessPoolExecutor() as executor:
            result = executor.map(_swiss_round, pairs)
            for round_score in result:
                for k, v in round_score.items():
                    swiss_players[k].score += v
            print_swiss_leaderboard(swiss_players)

    print_swiss_leaderboard(swiss_players)


"""
Uncomment lines to run your preferred competition mode.
"""

if __name__ == '__main__':
    # run_games(num_games=1)
    run_games_in_parallel(num_games=30)
    # run_and_get_scores(num_rounds=30, games_per_round=3)
    # run_swiss_tournament(swiss_tourn_players, num_rounds=200)
