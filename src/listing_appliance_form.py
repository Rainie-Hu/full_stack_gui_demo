from tkinter import *
from tkinter import ttk
from ttwidgets import TTButton
from tkinter import messagebox
from database import DB
import json

class ApplianceListForm:

    def __init__(self):
        self.root = None
        self.selected_type = None
        self.add_dropdown_entries_list = []
        self.row_buffer = 0 # to assign rows
        self.input = None

    def refresh_widget(self):
        self.root.destroy()
        self.root = Tk()

    def initialize_widget(self):
        self.root = Tk()

    def render(self, input):
        self.input = input
        if self.root is None:
            self.initialize_widget()
        else:
            self.refresh_widget()

        # render rows
        self.add_form_title(input)
        self.add_form_title2(input)
        self.add_permanent_buttons(input)
        self.add_appliance_table(input)
        self.add_hyperlink_to_add_appliance(input)
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

    def add_permanent_buttons(self, input):
        if 'perm_button_params' in input:
            for _, button_kwargs in input["perm_button_params"].items():
                forward_button = TTButton(self.root, command=self.go_next_page, **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def add_appliance_table(self, input):
        columns = input["table"]["columns"]
#        data = input["table"]["sampleData"]
        
        # Execute the SQL query to retrieve all the appliances
        db = DB()
        sql = "SELECT systemInputOrder, atype, manufacturerName, model FROM Appliances ORDER BY systemInputOrder ASC"
        result = db.fetch(sql)
        data = [[str(row[0]), row[1], row[2], row[3]] for row in result]

        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)
              
        for row in data:
            tree.insert("", "end", values=row)
        # Bind double-click event to the Treeview
        tree.bind("<Double-1>", self.on_row_double_click)
        tree.grid(row=self.row_buffer, column=0, columnspan=2)
        self.update_row_buffer(5) # would be number of rows from mysql instead of 5

    def on_row_double_click(self, event):
        # Get the selected row data
        selected_item = event.widget.selection()[0]
        row_data = event.widget.item(selected_item, 'values')
        
        # Create a popup dialog to confirm deletion
        result = messagebox.askyesno("Confirm", "Are you sure you want to delete this appliance?")
        if result:
            # Call delete_appliance method
            self.delete_appliance(row_data)

    def delete_appliance(self, row):
        db = DB()
        sql = "DELETE FROM Appliances WHERE systemInputOrder = %s"
        args = (row[0],) 
        cursor = db.query(sql, args)
        cursor.close()
        db.connection.commit()
        messagebox.showinfo("Success", "Appliance deleted successfully.")
        self.render(self.input)

    def add_hyperlink_to_add_appliance(self, input):
        hyperlink_label = Label(self.root, text=input['hyperlink'], fg="blue", cursor="hand2")
        hyperlink_label.grid(row=self.row_buffer, column=0, columnspan=2, pady=10)
        hyperlink_label.bind("<Button-1>", self.go_to_add_appliance)

    def go_next_page(self):
        print("ddd")
        # self.root.destroy()
        # from adding_appliance_form import ApplianceAddForm
        # f = open('input/add_appliance_input.json')
        # data = json.load(f)
        # f.close()
        # widget = ApplianceAddForm()
        # widget.render(data)

    def go_to_add_appliance(self, event):
        self.root.withdraw()
        # self.root = None
        from adding_appliance_form import ApplianceAddForm
        f = open('input/add_appliance_input.json')
        data = json.load(f)
        f.close()
        widget = ApplianceAddForm()
        widget.render(data)