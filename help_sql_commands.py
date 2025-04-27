import sqlite3
import pandas as pd

path = "bysykkel.db"
# Inserts to table
def insert_to_table(table, dict_attributes_values):
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()

    # Sql command, input to sqlite
    sql_command = f"INSERT INTO {table} ({",".join(list(dict_attributes_values.keys()))}) VALUES ({",".join(list(dict_attributes_values.values()))});" 
    try:
        cur.execute(sql_command)
        print("Added to db")
        # Commits
        con.commit()
        return True
    except:
        print("Not added")
        print(sql_command)
        return False

def search_table(search, table, main_attr, attributes):
    attr = ",".join(attributes) 
    # Connection to db
    con = sqlite3.connect(path)
    cur = con.cursor()
    sql_command = f"SELECT {attr} FROM {table} WHERE {main_attr} LIKE '%{search}%';"
    table = pd.read_sql_query(sql_command, con)

    return table


def update_table(table, id_name, id_value, attribute_name, value):
    con = sqlite3.connect(path)
    cur = con.cursor()
    
    sql_command = f"""
    UPDATE
        `{table}`
    SET
        `{attribute_name}` = ?
    WHERE
        `{id_name}` = ?
    """

    cur.execute(sql_command, (value, id_value))
    con.commit()
