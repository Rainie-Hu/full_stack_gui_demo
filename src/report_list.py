from Phase_3.src.tkinter_widget import FullWidget
from Phase_3.src.water_heater_stat import WaterHeaterStat
from Phase_3.src.heating_cooling_report import HeatingCoolingMethodReport
from Phase_3.src.household_average_by_radius import householdAverageByRadius
from Phase_3.src.off_the_grid import OffTheGridDashboard
from Phase_3.src.mm_search import MMSearchOutputWidget
from Phase_3.src.top25_popular_manufacturers import Top25ManufacturersWidget
from tkinter import *
from ttwidgets import TTButton
import json

class ReportList(FullWidget):

    def __init__(self):
        self.title_label = None
        self.frame = None
        self.water_heater_stat = WaterHeaterStat()
        self.heating_cooling_method_report = HeatingCoolingMethodReport()
        self.top25_popular_manufacturers = Top25ManufacturersWidget()
        self.mm_search = MMSearchOutputWidget()
        self.off_the_grid = OffTheGridDashboard()
        self.household_averages_by_radius = householdAverageByRadius()


        self._widget_data = {
            "top25_popular_manufacturers":
                {
                    "input_json": "../Phase_3/input/top25_dict.json",
                },
            "mm_search":
                {
                    "input_json": "../Phase_3/input/mm_search_dict.json",
                },
            "off_the_grid":
                {
                    "input_json": "../Phase_3/input/off_the_grid_dict.json",
                },
            "household_averages_by_radius":
                {
                    "input_json": "../Phase_3/input/household_average_by_radius.json",
                },
            "water_heater_stats":
                {
                    "input_json": "../Phase_3/input/water_heater_stat.json",
                 },
            "heating_cooling_method_details":
                {
                    "input_json": "../Phase_3/input/heating_cooling_dash.json",
                }
        }
        FullWidget.__init__(self)

    def _trigger(self, title):
        if title == "water_heater_stats":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.water_heater_stat.water_heater_statistics_trigger(trigger_data)
        elif title == "heating_cooling_method_details":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.heating_cooling_method_report.heating_cooling_dashboard_trigger(trigger_data)
        elif title == "household_averages_by_radius":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.household_averages_by_radius.render(trigger_data)
        elif title == "off_the_grid":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.off_the_grid.off_the_grid_dashboard(trigger_data)
        elif title == "mm_search":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.mm_search.mm_search_output_widget(trigger_data)
        elif title == "top25_popular_manufacturers":
            trigger_data = self._read_json(self._widget_data[title]["input_json"])
            self.top25_popular_manufacturers.top25_manufacturer_widget(trigger_data)

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

    def _add_menu_buttons_wframe(self, menu_dict):
        if 'menu_buttons_config' in menu_dict:
            for button_name, button_kwargs in menu_dict["menu_buttons_config"].items():
                forward_button = TTButton(self.frame,
                                          command=lambda f=button_name: self._trigger(f),
                                          **button_kwargs['button'])
                forward_button.pack(**button_kwargs['pack'])

    def report_list(self, dict):
        """

        :param dict
        """
        self.initialize_widget()
        self.root.geometry("250x250")
        self.root.title(dict['title'])

        # add custom buttons
        self._add_menu_buttons(dict)
        self.root.mainloop()

    def report_list_trigger(self, dict):
        """

        :param dict
        """
        self.initialize_widget()
        # self.frame = Frame(self.root)
        self.root.geometry("250x250")
        self.root.title(dict['title'])

        # add custom buttons
        self._add_menu_buttons(dict)