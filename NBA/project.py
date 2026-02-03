import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats, leaguestandings

# Pull Player Data
player_data = leaguedashplayerstats.LeagueDashPlayerStats(
    measure_type_detailed_defense='Advanced',
    season='2025-26' # Updated to the current season as we discussed
).get_data_frames()[0]

scouting_df = player_data[[
    'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE',
    'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'USG_PCT'
]]

# Pull Standings Data - Fixed the season='2025-26' syntax here
standings_data = leaguestandings.LeagueStandings(season='2025-26').get_data_frames()[0]
standings_df = standings_data[['TeamID', 'TeamCity', 'TeamName', 'Conference', 'WINS', 'LOSSES']]

# Save to CSV
scouting_df.to_csv('nba_player_stats.csv', index=False)
standings_df.to_csv('nba_team_standings.csv', index=False)

print("Success! Files saved to your Project folder.")
print(scouting_df.head())
