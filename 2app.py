import sqlite3
import pandas as pd
import utils
from utils import *
from shiny import render, ui
from shiny.express import input

path = "bysykkel.db"

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

ui.h1("BYSYKKEL DATABSE:)")
ui.input_text("input", "", "Filter")
# Renders table
@render.data_frame
def render_table1():
    # Shows coorect table based on user input
    table_df = search_table(input.input(), "user", "user_name", ["user_name", "user_phone_number"], path)
    return table_df






