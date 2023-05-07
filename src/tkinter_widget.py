from tkinter import *
from ttwidgets import TTButton
from tkinter import ttk
import tkinter as tk
import json

class FullWidget:

    def __init__(self):
        self.root = None
        self.label_entries_list = []
        self.checkbox_entries_list = []
        self.custom_entries_list = []
        self.row_buffer = 0 #to assign rows

    def refresh_widget(self):
        """

        :return:
        """
        self.root.destroy()
        self.root = Tk()

    def initialize_widget(self):
        self.root = Tk()

    def update_row_buffer(self, buffer):
        self.row_buffer += buffer
        return self.row_buffer

    def _add_label_entries(self, menu_dict):
        """

        :param menu_dict:
        :return:
        """

        def on_click(event):
            event.widget.delete(0, tk.END)

        if len(menu_dict['menu_labels']) > 0:
            self.label_entries_list = [
                (Label(self.root, text=label),
                 Entry(self.root, textvariable=StringVar(self.root, value=default_text)))
                for label, default_text in menu_dict['menu_labels'].items()]

            for r, label_entry in enumerate(self.label_entries_list):
                label_entry[1].bind("<Button-1>", on_click)
                label_entry[0].grid(row=r + self.row_buffer, sticky=W)
                label_entry[1].grid(row=r + self.row_buffer, column=1, ipadx=50)
            self.update_row_buffer(len(self.label_entries_list))

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

    def _add_form_title(self, input):
        label = Label(self.root, text=input["title"], font=("Helvetica", 16, "bold"), anchor="w")
        label.grid(row=self.row_buffer, column=0, columnspan=2)
        self.update_row_buffer(1)

    def _add_form_text(self, input):
        label = Label(self.root, text=input["text"], font=("Helvetica", 12), anchor="w")
        label.grid(row=self.row_buffer, column=0)
        self.update_row_buffer(1)

    def _add_checkboxes(self, menu_dict):
        """

        :return:
        """
        if len(menu_dict["menu_checkboxes"]) > 0:
            def onPress(label):
                menu_dict["menu_checkboxes"][label] = not menu_dict['menu_checkboxes'][label]
            self.check_var_list = [IntVar() for i in range(len(menu_dict['menu_checkboxes'].keys()))]
            self.checkbox_entries_list = [
                [
                (label[0], check_var),
                Label(self.root, text=label[0]),
                Checkbutton(self.root, onvalue=1, offvalue=0,
                            variable=check_var
                            # ,command=lambda label=label[0]: onPress(label)
                            )
                # Checkbutton(self.root, onvalue=1, offvalue=0, command=lambda label=label: onPress(label, 1)),
                # Entry(self.root, textvariable=StringVar(self.root, value=(menu_dict['xpaths'][label] if label in menu_dict['xpaths'].keys() else "")))
                ]
                for label, check_var in zip(menu_dict['menu_checkboxes'].items(), self.check_var_list)
            ]

            for r, checkbox in enumerate(self.checkbox_entries_list):
                checkbox[1].grid(row=r + self.row_buffer, sticky=W, )
                checkbox[2].grid(row=r + self.row_buffer, column=1, ipadx=50)

        self.update_row_buffer(len(self.checkbox_entries_list))

    def _add_permanent_buttons(self, menu_dict):

        if 'perm_button_params' in menu_dict:
            for _, button_kwargs in menu_dict["perm_button_params"].items():
                forward_button = TTButton(self.root, command=lambda f=menu_dict['title']: self.parse_values(f), **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def _add_menu_buttons(self, menu_dict):
        if 'menu_buttons_config' in menu_dict:
            for _, button_kwargs in menu_dict["menu_buttons_config"].items():
                forward_button = TTButton(self.root, command=lambda f=menu_dict['title']: self.parse_values(f), **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def parse_values(self, title):
        # read from self.label_entries_list
        title = title.lower().replace(" ", "_").replace(":", "").replace("!", "")
        D = {}
        if self.label_entries_list is not None:
            l_e_len = len(self.label_entries_list)
            for l in range(l_e_len):
                label_tx = self.label_entries_list[l][0].cget("text")
                entry_tx = self.label_entries_list[l][1].get()
                D[label_tx] = entry_tx
        # read from self.checkbox_entries_list
        if self.checkbox_entries_list is not None:
            c_e_len = len(self.checkbox_entries_list)
            for l2 in range(c_e_len):
                ce_label_tx = self.checkbox_entries_list[l2][0][0]
                ce_checkbutton_tx = self.checkbox_entries_list[l2][0][1].get()
                D[ce_label_tx] = ce_checkbutton_tx
        # print(D)
        with open(f'../Phase_3/output/{title}.json', 'w') as fp:
            json.dump(D, fp)


    def _add_table(self, dict):
        if 'table_param' in dict:
            table_dict = dict['table_param']
            my_tree = ttk.Treeview(self.root)
            my_tree['columns'] = table_dict['columns']
            my_tree.column("#0",width=0,stretch=NO)
            for idx, _ in enumerate(table_dict['columns']):
                my_tree.column(table_dict['columns'][idx], width=table_dict['width'],minwidth=table_dict['minwidth'],anchor=table_dict['anchor'])
            for idx, _ in enumerate(table_dict['columns']):
                my_tree.heading(table_dict['columns'][idx], text=table_dict['columns'][idx],anchor=table_dict['anchor'])
            for idx, _ in enumerate(table_dict['rows']):
                my_tree.insert(parent='',index='end',iid=idx,values=tuple(table_dict['rows'][idx]))
            my_tree.pack(expand=True)

            scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=my_tree.yview)
            my_tree.configure(yscroll=scrollbar.set)
            return my_tree


    def menu_widget(self, menu_dict):
        """

        :param menu_dict:
        :return:
        """

        self.root.title(menu_dict['title'])

        # add entries with labels
        self._add_label_entries(menu_dict)

        # add checkboxes with labels
        self._add_checkboxes(menu_dict)

        # add permanent buttons
        self._add_permanent_buttons(menu_dict)

        # add custom buttons
        self._add_menu_buttons(menu_dict)

        self.root.mainloop()