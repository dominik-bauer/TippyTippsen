# TippyTippsen
A Threema bot that sends the ranking of a Bundesliga betting game to all players.

### Rationale
This is a fun project to learn new stuff, especiall CI/CD.

#### The Betting Game
In this private betting game, 5 players are guessing each, how the final ranking tables of the first three german soccer leagues will look like after the current season 22/23. Those leagues are 1. Bundesliga, 2. Bundesliga and 3. Bundesliga. The player with the best guess wins. The best guess is determined by a simple points system:

- 3 Points for a team, whose rank was correctly guessed (diff: 0)
- 2 Points for a team, whose rank was almost certainly correctly guessed (diff: 1)
- 1 Point for a team, whose rank was almost correctly guessed (diff: 2)
- 0 Points for a team, whose rank was incorrectly guesses (diff > 2)

Say, Team A wins the season championship and is ranked in first position. If one predicted that Team A is first, 3 points are received. But if one predicted Team A in 2nd or 3rd or 4th position, accordingly 2 or 1 or 0 points are received.

#### The Bot
The Bot scrapes match data from the sports news site sportschau.de. In order to avoid uneccessary calls of the site, the bot estimates the end time of the final matches of the current day. At the estimated time the bot will check every two minutes if all games are finished. If so, it will scrape the current ranking tables of 1st, 2nd and 3rd Bundesliga and compare those with the tipps of the 5 players. It will apply the point system and will send every player the according overview of the points. The overview will be send as an image to all players.
