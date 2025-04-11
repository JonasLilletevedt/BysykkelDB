
from shiny import reactive, render
from shiny.express import input, render, ui
import utils
from utils import *

ui.page_opts(fillable=True)


with ui.layout_columns():
    with ui.card():
        ui.input_text("user_name", "Username", "")  
        ui.input_text("user_phone_number", "Phone number", "") 
        ui.input_text("user_email", "Email", "") 


    with ui.card():

        @render.text  
        def error_user_name():
            if not check_valid_name(input.user_name()):
                return "user name is not valid, should only contain english letters"  
            else:
                return "User name is valid"

            
        @render.text  
        def error_phone_number():
            if not check_phone_number(input.user_phone_number()):
                return "phone number is not valid, should be exactly nine digits"
            else:
                return "phone number is valid"

        @render.text  
        def error_email():
            if not check_valid_email(input.user_email()):
                return "email is not valid, should contain '@'"
            else:
                return "email is valid"
            
def check_all_inputs(user_name, user_phone_number, user_email):
    return check_valid_name(user_name) and check_phone_number(user_phone_number) and check_valid_email(user_email)



# Path to db
path = "bysykkel.db"

ui.input_action_button("sub", "Submit")  
    
with ui.card():
    @render.text
    @reactive.event(input.sub)
    def data():
        if(check_all_inputs(input.user_name(), input.user_phone_number(), input.user_email())):
            d = {
                "user_name" : f"'{input.user_name()}'",
                "user_phone_number" : f"'{input.user_phone_number()}'",
                "user_email" : f"'{input.user_email()}'"
                }

            if(insert_to_table("user", d, path)):
                return f"User added \n user_name = {input.user_email()} \n user_phone_number = {input.user_phone_number()} \n user_email = {input.user_name()}"
            else:
                return "WTF"
        else:
            return "User not added, wrong input"

        




