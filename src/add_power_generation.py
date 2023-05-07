from tkinter import *
from ttwidgets import TTButton
import json


class AddPowerGenerationWidget:

    def __init__(self):
        self.root = None
        self.label_entries_list = []
        self.button_entries_list = []
        self.checkbox_entries_list = []
        self.custom_entries_list = []
        self.row_buffer = 0  # to assign rows

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
        household_type_var = StringVar(self.root)
        household_type_var.set(household_type_options[0])
        household_type_label = Label(self.root, text=input['label_name'])
        household_type_dropdown = OptionMenu(self.root, household_type_var, *household_type_options)
        household_type_label.grid(row=self.row_buffer, column=0, sticky=W)
        household_type_dropdown.grid(row=self.row_buffer, column=1, sticky=W)
        self.label_entries_list.append((household_type_label, household_type_dropdown))
        self.update_row_buffer(1)

    def _add_label_entries(self, input):
        if len(input) > 0:
            self.label_entries_list = [
                (Label(self.root, text=label), Entry(self.root, textvariable=StringVar(self.root, value=default_text)))
                for label, default_text in input.items()
            ]

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
        type_options = []
        for t in bottom_input['checkbox_list']:
            type_options.append((t, 0))
        self.type_var_list = [IntVar() for _ in range(len(type_options))]
        for r, option in enumerate(type_options):
            check_button = Checkbutton(self.root, text=option[0], variable=self.type_var_list[r], onvalue=1, offvalue=0)
            check_button.grid(row=self.update_row_buffer(1), column=1, sticky=W)

        self.update_row_buffer(1)

    def _add_permanent_buttons(self, input):

        if 'perm_button_params' in input:
            for _, button_kwargs in input["perm_button_params"].items():
                forward_button = TTButton(self.root, command=self.parse_values, **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def _add_temp_buttons(self, input):
        #TODO: disable skip button when household is off-grid
        if 'temp_button_params' in input:
            for _, button_kwargs in input["temp_button_params"].items():
                forward_button = TTButton(self.root, command=self.parse_values, **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def parse_values(self):
        print(self.label_entries_list)

    def render(self, input):
        self.initialize_widget()
        self._add_form_title(input)
        # add entries with labels
        self._add_label_entries(input['header_inputs'])

        # add entries with labels
        self._add_dropdown(input['type_dropdown'])
        # add checkboxes with labels
        self._add_checkboxes(input["middle_checkboxes"], input["bottom_checkboxes"])

        # add permanent buttons
        self._add_permanent_buttons(input)
        self.root.mainloop()

    def power_generation_widget_trigger(self, input):
        self.initialize_widget()
        self._add_form_title(input)
        self._add_dropdown(input['type_dropdown'])
        self._add_label_entries(input['monthly_kWh_textbox'])
        self._add_label_entries(input['storage_kWh_textbox'])
        #self._add_temp_buttons(input)
        #self._add_label_entries(input)


        self._add_permanent_buttons(input)
        self._add_temp_buttons(input)
        self.root.mainloop()
