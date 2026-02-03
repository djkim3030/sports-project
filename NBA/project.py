import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats, leaguestandings
import pyodbc

# --- PART 1: DATA COLLECTION ---
player_data = leaguedashplayerstats.LeagueDashPlayerStats(
    measure_type_detailed_defense='Advanced',
    season='2025-26' 
).get_data_frames()[0]

scouting_df = player_data[[
    'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE',
    'OFF_RATING', 'DEF_RATING', 'TS_PCT', 'USG_PCT'
]]

# Save to CSV
scouting_df.to_csv('nba_player_stats.csv', index=False)
print("Success! Files saved to your Project folder.")

# --- PART 2: CLOUD UPLOAD ---
server = 'dj-nbastats.database.windows.net'
database = 'nba'
username = 'dj3030'
password = 'l17951131a!'
driver = '/opt/homebrew/lib/libmsodbcsql.18.dylib'

conn_str = f'DRIVER={{{driver}}};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# NEW STEP: Create the table if it doesn't exist in the 'nba' database
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PlayerStats]') AND type in (N'U'))
    CREATE TABLE PlayerStats (
        PLAYER_ID INT,
        PLAYER_NAME VARCHAR(255),
        TEAM_ABBREVIATION VARCHAR(10),
        AGE FLOAT,
        OFF_RATING FLOAT,
        DEF_RATING FLOAT,
        TS_PCT FLOAT,
        USG_PCT FLOAT
    )
""")
conn.commit()

# Load the CSV and Push to Azure
df = pd.read_csv('nba_player_stats.csv')

for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO PlayerStats (PLAYER_ID, PLAYER_NAME, TEAM_ABBREVIATION, AGE, OFF_RATING, DEF_RATING, TS_PCT, USG_PCT)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, 
    row.PLAYER_ID, row.PLAYER_NAME, row.TEAM_ABBREVIATION, row.AGE, row.OFF_RATING, row.DEF_RATING, row.TS_PCT, row.USG_PCT)

conn.commit()
cursor.close()
conn.close()

print("Data pushed to Azure!")
