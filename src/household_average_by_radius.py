from tkinter import * 
from tkinter import ttk
from ttwidgets import TTButton
import json
import utilityClass

class householdAverageByRadius:

    def __init__(self):
        self.root = None
        self.selected_radius = None
        self.add_dropdown_entries_list = []
        self.row_buffer = 0 # to assign rows
        self.DB = utilityClass.mySqlDB()

    def refresh_widget(self):
        self.root.destroy()
        self.root = Tk()

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
        self.add_text_input(input['postal_code'])     
        self.button = Button(self.root, text="Validate postal code", command=self.validate_input)
        self.button.grid(row=self.row_buffer - 1, column=2, sticky="w")
        # self.input_field.bind("<FocusOut>", self.validate_input) 
        self.add_search_radius_dropdown(input)
        # self.add_permanent_buttons(input)
        self._add_table(input["housdhold_average table"])
        self.root.mainloop()

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

    def add_text_input(self, input):
        self.postal_code_input = Entry(self.root)
        self.postal_code_input.grid(row=self.row_buffer, column=1, columnspan=2, padx=10, pady=0, sticky="w")
        label_input = Label(self.root, text=input['label_name'])
        label_input.grid(row=self.row_buffer, column=0, sticky="w")
        self.update_row_buffer(1)

    def add_dropdown(self, input):
        options = input['dropdown_list']
        var = StringVar(self.root)
        var.set(options[0])
        label = Label(self.root, text=input['label_name'])
        dropdown = OptionMenu(self.root, var, *options)
        label.grid(row=self.row_buffer, column=0, sticky=W)
        dropdown.grid(row=self.row_buffer, column=1, sticky=W)
        self.add_dropdown_entries_list.append((label, dropdown))
        self.update_row_buffer(1)

    def add_search_radius_dropdown(self, input):
        options = input['search_radius dropdown']['dropdown_list']
        self.Selection = StringVar(self.root)
        if self.selected_radius is None:
            self.Selection.set(options[0])
        else:
            self.Selection.set(self.selected_radius)
        self.Selection.trace("w", lambda *args: self.update_select_var_and_refresh_treeview(self.Selection, input))
        label = Label(self.root, text=input['search_radius dropdown']['label_name'])
        dropdown = OptionMenu(self.root, self.Selection, *options)
        label.grid(row=self.row_buffer, column=0, sticky=W)
        dropdown.grid(row=self.row_buffer, column=1, sticky=W)
        self.add_dropdown_entries_list.append((label, dropdown))
        self.update_row_buffer(1)

        
    def update_select_var_and_refresh_treeview(self, var, input):
        self.selected_radius = var.get()
        print("current radius: " +  self.selected_radius)
        self.refresh_treeview(input['query_list'])

    def _add_table(self, dict):
        if 'table_param' in dict:
            table_dict = dict['table_param']
            self.my_tree = ttk.Treeview(self.root, height=10)
            self.my_tree['columns'] = table_dict['columns']
            self.my_tree.column("#0",width=0,stretch=NO)
            for idx, _ in enumerate(table_dict['columns']):
                self.my_tree.column(table_dict['columns'][idx], width=table_dict['width'],minwidth=table_dict['minwidth'],anchor=table_dict['anchor'])
            for idx, _ in enumerate(table_dict['columns']):
                self.my_tree.heading(table_dict['columns'][idx], text=table_dict['columns'][idx],anchor=table_dict['anchor'])
            for idx, _ in enumerate(table_dict['rows']):
                self.my_tree.insert(parent='',index='end',iid=idx,values=tuple(table_dict['rows'][idx]))  
            # my_tree.pack(pady=0.1)
            self.my_tree.grid(row=self.row_buffer, column=1, columnspan=2, padx=10, pady=0, sticky="w")
            scrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.my_tree.yview)
            self.my_tree.configure(yscroll=scrollbar.set)
            self.update_row_buffer(1)

    def validate_input(self):
        input = self.postal_code_input.get()
        res = self.DB.fetch('select postalcode from postalcode;')
        postal_code_list = [row[0] for row in res]
        if hasattr(self, "error_label"):
            self.error_label.destroy()
        if input not in postal_code_list:    
            self.error_label = Label(self.root, fg="red")
            self.error_label.config(text="Error: Input must be valid postal code")
            self.error_label.grid(row=self.row_buffer, column=1, columnspan=2, padx=10, pady=0, sticky="w")
        else:
            self.error_label = Label(self.root, fg="blue")
            self.error_label.config(text="Success: Input is a valid postal code")
            self.error_label.grid(row=self.row_buffer, column=1, columnspan=2, padx=10, pady=0, sticky="w")
            # self.error_label.grid_forget()

    def refresh_treeview(self, sql_list):
        for row in self.my_tree.get_children():
            # print("row delete")
            self.my_tree.delete(row)
        
        # Get the current selection from the dropdown
        current_selection = self.Selection.get()
        print(sql_list[0].format(self.postal_code_input.get(),int(current_selection),int(current_selection),int(current_selection)))
        # print(current_selection)

        res = self.DB.fetch(sql_list[0].format('"'+self.postal_code_input.get()+'"',int(current_selection),int(current_selection),int(current_selection)))
        # Insert new rows with updated data based on the current selection
        print(res)
        self.my_tree.insert("", END, values=("Household Count", res[0][0]))
        self.my_tree.insert("", END, values=("House Count", res[0][1]))
        self.my_tree.insert("", END, values=("Apartment Count", res[0][2]))
        self.my_tree.insert("", END, values=("Townhome Count", res[0][3]))
        self.my_tree.insert("", END, values=("Condominum Count", res[0][4]))
        self.my_tree.insert("", END, values=("Mobilehome Count", res[0][5]))
        self.my_tree.insert("", END, values=("Average Square Footage", res[0][6]))
        self.my_tree.insert("", END, values=("Average Cooling Temperature", res[0][7]))
        self.my_tree.insert("", END, values=("Average Heating Temperature", res[0][8]))
        self.my_tree.insert("", END, values=("Public Utilities", res[0][9]))
        self.my_tree.insert("", END, values=("Off-the-grid Count", res[0][10]))
        self.my_tree.insert("", END, values=("With Power Generation Count", res[0][11]))
        self.my_tree.insert("", END, values=("Average Monthly Kwh", res[0][12]))
        self.my_tree.insert("", END, values=("With Battery Storage Count", res[0][13]))
        self.my_tree.insert("", END, values=("Most Common Generator", res[0][14]))
