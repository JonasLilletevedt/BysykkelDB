import model
from model import *
from shiny import reactive, render
from shiny.express import input, render, ui, session
from ipyleaflet import Map, Marker
from shinywidgets import render_widget
import controller
from controller import *

### ----------------- TASK3 -----------------------###

# UI Modal for bike survey
bike_survey_modal = ui.modal(
    "Choose complaint type",
    ui.input_selectize(
        "complaint_id", 
        "If you have a complaint about the bike, please choose complaint under",
        get_complaint_types_and_id()
    ),
    ui.input_action_button("submit_complaint_button", "Submit complaint"),
    title="Bike survey",
    easy_close=True
)

ui.page_opts(fillable=True)
with ui.layout_column_wrap():
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
            # droppoff_info tuple, 0 is message to user, 1 is bool if droppoff went through
            droppoff_info = bike_droppoff(input.droppoff_user_name(), input.droppoff_station_name())
            if droppoff_info[1]:
                ui.modal_show(bike_survey_modal)
            droppoff_message = droppoff_info[0]
            return droppoff_message

    @reactive.Effect
    @reactive.event(input.submit_complaint_button)
    async def complaint():
        submit_complaint(input.droppoff_user_name(), input.complaint_id())

    @reactive.Effect
    @reactive.event(input.submit_complaint_button)
    async def complaint_message():
        ui.notification_show(
            "Complaint submitted, you can submit multiple complaints for a bike, press dismiss when done"
        )


### ---------- TASK4 ------------- ###
# Mapping of available spots
ui.page_opts(fillable=True)
with ui.layout_column_wrap():
    with ui.card():
        ui.h2("Mapping")
        ui.input_selectize(
            "mapping_station_name", 
            "Choose station",
            get_station_names()
        )
        ui.input_switch("get_park_mode_switch", "Find availble bike, instead of parking spots")
        @render.table(render_links=True, escape=False)
        def mapp():
            mode = 'park' if input.get_park_mode_switch() else 'get'
            table = get_available_spots(input.mapping_station_name(), mode)
            return table 

    with ui.card():
        @render_widget
        def render_map():
            x,y = get_cordinates(input.mapping_station_name())
            map = Map(center=(x, y), zoom=20)
            point = Marker(location=(x, y), draggable=False)
            map.add_layer(point)
            return map

 




