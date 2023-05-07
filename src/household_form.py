from tkinter import *
from ttwidgets import TTButton
from tkinter import messagebox
import json
from database import DB

class HouseHoldWidget:

    def __init__(self):
        self.root = None
        self.row_buffer = 0
        self.dropdown_var = None
        self.selected_household_type = None
        self.check_var_list = []
        self.checkbox_entries_list = []
        self.label_entries_list = []
        self.type_var_list = []
        self.bottom_input_checkboxes = []

    def refresh_widget(self):
        self.root.destroy()
        self.root = Tk()

    def initialize_widget(self):
        self.root = Tk()

    def update_row_buffer(self, buffer):
        self.row_buffer += buffer
        return self.row_buffer

    def _add_form_title(self, input):
        label = Label(self.root, text=input["title"], font=("Helvetica", 16, "bold"), anchor="w")
        label.grid(row=self.row_buffer, column=0, columnspan=2)
        self.update_row_buffer(1)

    def _add_dropdown(self, input):
        # Add household type dropdown
        household_type_options = input['dropdown_list']
        self.dropdown_var = StringVar(self.root)
        self.dropdown_var.set(household_type_options[0])
        household_type_label = Label(self.root, text=input['label_name'])
        household_type_dropdown = OptionMenu(self.root, self.dropdown_var, *household_type_options, command=self._on_dropdown_select)
        household_type_label.grid(row=self.row_buffer, column=0, sticky=W)
        household_type_dropdown.grid(row=self.row_buffer, column=1, sticky=W)
        self.update_row_buffer(1)

    def _on_dropdown_select(self, selected_option):
        self.selected_household_type = selected_option
        print("_on_dropdown_select: " + self.selected_household_type)

    def _add_label_entries(self, input):
        if len(input) > 0:
            for label, default_text in input.items():
                tup = (Label(self.root, text=label), 
                 Entry(self.root, textvariable=StringVar(self.root, value=default_text)))
                self.label_entries_list.append(tup)

            for r, label_entry in enumerate(self.label_entries_list):
                label_entry[0].grid(row=r + self.row_buffer, sticky=W)
                label_entry[1].grid(row=r + self.row_buffer, column=1, ipadx=50)
            self.update_row_buffer(len(self.label_entries_list))

    def _add_checkboxes(self, input, bottom_input):
        if len(input) > 0:
            def onPress(label):
                input[label] = not input[label]
            self.check_var_list = [IntVar() for i in range(len(input.keys()))]
            self.checkbox_entries_list = [
                [
                    (label[0], check_var),
                    Label(self.root, text=label[0]),
                    Entry(self.root, textvariable=StringVar(self.root, value=''), width=5),
                    Label(self.root, text="No " + label[0]),
                    Checkbutton(self.root, onvalue=1, offvalue=0,
                                variable=check_var)
                ]
                for label, check_var in zip(input.items(), self.check_var_list)
            ]

        for r, checkbox in enumerate(self.checkbox_entries_list):
            checkbox[1].grid(row=r + self.row_buffer, sticky=W)
            checkbox[2].grid(row=r + self.row_buffer, column=1, sticky=W)
            checkbox[3].grid(row=r + self.row_buffer, column=2, sticky=W)
            checkbox[4].grid(row=r + self.row_buffer, column=3, sticky=W)
        self.update_row_buffer(len(self.checkbox_entries_list))

        label = Label(self.root, text=bottom_input['label'])
        label.grid(row=self.row_buffer, sticky=W)        
        self.bottom_input_checkboxes = []
        for t in bottom_input['checkbox_list']:
            checkbox_var = IntVar()
            self.bottom_input_checkboxes.append((t, checkbox_var))
            check_button = Checkbutton(self.root, text=t, variable=checkbox_var, onvalue=1, offvalue=0)
            check_button.grid(row=self.update_row_buffer(1), column=1, sticky=W)

        self.update_row_buffer(1)
   
    def _add_permanent_buttons(self, input):

        if 'perm_button_params' in input:
            for _, button_kwargs in input["perm_button_params"].items():
                forward_button = TTButton(self.root, command=self.parse_values, **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])
   
    def parse_values(self):
        D = {}
        if self.label_entries_list is not None:
            l_e_len = len(self.label_entries_list)
            for l in range(l_e_len):
                label_tx = self.label_entries_list[l][0].cget("text")
                entry_tx = self.label_entries_list[l][1].get()
                D[label_tx] = entry_tx

        for checkbox in self.checkbox_entries_list:
            label = checkbox[0][0]
            entry_value = checkbox[2].get()
            checkbutton_value = checkbox[0][1].get()
            D[label] = {"entry value": entry_value, "checkbutton_value": checkbutton_value}

        if self.selected_household_type is not None:
            D["type_dropdown"] = self.selected_household_type
        else:
            D["type_dropdown"] = self.dropdown_var.get()

        for checkbox in self.bottom_input_checkboxes:
            label = checkbox[0]
            checkbutton_value = checkbox[1].get()
            D[label] = {"checkbutton_value": checkbutton_value}

        print(json.dumps(D, indent=4))
        with open('output/household_form_output.json', 'w') as fp:
            json.dump(D, fp)
        if self.save(D):
            self.openNext()
        

    def render(self, input):
        self.initialize_widget()
        self._add_form_title(input)
        # add entries with labels
        self._add_label_entries(input['header_inputs'])

        # add entries with labels
        self._add_dropdown(input['type_dropdown'])

        self._add_label_entries(input['middle_inputs'])

        # add checkboxes with labels
        self._add_checkboxes(input["middle_checkboxes"], input["bottom_checkboxes"])

        # add permanent buttons
        self._add_permanent_buttons(input)
        self.root.mainloop()

    def openNext(self):
        self.root.withdraw()
        self.root = None
        from adding_appliance_form import ApplianceAddForm
        f = open('input/add_appliance_input.json')
        data = json.load(f)
        f.close()
        widget = ApplianceAddForm()
        widget.render(data)

    def save(self, input_json):
        email_id = input_json['email address']
        square_footage = input_json['squarefootage_inputs']
        household_type = input_json['type_dropdown']
        regular_cooling_thermostat_setting = input_json['cooling']['entry value']
        regular_cooling_thermostat_enabled = input_json['cooling']['checkbutton_value']
        regular_heating_thermostat_setting = input_json['heating']['entry value']
        regular_heating_thermostat_enabled = input_json['heating']['checkbutton_value']
        electric = input_json['electric']['checkbutton_value']
        gas = input_json['gas']['checkbutton_value']
        steam = input_json['steam']['checkbutton_value']
        fuel_oil = input_json['fuel oil']['checkbutton_value']

        postal_code = input_json['postal code']

        # email_id validation
        if not email_id:
            messagebox.showerror("Error", "Email address cannot be empty")
            return False

        # Check if regular_cooling_thermostat_setting is an integer
        if not square_footage or not square_footage.isdigit():
            messagebox.showerror("Error", "Square_footage must be an integer and exists")
            return False

        # Check if regular_cooling_thermostat_setting is an integer
        if not regular_cooling_thermostat_enabled and not regular_cooling_thermostat_setting.isdigit():
            messagebox.showerror("Error", "Regular cooling thermostat setting must be an integer")
            return False
        
        # Check if regular_cooling_thermostat_setting is empty if regular_cooling_thermostat_enabled is 0
        if not regular_cooling_thermostat_enabled and not regular_cooling_thermostat_setting:
            messagebox.showerror("Error", "Regular cooling thermostat setting cannot be empty")
            return False
        
        # Check if regular_heating_thermostat_setting is an integer
        if not regular_heating_thermostat_enabled and not regular_heating_thermostat_setting.isdigit():
            messagebox.showerror("Error", "Regular heating thermostat setting must be an integer")
            return False
        
        # Check if regular_heating_thermostat_setting is empty if regular_heating_thermostat_enabled is 0
        if not regular_heating_thermostat_enabled and not regular_heating_thermostat_setting:
            messagebox.showerror("Error", "Regular heating thermostat setting cannot be empty")
            return False

        # Check if postal_code is empty
        if not postal_code:
            messagebox.showerror("Error", "Postal code cannot be empty")
            return False

        if regular_cooling_thermostat_enabled:
            regular_cooling_thermostat_setting = None

        if regular_heating_thermostat_enabled:
            regular_heating_thermostat_setting = None

        db = DB()

        # Check if postal_code exists
        sql = "SELECT postalCode FROM PostalCode WHERE postalCode = %s"
        result = db.fetchone(sql, (postal_code,))

        if not result:
            messagebox.showerror("Error", "Invalid postal code")
            return False

         # Check if emailId exists
        sql = "SELECT emailId FROM Household WHERE emailId=%s"
        result = db.fetchone(sql, (email_id,))
        if result:
            messagebox.showerror("Error", "Email address already exists in database")
            return

        sql = """INSERT INTO Household
        (emailId, squareFootage, householdType, regularCoolingThermostatSetting,
         regularHeatingThermostatSetting, postalCode)
         VALUES (%s, %s, %s, %s, %s, %s)"""

        args = (email_id, square_footage, household_type, regular_cooling_thermostat_setting,
        regular_heating_thermostat_setting, postal_code)
        print(args)

        result = db.insert(sql, args)
        print(result)
        # Check if postal_code exists
        sql = "SELECT emailId FROM Household WHERE emailId=%s"
        result = db.fetchone(sql, (email_id,))
        if not result:
            messagebox.showerror("Error", "Insertion Failed")
            return False

        # Insert data into HouseholdPublicUtilities table
        if electric:
            public_utility_sql = """INSERT INTO HouseholdPublicUtilities (emailId, publicUtilities)
                                    VALUES (%s, %s)"""
            public_utility_args = (email_id, 'Electric')
            db.insert(public_utility_sql, public_utility_args)

        if gas:
            public_utility_sql = """INSERT INTO HouseholdPublicUtilities (emailId, publicUtilities)
                                    VALUES (%s, %s)"""
            public_utility_args = (email_id, 'Gas')
            db.insert(public_utility_sql, public_utility_args)

        if steam:
            public_utility_sql = """INSERT INTO HouseholdPublicUtilities (emailId, publicUtilities)
                                    VALUES (%s, %s)"""
            public_utility_args = (email_id, 'Steam')
            db.insert(public_utility_sql, public_utility_args)

        if fuel_oil:
            public_utility_sql = """INSERT INTO HouseholdPublicUtilities (emailId, publicUtilities)
                                    VALUES (%s, %s)"""
            public_utility_args = (email_id, 'Fuel Oil')
            db.insert(public_utility_sql, public_utility_args)

        return True

        