
from shiny import reactive, render
from shiny.express import input, render, ui
import utils
from utils import *

path = "bysykkel.db"



ui.page_opts(fillable=True)


with ui.layout_columns():
    with ui.card():
        ui.h2("Checkout")
        ui.input_text("checkout_user_name", "User Name", "")  
        ui.input_selectize(
            "station_name", 
            "Choose station",
            get_station_names(path)
        )
        ui.input_action_button("checkout_bike", "Checkout")
        @render.text()
        @reactive.event(input.checkout_bike)
        def checkout():
            available_bike = get_first_available_bike(path, input.station_name())

            if len(available_bike) == 0:
                return "No bike available at station"
            
            # id [0]
            bike_id = available_bike[0]
            # name[1]
            bike_name = available_bike[1]
            bike_checkout(path, bike_id, "Active")

            return f"Checkout succesfull, collect your bike: {bike_name}"

        

    with ui.card():
        ui.h2("Dropoff")
        ui.input_text("droppoff_user_name", "Username", "")  
        ui.input_text("droppoff_station_name", "Phone number", "") 


