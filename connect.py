import sqlite3
from sqlite3 import Error
import pandas as pd
from pandas.core.frame import DataFrame

def sql_connection(): 
    try: 
        con = sqlite3.connect('Z://smart_wardrobe.db')
        print("Connection is established")
 
    except Error:
        print(Error)
 
    # finally:
    #     con.close()

def sql_table(con):
    cur = con.cursor()
    result = cur.execute("select * from indoor")
    result = result.fetchall()
    return result
    
 
con = sqlite3.connect('Z://smart_wardrobe.db')
print("Connection is established")
table = sql_table(con)
con.close()

table=DataFrame(table)
print(table.head())