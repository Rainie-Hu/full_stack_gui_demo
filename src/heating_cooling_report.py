from Phase_3.src.tkinter_widget import FullWidget
from tkinter import *
import utilityClass
from tkinter import ttk
import tkinter as tk

class HeatingCoolingMethodReport(FullWidget):

    def __init__(self):
        self.frame = None
        self.title_label = None
        self.DB = utilityClass.mySqlDB()

        FullWidget.__init__(self)

    def _add_table(self, dict):
        if 'table_param' in dict:
            table_dict = dict['table_param']
            my_tree = ttk.Treeview(self.root,  height=5)
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

    def heating_cooling_dashboard(self, dict):
        """
        creating heating cooling dashboard
        :param dict
        """
        self.initialize_widget()
        self.root.title("Heating Cooling Dashboard")
        self.root.geometry("1400x250")
        result = self.DB.fetch(
            """
                WITH airConditioner AS (
                    SELECT
                    h.householdType AS HouseholdType,
                    COUNT(*) AS AirConditionerCount,
                    ROUND(AVG(a.btuRating), 0) AS AirconditionerAvgBTU,
                    ROUND(AVG(ac.energyEfficiencyRatio), 1) AS AirconditionerEERAvg
                    FROM
                    Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN AirConditioner ac
                    ON a.emailId = ac.emailId AND a.systemInputOrder = ac.systemInputOrder
                    GROUP BY h.householdType),
                    heaterCountByHousehold AS (
                    SELECT
                    h.householdType AS HouseholdType,
                    COUNT(*) AS HeaterCount,
                    ROUND(AVG(a.btuRating), 0) AS HeaterAvgBTU
                    FROM
                    Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN Heater ha
                    ON a.emailId = ha.emailId AND a.systemInputOrder = ha.systemInputOrder
                    GROUP BY h.householdType),
                    heaterES AS (
                    SELECT
                    hes.householdType AS HouseholdType,
                    hes.energySource AS HeaterCommonEnergySource
                    FROM
                    (SELECT
                    h.householdType,
                    ha.energySource,
                    ROW_NUMBER() OVER (
                    PARTITION BY h.householdType
                    ORDER BY COUNT(ha.energySource) DESC) AS
                    rn
                    FROM Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN Heater ha ON
                    a.emailId = ha.emailId AND a.systemInputOrder = ha.systemInputOrder
                    GROUP BY h.householdType, ha.energySource) AS hes
                    WHERE hes.rn = 1),
                    heatPump AS (
                    SELECT
                    h.householdType AS HouseholdType,
                    COUNT(*) AS HeatpumpCount,
                    ROUND(AVG(a.btuRating), 0) AS HeatpumpAvgBTU,
                    ROUND(AVG(hp.seer), 1) AS HeatpumpSEERAvg,
                    ROUND(AVG(hp.hspf), 1) AS HeatpumpHSPFAvg
                    FROM
                    Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN HeatPump hp
                    ON a.emailId = hp.emailId AND a.systemInputOrder = hp.systemInputOrder
                    GROUP BY h.householdType)
                    SELECT
                    ac.HouseholdType,
                    ac.AirConditionerCount,
                    ac.AirconditionerAvgBTU,
                    ac.AirconditionerEERAvg,
                    ht.HeaterCount,
                    ht.HeaterAvgBTU,
                    hes.HeaterCommonEnergySource,
                    hp.HeatpumpCount,
                    hp.HeatpumpAvgBTU,
                    hp.HeatpumpSEERAvg,
                    hp.HeatpumpHSPFAvg
                    FROM airConditioner ac
                    LEFT JOIN heaterCountByHousehold AS ht ON ac.HouseholdType =
                    ht.HouseholdType
                    LEFT JOIN heaterES AS hes ON ac.HouseholdType = hes.HouseholdType
                    LEFT JOIN heatPump AS hp ON ac.HouseholdType = hp.HouseholdType;
            """
        )
        listed_res = [list(row) for row in result]
        dict['Heating Cooling Method Details']["table_param"]["rows"] = listed_res


        # #Power generation type percentage
        # self.title_label = Label(self.frame, text="Heating Cooling Method Details", font=("Helvetica", 15))
        # self.title_label.pack(pady=20)
        self._add_table(dict["Heating Cooling Method Details"]).place()

        self.root.mainloop()

    def heating_cooling_dashboard_trigger(self, dict):
        """
        creating heating cooling dashboard
        :param dict
        """
        self.initialize_widget()
        self.root.title("Heating Cooling Dashboard")
        self.root.geometry("1400x250")
        result = self.DB.fetch(
            """
                WITH airConditioner AS (
                    SELECT
                    h.householdType AS HouseholdType,
                    COUNT(*) AS AirConditionerCount,
                    ROUND(AVG(a.btuRating), 0) AS AirconditionerAvgBTU,
                    ROUND(AVG(ac.energyEfficiencyRatio), 1) AS AirconditionerEERAvg
                    FROM
                    Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN AirConditioner ac
                    ON a.emailId = ac.emailId AND a.systemInputOrder = ac.systemInputOrder
                    GROUP BY h.householdType),
                    heaterCountByHousehold AS (
                    SELECT
                    h.householdType AS HouseholdType,
                    COUNT(*) AS HeaterCount,
                    ROUND(AVG(a.btuRating), 0) AS HeaterAvgBTU
                    FROM
                    Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN Heater ha
                    ON a.emailId = ha.emailId AND a.systemInputOrder = ha.systemInputOrder
                    GROUP BY h.householdType),
                    heaterES AS (
                    SELECT
                    hes.householdType AS HouseholdType,
                    hes.energySource AS HeaterCommonEnergySource
                    FROM
                    (SELECT
                    h.householdType,
                    ha.energySource,
                    ROW_NUMBER() OVER (
                    PARTITION BY h.householdType
                    ORDER BY COUNT(ha.energySource) DESC) AS
                    rn
                    FROM Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN Heater ha ON
                    a.emailId = ha.emailId AND a.systemInputOrder = ha.systemInputOrder
                    GROUP BY h.householdType, ha.energySource) AS hes
                    WHERE hes.rn = 1),
                    heatPump AS (
                    SELECT
                    h.householdType AS HouseholdType,
                    COUNT(*) AS HeatpumpCount,
                    ROUND(AVG(a.btuRating), 0) AS HeatpumpAvgBTU,
                    ROUND(AVG(hp.seer), 1) AS HeatpumpSEERAvg,
                    ROUND(AVG(hp.hspf), 1) AS HeatpumpHSPFAvg
                    FROM
                    Household h
                    LEFT JOIN Appliances a ON h.emailId = a.emailId
                    LEFT JOIN HeatPump hp
                    ON a.emailId = hp.emailId AND a.systemInputOrder = hp.systemInputOrder
                    GROUP BY h.householdType)
                    SELECT
                    ac.HouseholdType,
                    ac.AirConditionerCount,
                    ac.AirconditionerAvgBTU,
                    ac.AirconditionerEERAvg,
                    ht.HeaterCount,
                    ht.HeaterAvgBTU,
                    hes.HeaterCommonEnergySource,
                    hp.HeatpumpCount,
                    hp.HeatpumpAvgBTU,
                    hp.HeatpumpSEERAvg,
                    hp.HeatpumpHSPFAvg
                    FROM airConditioner ac
                    LEFT JOIN heaterCountByHousehold AS ht ON ac.HouseholdType =
                    ht.HouseholdType
                    LEFT JOIN heaterES AS hes ON ac.HouseholdType = hes.HouseholdType
                    LEFT JOIN heatPump AS hp ON ac.HouseholdType = hp.HouseholdType;
            """
        )
        listed_res = [list(row) for row in result]
        dict['Heating Cooling Method Details']["table_param"]["rows"] = listed_res


        #Power generation type percentage
        # self.title_label = Label(self.frame, text="Heating Cooling Method Details", font=("Helvetica", 15))
        # self.title_label.pack(pady=20)
        self._add_table(dict["Heating Cooling Method Details"]).place()