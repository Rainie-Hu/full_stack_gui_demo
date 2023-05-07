from Phase_3.src.tkinter_widget import FullWidget
from Phase_3.src.report_list import ReportList
from Phase_3.src.household_form import HouseHoldWidget
from tkinter import *
from ttwidgets import TTButton
import json

class MainScreen(FullWidget):

    def __init__(self):
        self.frame = None
        self.title_label = None
        FullWidget.__init__(self)
        self.report_list = ReportList()
        self.household_form = HouseHoldWidget()
        self._widget_data = {
            "enter_household_info":
                {
                    "input_json": "../Phase_3/input/household_form_input.json",
                 },
            "display_reports":
                {
                    "input_json": "../Phase_3/input/report_list.json",
                }
        }
        FullWidget.__init__(self)

    def _trigger(self, title):
        if title == "enter_household_info":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.household_form.render(trigger_data)
        elif title == "display_reports":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.report_list.report_list_trigger(trigger_data)

    def _read_json(self, json_path):
        """

        :param json_path:
        :return:
        """
        f = open(json_path)
        data = json.load(f)
        f.close()
        return data

    def _add_menu_buttons(self, menu_dict):
        if 'menu_buttons_config' in menu_dict:
            for button_name, button_kwargs in menu_dict["menu_buttons_config"].items():
                forward_button = TTButton(self.root,
                                          command=lambda f=button_name: self._trigger(f),
                                          **button_kwargs['button'])
                forward_button.pack(**button_kwargs['pack'])

    def show_main_screen(self, dict):
        self.initialize_widget()
        self.root.geometry("200x250")
        self.menu_widget(dict)