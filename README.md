# BigJudge

BigJudge is a non-official judge system for a Big Two bots competitions. It allows you to test and evaluate different algorithms efficiently.

## How to Add Your Algorithm

To add your own algorithm to the competition, follow these steps:

1. **Place Your Algorithm File:**
   
   Copy your algorithm as a single Python file and place it in the `algorithms` folder.

2. **Modify Imports in `judge_main.py`:**
   - Locate the import section in `judge_main.py` and add your algorithm file:
     ```python
     import algorithms.rnd_5321_w as alg1
     import algorithms.always_high_card as alg2
     import algorithms.play_weakest as alg3
     import algorithms.YOUR_FILE_NAME as alg4
     ```
   - You can change `alg1`, `alg2`, `alg3`, and `alg4` as needed.

3. **Add Your Algorithm to the Swiss Tournament:**

   To include your algorithm in the Swiss tournament, modify the following section in `judge_main.py`:
     ```python
     swiss_tourn_players.append(algorithms.YOUR_FILE_NAME.Algorithm())
     ```

## How to Run

To run the competition, go to the bottom of the `judge_main.py` file and uncomment the line corresponding to the mode you wish to run:

```python
run_games(num_games=1) 
run_games_in_parallel(num_games=30) 
run_and_get_score(num_rounds=30, games_per_round=3) 
run_swiss_tournament(swiss_tourn_players, 200)
```

**Competition Modes**

- `run_games(num_games=1)`: Runs a specified number of games using alg1, alg2, alg3, and alg4. This mode prints the entire gameplay process in detail and the results.
- `run_games_in_parallel(num_games=30)`: Runs games in parallel using multithreading to speed up execution. It prints only the results, not the detailed gameplay.
- `run_and_get_score(num_rounds=30, games_per_round=3)`: Runs a set number of games using the competition's scoring system.
- `run_swiss_tournament(swiss_tourn_players, 200)`: Runs a Swiss tournament with the players listed in swiss_tourn_players for a number of rounds.