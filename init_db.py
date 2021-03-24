import sqlite3
import pandas as pd
from scraper import vice_data_df, itsnicethat_df, pitchfork_df, the_verge_df, ars_df, wired_df

connection = sqlite3.connect('database.db')

vice_data_df.to_sql('vicenews', connection, if_exists='replace')
itsnicethat_df.to_sql('itsnicethat', connection, if_exists='replace')
pitchfork_df.to_sql('pitchfork', connection, if_exists='replace')
the_verge_df.to_sql('verge', connection, if_exists='replace')
ars_df.to_sql('ars', connection, if_exists='replace')
wired_df.to_sql('wired', connection, if_exists='replace')

vice = pd.read_sql('SELECT * FROM vicenews', connection)
itsnicethat = pd.read_sql('SELECT * FROM itsnicethat', connection)
pitchfork = pd.read_sql('SELECT * FROM pitchfork', connection)
the_verge = pd.read_sql('SELECT * FROM verge', connection)
ars_technica = pd.read_sql('SELECT * FROM ars', connection)
wired = pd.read_sql('SELECT * FROM wired', connection)


# print(itsnicethat)
# print(pitchfork)
# print(ars_technica)
# print(wired)
# print(the_verge)