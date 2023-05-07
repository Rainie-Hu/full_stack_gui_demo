from Phase_3.src.tkinter_widget import FullWidget
from tkinter import ttk
from tkinter import *
import utilityClass
import tkinter as tk

class WaterHeaterStat(FullWidget):

    def __init__(self):
        self.frame = None
        self.title_label = None
        self.DB = utilityClass.mySqlDB()
        FullWidget.__init__(self)

    def _add_table(self, dict):
        if 'table_param' in dict:
            table_dict = dict['table_param']
            my_tree = ttk.Treeview(self.root,  height=20)
            my_tree['columns'] = table_dict['columns']
            my_tree.column("#0",width=0,stretch=NO)
            for idx, _ in enumerate(table_dict['columns']):
                my_tree.column(table_dict['columns'][idx], width=table_dict['width'],minwidth=table_dict['minwidth'],anchor=table_dict['anchor'])
            for idx, _ in enumerate(table_dict['columns']):
                my_tree.heading(table_dict['columns'][idx], text=table_dict['columns'][idx],anchor=table_dict['anchor'])
            for idx, _ in enumerate(table_dict['rows']):
                my_tree.insert(parent='',index='end',iid=idx,values=tuple(table_dict['rows'][idx]))
            my_tree.pack(pady=0.1)

            scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=my_tree.yview)
            my_tree.configure(yscroll=scrollbar.set)
            return my_tree

    def water_heater_statistics(self, dict):
        """
        water heater statistic
        :param dict
        """
        self.initialize_widget()
        self.root.title("Water Heater Statistics")
        self.root.geometry("1000x500")
        result = self.DB.fetch(
            """
            SELECT
            pc.state AS State,
            ROUND(AVG(wh.capacity), 0) AS CapacityAvg,
            ROUND(AVG(a.btuRating), 0) AS BTURatingAvg,
            ROUND(AVG(wh.currentTemperature), 1) AS TemperatureSettingAvg,
            COUNT(
            CASE WHEN currentTemperature IS NOT NULL THEN wh.emailId
            ELSE NULL END
            ) AS TemperatureSettingInputCount,
            COUNT(
            CASE WHEN currentTemperature IS NULL THEN wh.emailId
            ELSE NULL END
            ) AS TemperatureSettingNoInputCount
            FROM
            PostalCode pc
            LEFT JOIN Household h ON pc.postalCode = h.postalCode
            JOIN Appliances a ON h.emailId = a.emailId
            JOIN WaterHeater wh ON a.emailId = wh.emailId AND a.systemInputOrder =
            wh.systemInputOrder
            GROUP BY
            pc.state
            ORDER BY
            pc.state ASC;"""
                      )
        listed_res = [list(row) for row in result]
        dict['Water Heater Stat']["table_param"]["rows"] = listed_res
        # self.title_label = Label(self.frame, text="Water Heater Statistics", font=("Helvetica", 15))
        # self.title_label.pack(pady=20)
        self._add_table(dict["Water Heater Stat"]).place()
        self.root.mainloop()

    def water_heater_statistics_trigger(self, dict):
        """
        water heater statistic
        :param dict
        """
        self.initialize_widget()
        self.root.title("Water Heater Statistics")
        self.root.geometry("1000x500")
        result = self.DB.fetch(
            """
            SELECT
            pc.state AS State,
            ROUND(AVG(wh.capacity), 0) AS CapacityAvg,
            ROUND(AVG(a.btuRating), 0) AS BTURatingAvg,
            ROUND(AVG(wh.currentTemperature), 1) AS TemperatureSettingAvg,
            COUNT(
            CASE WHEN currentTemperature IS NOT NULL THEN wh.emailId
            ELSE NULL END
            ) AS TemperatureSettingInputCount,
            COUNT(
            CASE WHEN currentTemperature IS NULL THEN wh.emailId
            ELSE NULL END
            ) AS TemperatureSettingNoInputCount
            FROM
            PostalCode pc
            LEFT JOIN Household h ON pc.postalCode = h.postalCode
            JOIN Appliances a ON h.emailId = a.emailId
            JOIN WaterHeater wh ON a.emailId = wh.emailId AND a.systemInputOrder =
            wh.systemInputOrder
            GROUP BY
            pc.state
            ORDER BY
            pc.state ASC;"""
                      )
        listed_res = [list(row) for row in result]
        dict['Water Heater Stat']["table_param"]["rows"] = listed_res
        # self.title_label = Label(self.frame, text="Water Heater Statistics", font=("Helvetica", 15))
        # self.title_label.pack(pady=20)
        self._add_table(dict["Water Heater Stat"]).place()