import pandas as pd
from sqlalchemy import create_engine
import urllib

server   = 'willsqlserver.database.windows.net'
database = 'wesqldev'
username = 'CloudSAadf997a5'
password = 'Gene$7escalante'

connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

csv_path = 'data/raw/NFL Play by Play 2009-2018 (v5).csv'
print("Reading CSV...")
df = pd.read_csv(csv_path, low_memory=False)
print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")

print("Uploading to Azure SQL...")
df.to_sql(
    name='nfl_play_by_play',
    con=engine,
    if_exists='replace',
    index=False,
    chunksize=1000
)
print(f"Done! {len(df):,} rows uploaded to table 'nfl_play_by_play'.")

