from tkinter import *
from ttwidgets import TTButton
from tkinter import messagebox
from database import DB

import json

class ApplianceAddForm:

    def __init__(self):
        self.root = None
        self.add_dropdown_entries_list = []
        self.row_buffer = 0 # to assign rows
        self.dropdown_vars = {}
        self.selected_type = "Air handler"
        self.selected_types = {}
        self.label_entries_list = []
        self.checkbox_entries_list = []

    def refresh_widget(self):
        self.root.destroy()
        self.root = Tk()
        # reset the member instance vars
        self.add_dropdown_entries_list = []
        self.row_buffer = 0 # to assign rows
        self.dropdown_vars = {}
        self.selected_types = {}
        self.label_entries_list = []
        self.checkbox_entries_list = []

    def initialize_widget(self):
        self.root = Tk()

    def render(self, input):
        if self.root is None:
            self.initialize_widget()
        else:
            self.refresh_widget()
        # render rows
        self.add_form_title(input)
        self.add_form_title2(input)
        self.add_dropdown_for_app_type(input)
        self.addManufactuerList()
        # self.add_dropdown(input['manufacturer_dropdown'])
        self.add_text_input(input['model_name'])
        self.add_text_input(input['waterHeater']['btuRating'])
        if self.selected_type == input["waterHeater"]["label_name"]:
            print("waterHeater selected")
            self.add_dropdown(input['waterHeater']['type_dropdown'])
            self.add_text_input(input['waterHeater']['capacity'])
            self.add_text_input(input['waterHeater']['temperature'])
        else:
            print("air handler selected")
            self.add_form_checkboxes(input['airHandler'])
            self.add_text_input(input['airHandler']['energyEfficiencyRatio'])
            self.add_dropdown(input['airHandler']['energySource_dropdown'])
            self.add_text_input(input['airHandler']['hspf'])
            self.add_text_input(input['airHandler']['seer'])

        self.add_permanent_buttons(input)
        self.root.mainloop()

    def addManufactuerList(self):
        db = DB()
        sql = "SELECT manufacturerName FROM Manufacturer"
        result = db.fetch(sql, None)

        if not result:
            messagebox.showerror("Error", "Invalid postal code")
            return False

        dropdown_list = [row[0] for row in result]

        json_data = {
            "dropdown_list": dropdown_list,
            "label_name": "Manufacturer: "
        }
        print(json_data)
        self.add_dropdown(json_data)

    def update_row_buffer(self, buffer):
        self.row_buffer += buffer
        return self.row_buffer

    def add_form_title(self, input):
        label = Label(self.root, text=input["title"], font=("Helvetica", 16, "bold"), anchor="w")
        label.grid(row=self.row_buffer, column=0, columnspan=2)
        self.update_row_buffer(1)

    def add_form_title2(self, input):
        label = Label(self.root, text=input["title2"], font=("Helvetica", 13, "bold"), anchor="w")
        label.grid(row=self.row_buffer, column=0, columnspan=2, sticky="w")
        self.update_row_buffer(1)

    def add_dropdown(self, input):
        key = input['label_name']
        options = input['dropdown_list']
        self.dropdown_vars[key] = StringVar(self.root)
        self.dropdown_vars[key].set(options[0])
        label = Label(self.root, text=input['label_name'])
        dropdown = OptionMenu(self.root, self.dropdown_vars[key], *options, command=lambda selected_option, k=key: self.on_dropdown_select(selected_option, k))
        label.grid(row=self.row_buffer, column=0, sticky=W)
        dropdown.grid(row=self.row_buffer, column=1, sticky=W)
        self.add_dropdown_entries_list.append((label, dropdown))
        self.update_row_buffer(1)

    def on_dropdown_select(self, selected_option, key):
        self.selected_types[key] = selected_option
        print(f"_on_dropdown_select for {key}: " + self.selected_types[key])

    def add_dropdown_for_app_type(self, input):
        key = "airHandler"
        options = input['type_dropdown']['dropdown_list']
        self.dropdown_vars[key] = StringVar(self.root)
        if self.selected_type is None:
            self.dropdown_vars[key].set(options[0])
        else:
            self.dropdown_vars[key].set(self.selected_type)
        self.dropdown_vars[key].trace("w", lambda *args: self.update_select_var(self.dropdown_vars[key], input))
        label = Label(self.root, text=input['type_dropdown']['label_name'])
        dropdown = OptionMenu(self.root, self.dropdown_vars[key], *options)
        label.grid(row=self.row_buffer, column=0, sticky=W)
        dropdown.grid(row=self.row_buffer, column=1, sticky=W)
        self.add_dropdown_entries_list.append((label, dropdown))
        self.update_row_buffer(1)
        
    def update_select_var(self, var, input):
        self.selected_type = var.get()
        self.render(input)
        print("current type: " +  self.selected_type)

    def add_text_input(self, input):
        input_field = Entry(self.root)
        input_field.grid(row=self.row_buffer, column=1, columnspan=2, padx=10, pady=0, sticky="w")
        label_input = Label(self.root, text=input['label_name'])
        label_input.grid(row=self.row_buffer, column=0, sticky="w")
        self.label_entries_list.append((label_input, input_field))
        self.update_row_buffer(1)

    def add_form_checkboxes(self, input):
        label = Label(self.root, text=input["label_name"], font=("Helvetica", 13, "bold"), anchor="w")
        label.grid(row=self.row_buffer, column=0, columnspan=2, sticky="w")
        self.update_row_buffer(1)
        self.checkbox_entries_list = []
        for appliance_type in input["middle_checkboxes"]:
            var = IntVar()
            self.checkbox_entries_list.append((appliance_type,var))
            checkbox = Checkbutton(self.root, text=appliance_type, variable=var)
            checkbox.grid(row=self.row_buffer, column=0, columnspan=2, sticky="w")
            self.update_row_buffer(1)

    def add_permanent_buttons(self, input):
        if 'perm_button_params' in input:
            for _, button_kwargs in input["perm_button_params"].items():
                forward_button = TTButton(self.root, command=self.parse_value, **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def parse_value(self):
        f = open('output/household_form_output.json')
        data = json.load(f)
        D = data
        for key, var in self.dropdown_vars.items():
            if key in self.selected_types:
                D[key] = self.selected_types[key]
            else:
                D[key] = var.get()

        D["selected_type"] = self.selected_type

        for label_entry in self.label_entries_list:
            print(label_entry)
            label_text = label_entry[0]['text']
            D[label_text] = label_entry[1].get()

        for checkbox in self.checkbox_entries_list:
            label = checkbox[0]
            checkbutton_value = checkbox[1].get()
            D[label] = {"checkbutton_value": checkbutton_value}

        print(json.dumps(D, indent=4))
        if self.save(D):
            self.openNext()

    def save(self, input_json):
        # Extract input values
        email = input_json['email address']
        btuRating = input_json['BTU rating']
        selected_type = input_json['selected_type']
        manufacturer_name = input_json['Manufacturer: ']
        energy_source = input_json['Energy source: ']
        model_name = input_json['Model name: ']
        if selected_type == "Air handler":
            eer = input_json.get('Energy efficiency ratio: ', None)
            hspf = input_json.get('hspf: ', None)
            seer = input_json.get('seer: ', None)
            if not (eer and hspf and seer):
                messagebox.showerror("Error", "Failed get right data.")
                return False
            heater_checkbutton = input_json['Heater']['checkbutton_value']
            ac_checkbutton = input_json['Air conditioner']['checkbutton_value']
            hp_checkbutton = input_json['Heat pump']['checkbutton_value']
        if selected_type == "Water heater":
            current_temperature = int(input_json["Temperature"])
            capacity = float(input_json["Capacity (gallons)"])

        # Validate inputs
        if not email or not email.strip():
            messagebox.showerror("Error", "Email address is required.")
            return False
        if not manufacturer_name or not manufacturer_name.strip():
            messagebox.showerror("Error", "Manufacturer name is required.")
            return False
        if not energy_source or not energy_source.strip():
            messagebox.showerror("Error", "Energy source is required.")
            return False
        if not model_name or not model_name.strip():
            messagebox.showerror("Error", "Model name is required.")
            return False
        if selected_type == "Air handler" and hp_checkbutton and (not hspf or not hspf.strip() or not seer or not seer.strip()):
            messagebox.showerror("Error", "HSPF and SEER are required for heat pumps.")
            return False
        if selected_type == "Air handler" and ac_checkbutton and (not eer or not eer.strip()):
            messagebox.showerror("Error", "Energy efficiency ratio is required for air conditioners.")
            return False
        if selected_type == "Air handler" and heater_checkbutton and (not energy_source or not energy_source.strip()):
            messagebox.showerror("Error", "Energy_source is required for heater.")
            return False
        db = DB()
        try:
            # Insert values into Appliances table
            query = "INSERT INTO Appliances (emailId, model, btuRating, manufacturerName, atype) VALUES (%s, %s, %s, %s, %s)"
            args = (email, model_name, btuRating, manufacturer_name, selected_type)
            print(args)
            system_input_order = db.insert(query, args)

            # Insert values into corresponding tables based on selected checkboxes
            if selected_type == "Air handler":
                query = "INSERT INTO AirHandler (emailId, systemInputOrder) VALUES (%s, %s)"
                db.insert(query, (email, system_input_order))

            if selected_type == "Air handler" and ac_checkbutton and eer:
                query = "INSERT INTO AirConditioner (emailId, systemInputOrder, energyEfficiencyRatio) VALUES (%s, %s, %s)"
                db.insert(query, (email, system_input_order, eer))

            if selected_type == "Air handler" and heater_checkbutton and energy_source:
                query = "INSERT INTO Heater (emailId, systemInputOrder, energySource) VALUES (%s, %s, %s)"
                db.insert(query, (email, system_input_order, energy_source))

            if selected_type == "Air handler" and hp_checkbutton and hspf and seer:
                query = "INSERT INTO HeatPump (emailId, systemInputOrder, hspf, seer) VALUES (%s, %s, %s, %s)"
                db.insert(query, (email, system_input_order, hspf, seer))

            if selected_type == "Water heater" and current_temperature and capacity and energy_source: 
                query = "INSERT INTO WaterHeater (emailId, systemInputOrder, capacity, currentTemperature, energySource) VALUES (%s, %s, %s, %s, %s)"
                args = (email, system_input_order, capacity, current_temperature, energy_source)
                db.insert(query, args)

        except Exception as e:
            print("MySQL Error: ", str(e))
            messagebox.showerror("Error", "Failed to save data to database.")
            return False
        return True
        
    def openNext(self):
        self.root.withdraw()
        # self.root = None
        from listing_appliance_form import ApplianceListForm
        f = open('input/listing_appliance_input.json')
        data = json.load(f)
        f.close()
        widget = ApplianceListForm()
        widget.render(data)
   
