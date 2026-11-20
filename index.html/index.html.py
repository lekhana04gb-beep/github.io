import os
import pandas as pd
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

FILE_NAME = "NC_Registration.xlsx"

# Function-wise responsibility mapping
responsibility_map = {
    "SMT": "Santosh",
    "QA": "Vidhyashree",
    "Production": "Karthik",
    "Maintenance": "Basavaraj",
    "Engineering": "Sujith",
    "Stores": "Prashanth"
}

# Generate NC Number
def generate_nc_number():
    year = 2026
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME)
            count = len(df) + 1
        except Exception:
            count = 1
    else:
        count = 1
    return f"NC-{year}-{count:03d}"

# Widgets Setup
style = {'description_width': '130px'}
layout = widgets.Layout(width='450px')

nc_no_widget = widgets.Text(value=generate_nc_number(), description="NC Number:", disabled=True, style=style, layout=layout)

current_date = datetime.now()
date_widget = widgets.Text(value=current_date.strftime("%d-%m-%Y"), description="Date:", disabled=True, style=style, layout=layout)
month_widget = widgets.Text(value=current_date.strftime("%B"), description="Month:", disabled=True, style=style, layout=layout)
week_widget = widgets.Text(value=str(current_date.isocalendar()[1]), description="Week:", disabled=True, style=style, layout=layout)

customer_widget = widgets.Dropdown(options=["", "Bosch", "Continental", "Valeo", "Cummins", "Delphi"], description="Customer:", style=style, layout=layout)
model_widget = widgets.Text(description="Model:", style=style, layout=layout)
function_widget = widgets.Dropdown(options=[""] + list(responsibility_map.keys()), description="Function:", style=style, layout=layout)
stage_widget = widgets.Dropdown(options=["", "Incoming", "SPI", "Placement", "Reflow", "AOI", "Testing", "Packing"], description="Stage:", style=style, layout=layout)

observation_widget = widgets.Textarea(description="Observation:", style=style, layout=widgets.Layout(width='450px', height='80px'))
nc_category_widget = widgets.Dropdown(options=["", "Major", "Minor"], description="NC Category:", style=style, layout=layout)

sixm_widget = widgets.Dropdown(options=["", "Man", "Machine", "Method", "Material", "Measurement", "Mother Nature"], description="6M Category:", style=style, layout=layout)
sub_category_widget = widgets.Text(description="Sub Category:", style=style, layout=layout)
responsibility_widget = widgets.Text(description="Responsibility:", disabled=True, style=style, layout=layout)
raised_by_widget = widgets.Text(description="NC Raised By:", style=style, layout=layout)
action_widget = widgets.Textarea(description="Action Plan:", style=style, layout=widgets.Layout(width='450px', height='80px'))

save_btn = widgets.Button(description="Save Registration", button_style='success', layout=widgets.Layout(width='200px', margin='20px 0px 0px 140px'))
output_area = widgets.Output()

# Auto update responsibility when function changes
def on_function_change(change):
    func = change['new']
    responsibility_widget.value = responsibility_map.get(func, "")

function_widget.observe(on_function_change, names='value')

# Reset Form
def reset_form():
    curr = datetime.now()
    date_widget.value = curr.strftime("%d-%m-%Y")
    month_widget.value = curr.strftime("%B")
    week_widget.value = str(curr.isocalendar()[1])
    
    customer_widget.value = ""
    model_widget.value = ""
    function_widget.value = ""
    stage_widget.value = ""
    observation_widget.value = ""
    nc_category_widget.value = ""
    sixm_widget.value = ""
    sub_category_widget.value = ""
    responsibility_widget.value = ""
    raised_by_widget.value = ""
    action_widget.value = ""
    
    nc_no_widget.value = generate_nc_number()

# Save Data function
def on_save_clicked(b):
    with output_area:
        clear_output()
        if not customer_widget.value:
            display(HTML("<div style='color: red; font-weight: bold;'>Error: Please Select Customer</div>"))
            return
        
        data = {
            "NC Number": [nc_no_widget.value],
            "Date": [date_widget.value],
            "Month": [month_widget.value],
            "Week": [week_widget.value],
            "Customer": [customer_widget.value],
            "Model": [model_widget.value],
            "Function": [function_widget.value],
            "Stage": [stage_widget.value],
            "Observation": [observation_widget.value.strip()],
            "NC Category": [nc_category_widget.value],
            "6M Category": [sixm_widget.value],
            "Sub Category": [sub_category_widget.value],
            "Responsibility": [responsibility_widget.value],
            "NC Raised By": [raised_by_widget.value],
            "Action Plan": [action_widget.value.strip()]
        }
        
        df_new = pd.DataFrame(data)
        
        if os.path.exists(FILE_NAME):
            try:
                df_old = pd.read_excel(FILE_NAME)
                df_final = pd.concat([df_old, df_new], ignore_index=True)
            except Exception:
                df_final = df_new
        else:
            df_final = df_new
            
        df_final.to_excel(FILE_NAME, index=False)
        
        display(HTML(f"<div style='color: green; font-weight: bold;'>Success: {nc_no_widget.value} Saved Successfully!</div>"))
        reset_form()

save_btn.on_click(on_save_clicked)

# Build Form Layout
form = widgets.VBox([
    widgets.HTML("<h2>NC Registration System</h2>"),
    nc_no_widget,
    date_widget,
    month_widget,
    week_widget,
    customer_widget,
    model_widget,
    function_widget,
    stage_widget,
    observation_widget,
    nc_category_widget,
    sixm_widget,
    sub_category_widget,
    responsibility_widget,
    raised_by_widget,
    action_widget,
    save_btn,
    output_area
])

display(form)
