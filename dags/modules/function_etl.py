import pandas as pd
import sqlite3

def write_df_table(df,table,con=None):
    
    df.to_sql(table,con,   if_exists='append', index=False)
    print('Wrote correctly {}'.format(True))
def get_connnection(fruit_db):
    return sqlite3.connect(fruit_db)
