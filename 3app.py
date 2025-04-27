
from shiny import reactive, render
from shiny.express import input, render, ui
import utils
from utils import *

### ----------------- TASK3 -----------------------###
ui.page_opts(fillable=True)
with ui.layout_columns():
    # Checkout
    with ui.card():
        ui.h2("Checkout")
        ui.input_text("checkout_user_name", "User Name", "")  
        ui.input_selectize(
            "checkout_station_name", 
            "Choose station",
            get_station_names()
        )
        ui.input_action_button("checkout_bike", "Checkout")
        @render.text()
        @reactive.event(input.checkout_bike)
        def checkout():
            return bike_checkout(input.checkout_user_name(), input.checkout_station_name())

    # Droppoff
    with ui.card():
        ui.h2("Droppoff")
        ui.input_text("droppoff_user_name", "Username", "")  
        ui.input_selectize(
                "droppoff_station_name", 
                "Choose station",
                get_station_names()
        )
        ui.input_action_button("droppoff_bike", "Droppoff")
        @render.text()
        @reactive.event(input.droppoff_bike)
        def droppoff():
            return bike_droppoff(input.droppoff_user_name(), input.droppoff_station_name())

# Mapping of available spots
with ui.card():
    ui.h2("Mapping")
    ui.input_selectize(
            "mapping_station_name", 
            "Choose station",
            get_station_names()
    )
    ui.input_switch("get_park_mode_switch", "Available spots to take bike, or park")
    ui.input_action_button("mapping_station", "Search for available spots")
    @render.table(render_links=True, escape=False)
    @reactive.event(input.mapping_station)
    def mapp():
        mode = 'park' if input.get_park_mode_switch() else 'get'
        table = get_available_spots(input.mapping_station_name(), mode)
        return table 




