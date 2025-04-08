import sqlite3
import pandas as pd

from shiny.express import input, ui, render


def getTable(table_name):
    # Whitelist
    whitelist = {"user", "bike", "subscription"}
    if table_name not in whitelist:
        return "ERROR: Wrong table name"
    # Open connection to database
    con = sqlite3.connect('bysykkel.db')

    # Use parameterized query to prevent SQL injection
    query = f"SELECT * FROM {table_name}"
    
    # Execute query with the table name
    df = pd.read_sql_query(query, con)
    
    # Close the connection
    con.close()

    return df

def get_task_a():
    # Open connection to database
    con = sqlite3.connect('bysykkel.db')

    # Use parameterized query to prevent SQL injection
    query = "SELECT user_name FROM user ORDER BY user_name"

    # Execute query with the table name
    df = pd.read_sql_query(query, con)

    # Close the connection
    con.close()

    return df

def get_task_b():
    # Open connection to database
    con = sqlite3.connect('bysykkel.db')

    # Use parameterized query to prevent SQL injection
    query = "SELECT bike_name, bike_status FROM bike"

    # Execute query with the table name
    df = pd.read_sql_query(query, con)

    # Close the connection
    con.close()

    return df

def get_task_c():
    # Open connection to database
    con = sqlite3.connect('bysykkel.db')

    # Use parameterized query to prevent SQL injection
    query = "SELECT subscription_type FROM subscription"

    # Execute query with the table name
    df = pd.read_sql_query(query, con)

    # Count different subscription types and create a new DataFrame
    count_df = df['subscription_type'].value_counts().reset_index()
    count_df.columns = ['Type', 'count']

    # Sort based on the custom order
    count_df = count_df.sort_values(by='Type')

    # Close the connection
    con.close()

    return count_df

# Chooses correct table based in user input
def get_table_from_task(task):
    if task == "a": 
        return get_task_a()
    elif task == "b":
        return get_task_b()
    elif task == "c":
        return get_task_c()
    else:
        return pd.DataFrame()
        

# Allows user input
ui.input_selectize(  
    "selectize",  
    "Velg oppgave a, b eller c:",  
    {"a": "User names (a)", "b": "Bike names with status (b)", "c": "Subscription purchases (c)"}  
) 

# Renders table
ui.h1("BYSYKKEL DATABSE:)")
@render.data_frame
def render_table1():
    # User input through selectize
    inp = input.selectize()
    # Shows coorect table based on user input
    table_df = get_table_from_task(inp)
    return table_df

