import pandas as pd

#https://database.lichess.org/#puzzles
df = pd.read_csv('lichess_db_puzzle.csv.zst', usecols=['Moves','Rating'])

df['MoveCount'] = df.Moves.str.split().apply(lambda x: len(x))

df['RatingBin'] = pd.cut(df.Rating, range(0,3200,200))

print(df[['RatingBin', 'MoveCount']].groupby('RatingBin').agg({'MoveCount':'mean','RatingBin':'count'}))

# MoveCount includes both sides, so should be halved for one player's moves
"""
| RatingBin    |   MoveCountAverage |   TotalPuzzles |
|--------------|--------------------|----------------|
| (0, 200]     |           NaN      |              0 |
| (200, 400]   |          2.921356  |          14216 |
| (400, 600]   |          3.032931  |         146213 |
| (600, 800]   |          3.264057  |         254862 |
| (800, 1000]  |          3.624514  |         576810 |
| (1000, 1200] |          4.010414  |         671590 |
| (1200, 1400] |          4.344388  |         581089 |
| (1400, 1600] |          4.577844  |         593399 |
| (1600, 1800] |          4.896454  |         537509 |
| (1800, 2000] |          5.212270  |         460617 |
| (2000, 2200] |          5.569663  |         381176 |
| (2200, 2400] |          5.998178  |         301916 |
| (2400, 2600] |          6.516740  |         158838 |
| (2600, 2800] |          7.162796  |         106151 |
| (2800, 3000] |          7.967473  |          14511 |
"""