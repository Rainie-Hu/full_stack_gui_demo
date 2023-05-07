from tkinter import *
from tkinter import ttk
from ttwidgets import TTButton
import json


class PowerGenerationListForm:

	def __init__(self):
		self.root = None
		self.selected_type = None
		self.add_dropdown_entries_list = []
		self.row_buffer = 0  # to assign rows

	def refresh_widget(self):
		self.root.destroy()
		self.root = Tk()

	def initialize_widget(self):
		self.root = Tk()

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
				forward_button = TTButton(self.root, command=self.go_to_add_power_generation(), **button_kwargs['button'])
				forward_button.grid(**button_kwargs['grid'])

	def go_to_add_power_generation(self):
		print("TODO: I will go to power_generation")

	def add_power_generation_table(self, input):
		columns = input["table"]["columns"]
		sample_data = input["table"]["sampleData"]

		tree = ttk.Treeview(self.root, columns=columns, show="headings")

		for column in columns:
			tree.heading(column, text=column)
			tree.column(column, width=100)

		# TODO: ADD LOGIC TO FETCH FROM MYSQL
		for data in sample_data:
			tree.insert("", "end", values=data)

		tree.grid(row=self.row_buffer, column=0, columnspan=2)
		self.update_row_buffer(5)  # would be number of rows from mysql instead of 5

	def add_hyperlink_to_add_power_generation(self, input):
		hyperlink_label = Label(self.root, text=input['hyperlink'], fg="blue", cursor="hand2")
		hyperlink_label.grid(row=self.row_buffer, column=0, columnspan=2, pady=10)
		hyperlink_label.bind("<Button-1>", self.go_to_add_power_generation)

	#def go_to_add_power_generation(self, event):
		#print("TODO: I will go to listing power generation")


	def render(self, input):
		if self.root is None:
			self.initialize_widget()
		else:
			self.refresh_widget()

		# render rows
		self.add_form_title(input)
		self.add_form_title2(input)
		self.add_permanent_buttons(input)
		self.add_power_generation_table(input)
		self.add_hyperlink_to_add_power_generation(input)
		self.root.mainloop()