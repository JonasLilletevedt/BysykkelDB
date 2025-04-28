import sqlite3
import pandas as pd
import controller
from controller import *
import model
from model import *
from shiny import render, ui
from shiny.express import input

### ----------------- TASK2 -----------------------###
def get_task_a():
    table_df = search_table(input.input_filter_a(), 
                                "user", "user_name", 
                                ["user_name", "user_phone_number"] 
                                )
    return table_df

def get_task_b():
    table_df = get_trips_ended_on_all_stations()
    return table_df

def get_task_c(): 
    return get_available_bikes_based_on_station_and_bike_name(input.station_filter_name(), input.bike_filter_name())

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
    "Velg oppgave a eller b:",  
    {"a": "Filter user (a)", 
     "b": "Antall trips til stasjon (b)", 
     "c": "Tilgengelige sykler på stasjon (c)"}  
) 

ui.output_ui("conditional_controls")
ui.h1("BYSYKKEL DATABSE:)")
@render.ui
def conditional_controls_def():
    task = input.selectize()
    if task == "a":
        return ui.input_text(
            "input_filter_a",
            "Filter user name",
            ""
        )
    elif task == "b":
        return ui.tags.p("Antall trips til endestasjon"),

    elif task == "c":
        return [
            ui.input_text("station_filter_name",
                          "Filter station name",
                          ""),
            ui.input_text("bike_filter_name",
                          "Filter bike name",
                          "")
        ]
# Renders table
@render.data_frame
def render_table1():
    inp = input.selectize()
    table_df = get_table_from_task(inp)
    # Shows coorect table based on user input
    return table_df






