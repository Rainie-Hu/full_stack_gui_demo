from tkinter_widget import FullWidget
from tkinter import *
import utilityClass
import json

class OffTheGridDashboard(FullWidget):

    def __init__(self):
        self.frame = None
        self.title_label = None
        self.row_buffer = 0 
        self.DB = utilityClass.mySqlDB()
        FullWidget.__init__(self)

    def off_the_grid_dashboard(self, dict):
        """
        creating off-the-grid dashboard
        :param dict
        """
        self.initialize_widget()
        self.root.title("off-the-grid Dashboard")
        self.root.geometry("1000x600")

        #State with most of the grid
        self.frame = Frame(self.root)
        self.frame.place(x=10,y=10,width=300,height=300)
        res = self.DB.fetch('SELECT pc.state AS State,COUNT(*) AS Count FROM PostalCode pc INNER JOIN Household h ON pc.postalCode = h.postalCode INNER JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId WHERE hpu.publicUtilities = "off-the-grid" GROUP BY pc.state ORDER BY COUNT(*) DESC LIMIT 1;')
        if res == [] or res == [(None,)]: 
            res = [('test',0),]
        self.frame.digit_label = Label(self.frame, text=res[0][1], font=("Helvetica", 40))
        self.frame.digit_label.pack(side="top", pady=1)
        self.title_label = Label(self.frame, text="State with most of the grid:\n"+res[0][0], font=("Helvetica", 13))
        self.title_label.pack( pady=1)

        #Average battery storage capacity
        self.frame = Frame(self.root)
        self.frame.place(x=350,y=10,width=300,height=300)
        res = self.DB.fetch('SELECT ROUND(AVG(pg.storageCapacity)) AS batteryStorageAvgerage FROM Household h INNER JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId INNER JOIN powerGeneration pg ON h.emailId = pg.emailId WHERE hpu.publicUtilities = "off-the-grid";')
        if res == [] or res == [(None,)]: 
            res = [(0,0)]
        self.frame.digit_label = Label(self.frame, text=res[0][0], font=("Helvetica", 40))
        self.frame.digit_label.pack(side="top", pady=1)
        self.title_label = Label(self.frame, text="Average battery storage capacity", font=("Helvetica", 13))
        self.title_label.pack(pady=1)


        #Power generation type percentage
        res = self.DB.fetch('WITH powerGenExtract as (SELECT pg.*, hpu.publicUtilities FROM PowerGeneration pg JOIN Household h ON pg.emailId = h.emailId JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId WHERE hpu.publicUtilities = "off-the-grid") SELECT p.generatorType, ROUND((COUNT(*) / ( SELECT COUNT(*) FROM powerGenExtract)) * 100, 1) AS percentPowerGeneratorType FROM powerGenExtract p GROUP BY p.generatorType;')
        listed_res=[list(row) for row in res]
        f = open('input/off_the_grid_dict.json')
        data = json.load(f)
        data["Power generation type percentage table"]['table_param']['rows'] = listed_res
        self.frame = Frame(self.root)
        self.frame.place(x=750,y=10,width=300,height=300)
        self.title_label = Label(self.frame,anchor='w',  text="Power generation type\npercentage", font=("Helvetica", 12))
        self.title_label.pack(pady=1, fill=BOTH)
        if res == [] or res == [(None,)]: 
            self._add_table(dict["Power generation type percentage table"]).place(x=750,y=50,width=200,height=150)
        else:
            self._add_table(data["Power generation type percentage table"]).place(x=750,y=50,width=200,height=150)


        #Water heater gallon capacity on-grid vs off-grid
        res = self.DB.fetch('SELECT CASE WHEN hpu.publicUtilities!="off-the-grid" THEN "on-the-grid" ELSE "off-the-grid" END AS householdGrid, ROUND(AVG(wh.capacity),1) AS waterHeaterCapacityAverage FROM Household h INNER JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId INNER JOIN Appliances a ON h.emailId = h.emailId INNER JOIN WaterHeater wh ON a.emailId = wh.emailId AND a.systemInputOrder = wh.systemInputOrder GROUP BY 1;')
        listed_res=[list(row) for row in res]
        data["Water heater gallon capacity on-grid vs off-grid"]['table_param']['rows'] = listed_res
        self.frame = Frame(self.root)
        self.frame.place(x=200,y=300,width=300,height=300)
        self.title_label = Label(self.frame, anchor='w', text="Water heater gallon capacity\non-grid vs off-grid", font=("Helvetica", 12))
        self.title_label.pack(pady=1,fill=BOTH)
        print(res)
        if res == [] or res == [(None,)]: 
            self._add_table(dict["Water heater gallon capacity on-grid vs off-grid"]).place(x=200,y=350,width=200,height=150)
        else:
            self._add_table(data["Water heater gallon capacity on-grid vs off-grid"]).place(x=200,y=350,width=200,height=150)

        #Minimum avg and maximum BTU rating for off-grid
        res = self.DB.fetch("SELECT 'btuRatingAverage' AS statistics, ROUND(AVG(btuRating), 0) AS tmp FROM Household h JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId JOIN Appliances a ON h.emailId = a.emailId WHERE publicUtilities = 'off-the-grid' GROUP BY hpu.publicUtilities UNION SELECT 'btuRatingMinimum' AS statistics, ROUND(MIN(btuRating), 0) AS tmp FROM Household h JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId JOIN Appliances a ON h.emailId = a.emailId WHERE publicUtilities = 'off-the-grid' GROUP BY hpu.publicUtilities UNION SELECT 'btuRatingMaximum' AS statistics, ROUND(MAX(btuRating), 0) AS tmp FROM Household h JOIN HouseholdPublicUtilities hpu ON h.emailId = hpu.emailId JOIN Appliances a ON h.emailId = a.emailId WHERE publicUtilities = 'off-the-grid' GROUP BY hpu.publicUtilities;")
        listed_res=[list(row) for row in res]
        data["Minimum avg and maximum BTU rating for off-grid"]['table_param']['rows'] = listed_res
        self.frame = Frame(self.root)
        self.frame.place(x=600,y=300,width=300,height=300)
        self.title_label = Label(self.frame,anchor='w', text="Minimum avg and maximum\nBTU rating for off-grid", font=("Helvetica", 12))
        self.title_label.pack(pady=1,fill=BOTH)
        print(res)
        if res == [] or res == [(None,)]: 
            self._add_table(dict["Minimum avg and maximum BTU rating for off-grid"]).place(x=600,y=350,width=200,height=150)
        else:
            self._add_table(data["Minimum avg and maximum BTU rating for off-grid"]).place(x=600,y=350,width=200,height=150)
            
        self.root.mainloop()
