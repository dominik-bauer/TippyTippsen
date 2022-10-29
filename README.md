# TippyTippsen
A Threema bot that sends the ranking of a Bundesliga betting game to all players.

#### The Betting Game
In this private betting game, 5 players are guessing each, how the final ranking tables of the first three german soccer leagues will look like after the current season 22/23. Those leagues are 1. Bundesliga, 2. Bundesliga and 3. Bundesliga. The player with the best guess wins. The best guess is determined by a simple points system:

- 3 Points for a team, whose rank was correctly guessed (diff: 0)
- 2 Points for a team, whose rank was almost certainly correctly guessed (diff: 1)
- 1 Point for a team, whose rank was almost correctly guessed (diff: 2)
- 0 Points for a team, whose rank was incorrectly guesses (diff > 2)

Say, Team A wins the season championship and is ranked in first position. If one predicted that Team A is first, 3 points are received. But if one predicted Team A in 2nd or 3rd or 4th position, accordingly 2 or 1 or 0 points are received.

#### The Bot
The Bot regulary fetches the current Bundesliga tables and compares them with the guesses (tipps) of each player. The Bundesliga tables are derived from the awesome [OpenLigaDB](https://www.openligadb.de/), examples for API usage are found [here](https://github.com/OpenLigaDB/OpenLigaDB-Samples) on GitHub. 