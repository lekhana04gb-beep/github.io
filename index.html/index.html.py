import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import os

FILE_NAME = "NC_Registration.xlsx"

# Function wise responsibility mapping
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
        df = pd.read_excel(FILE_NAME)
        count = len(df) + 1
    else:
        count = 1

    return f"NC-{year}-{count:03d}"

# Update Responsibility Automatically
def update_responsibility(event=None):
    function = function_var.get()
    responsibility_var.set(
        responsibility_map.get(function, "")
    )

# Reset Form After Save
def reset_form():

    current_date = datetime.now()

    date_var.set(
        current_date.strftime("%d-%m-%Y")
    )

    month_var.set(
        current_date.strftime("%B")
    )

    week_var.set(
        str(current_date.isocalendar()[1])
    )

    customer_var.set("")
    model_var.set("")
    function_var.set("")
    stage_var.set("")
    nc_category_var.set("")
    sixm_var.set("")
    sub_category_var.set("")
    responsibility_var.set("")
    raised_by_var.set("")

    observation_text.delete("1.0", tk.END)
    action_text.delete("1.0", tk.END)

# Save Data
def save_data():

    if customer_var.get() == "":
        messagebox.showerror(
            "Error",
            "Please Select Customer"
        )
        return

    data = {
        "NC Number": [nc_no_var.get()],
        "Date": [date_var.get()],
        "Month": [month_var.get()],
        "Week": [week_var.get()],
        "Customer": [customer_var.get()],
        "Model": [model_var.get()],
        "Function": [function_var.get()],
        "Stage": [stage_var.get()],
        "Observation": [
            observation_text.get("1.0", tk.END).strip()
        ],
        "NC Category": [nc_category_var.get()],
        "6M Category": [sixm_var.get()],
        "Sub Category": [sub_category_var.get()],
        "Responsibility": [responsibility_var.get()],
        "NC Raised By": [raised_by_var.get()],
        "Action Plan": [
            action_text.get("1.0", tk.END).strip()
        ]
    }

    df_new = pd.DataFrame(data)

    if os.path.exists(FILE_NAME):
        df_old = pd.read_excel(FILE_NAME)
        df_final = pd.concat(
            [df_old, df_new],
            ignore_index=True
        )
    else:
        df_final = df_new

    df_final.to_excel(
        FILE_NAME,
        index=False
    )

    messagebox.showinfo(
        "Success",
        f"{nc_no_var.get()} Saved Successfully"
    )

    nc_no_var.set(generate_nc_number())
    reset_form()

# Main Window
root = tk.Tk()
root.title("NC Registration System")
root.geometry("900x750")

# Auto Date / Month / Week
current_date = datetime.now()

# Variables
nc_no_var = tk.StringVar(
    value=generate_nc_number()
)

date_var = tk.StringVar(
    value=current_date.strftime("%d-%m-%Y")
)

month_var = tk.StringVar(
    value=current_date.strftime("%B")
)

week_var = tk.StringVar(
    value=str(current_date.isocalendar()[1])
)

customer_var = tk.StringVar()
model_var = tk.StringVar()
function_var = tk.StringVar()
stage_var = tk.StringVar()
nc_category_var = tk.StringVar()
sixm_var = tk.StringVar()
sub_category_var = tk.StringVar()
responsibility_var = tk.StringVar()
raised_by_var = tk.StringVar()

row = 0

# NC Number
tk.Label(root, text="NC Number").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=nc_no_var,
    state="readonly",
    width=35
).grid(row=row, column=1)

row += 1

# Date
tk.Label(root, text="Date").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=date_var,
    state="readonly",
    width=35
).grid(row=row, column=1)

row += 1

# Month
tk.Label(root, text="Month").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=month_var,
    state="readonly",
    width=35
).grid(row=row, column=1)

row += 1

# Week
tk.Label(root, text="Week").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=week_var,
    state="readonly",
    width=35
).grid(row=row, column=1)

row += 1

# Customer
tk.Label(root, text="Customer").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

ttk.Combobox(
    root,
    textvariable=customer_var,
    width=32,
    values=[
        "Bosch",
        "Continental",
        "Valeo",
        "Cummins",
        "Delphi"
    ]
).grid(row=row, column=1)

row += 1

# Model
tk.Label(root, text="Model").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=model_var,
    width=35
).grid(row=row, column=1)

row += 1

# Function
tk.Label(root, text="Function").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

function_combo = ttk.Combobox(
    root,
    textvariable=function_var,
    width=32,
    values=[
        "SMT",
        "QA",
        "Production",
        "Maintenance",
        "Engineering",
        "Stores"
    ]
)

function_combo.grid(row=row, column=1)
function_combo.bind(
    "<<ComboboxSelected>>",
    update_responsibility
)

row += 1

# Stage
tk.Label(root, text="Stage").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

ttk.Combobox(
    root,
    textvariable=stage_var,
    width=32,
    values=[
        "Incoming",
        "SPI",
        "Placement",
        "Reflow",
        "AOI",
        "Testing",
        "Packing"
    ]
).grid(row=row, column=1)

row += 1

# Observation
tk.Label(root, text="Observation").grid(
    row=row, column=0, padx=10, pady=5, sticky="nw"
)

observation_text = tk.Text(
    root,
    height=4,
    width=40
)

observation_text.grid(
    row=row,
    column=1
)

row += 1

# NC Category
tk.Label(root, text="NC Category").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

ttk.Combobox(
    root,
    textvariable=nc_category_var,
    width=32,
    values=[
        "Major",
        "Minor"
    ]
).grid(row=row, column=1)

row += 1

# 6M Category
tk.Label(root, text="6M Category").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

ttk.Combobox(
    root,
    textvariable=sixm_var,
    width=32,
    values=[
        "Man",
        "Machine",
        "Method",
        "Material",
        "Measurement",
        "Mother Nature"
    ]
).grid(row=row, column=1)

row += 1

# Sub Category
tk.Label(root, text="Sub Category").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=sub_category_var,
    width=35
).grid(row=row, column=1)

row += 1

# Responsibility
tk.Label(root, text="Responsibility").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=responsibility_var,
    state="readonly",
    width=35
).grid(row=row, column=1)

row += 1

# NC Raised By
tk.Label(root, text="NC Raised By").grid(
    row=row, column=0, padx=10, pady=5, sticky="w"
)

tk.Entry(
    root,
    textvariable=raised_by_var,
    width=35
).grid(row=row, column=1)

row += 1

# Action Plan
tk.Label(root, text="Action Plan").grid(
    row=row, column=0, padx=10, pady=5, sticky="nw"
)

action_text = tk.Text(
    root,
    height=4,
    width=40
)

action_text.grid(
    row=row,
    column=1
)

row += 1

# Save Button
tk.Button(
    root,
    text="Save Registration",
    bg="green",
    fg="white",
    font=("Arial", 11, "bold"),
    command=save_data
).grid(
    row=row,
    column=1,
    pady=20
)

root.mainloop()