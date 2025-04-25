
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
            "checkout_station_name", 
            "Choose station",
            get_station_names(path)
        )
        ui.input_action_button("checkout_bike", "Checkout")
        @render.text()
        @reactive.event(input.checkout_bike)
        def checkout():
            available_bike = get_first_available_bike(path, input.checkout_station_name())
            if len(available_bike) == 0:
                return "No bike available at station"
            
            # id [0]
            bike_id = available_bike[0]
            # name[1]
            bike_name = available_bike[1]
            bike_checkout(path, bike_id)
            print("Checkout complete")
            user_id = get_user_id_from_user_name(path, input.checkout_user_name())
            print("user")
            station_id = get_station_id_from_station_name(path, input.checkout_station_name())
            print("station")
            start_new_trip(path, user_id, bike_id, station_id)
            print("new trip created")
            return f"Checkout succesfull, collect your bike: {bike_name}"

        

with ui.card():
    ui.h2("Dropoff")
    ui.input_text("droppoff_user_name", "Username", "")  
    ui.input_selectize(
            "droppoff_station_name", 
            "Choose station",
            get_station_names(path)
    )
    ui.input_action_button("droppoff_bike", "Dropoff")
    @render.text()
    @reactive.event(input.droppoff_bike)
    def droppoff():
        bike_droppoff(path, input.droppoff_user_name(), input.droppoff_station_name())
        return "Droppoff done :)"

with ui.card():
    ui.h2("Mapping")
    ui.input_selectize(
            "mapping_station_name", 
            "Choose station",
            get_station_names(path)
    )
    ui.input_action_button("droppoff_bike", "Dropoff")
    @render.text()
    @reactive.event(input.droppoff_bike)
    def droppoff():
        bike_droppoff(path, input.droppoff_user_name(), input.droppoff_station_name())
        return "Droppoff done :)"




