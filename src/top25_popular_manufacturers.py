from Phase_3.src.tkinter_widget import FullWidget
from Phase_3.src.top25_drilldown import Top25DrilldownWidget
from database import DB
from ttwidgets import TTButton
import json

class Top25ManufacturersWidget(FullWidget):
    def _add_menu_buttons_pack(self, input):
        dd = Top25DrilldownWidget()
        if 'menu_buttons_config' in input:
            for _, button_kwargs in input["menu_buttons_config"].items():
                button1 = TTButton(self.root, command=lambda f=input: dd.top25_drilldown_widget(f), **button_kwargs['button'])
                button1.pack(**button_kwargs['pack'])

    # def handle_selection(event):
    #
    #     selected_item = my_treeview.selection()[0]
    #     print(selected_item)


    def top25_manufacturer_widget(self, input):
        self.initialize_widget()
        self.root.title("Top 25 Popular Manufacturer")
        db = DB()
        sql = """
        WITH app_label AS 
(SELECT 
a.*, 
CASE WHEN (ac.emailId IS NOT NULL) AND (ac.systemInputOrder IS NOT NULL) THEN 1 ELSE 0 END AS is_ac,
CASE WHEN (h.emailId IS NOT NULL) AND (h.systemInputOrder IS NOT NULL) THEN 1 ELSE 0 END AS is_h,
CASE WHEN (hp.emailId IS NOT NULL) AND (hp.systemInputOrder IS NOT NULL) THEN 1 ELSE 0 END AS is_hp,
CASE WHEN (wh.emailId IS NOT NULL) AND (wh.systemInputOrder IS NOT NULL) THEN 1 ELSE 0 END AS is_wh
FROM Appliances a LEFT JOIN airconditioner ac ON a.emailId = ac.emailId AND a.systemInputOrder = ac.systemInputOrder LEFT JOIN heater h ON a.emailId = h.emailId AND a.systemInputOrder = h.systemInputOrder LEFT JOIN heatpump hp ON a.emailId = hp.emailId AND a.systemInputOrder = hp.systemInputOrder LEFT JOIN waterheater wh ON a.emailId = wh.emailId AND a.systemInputOrder = wh.systemInputOrder)
SELECT 
manufacturerName, (SUM(is_ac) + SUM(is_h) + SUM(is_hp) + SUM(is_wh)) AS ApplianceCount
FROM app_label
GROUP BY manufacturerName ORDER BY ApplianceCount DESC LIMIT 25;"""
        result = db.fetch(sql)
        input["Top 25 popular manufacturer table"]["table_param"]["rows"] = result
        self.root.geometry("400x400")
        finaltree = self._add_table(input["Top 25 popular manufacturer table"])

        def item_clicked(event):
            # Get the selected row data
            selected_item = event.widget.selection()[0]
            manufacturer_selected = event.widget.item(selected_item, 'values')[0]
            db = DB()
            sql1 = f'''SELECT COUNT(DISTINCT a.emailId, a.systemInputOrder)
FROM appliances a 
RIGHT JOIN airconditioner ai ON a.systemInputOrder = ai.systemInputOrder AND a.emailId = ai.emailId
WHERE a.manufacturerName = "{manufacturer_selected}"'''.format(manufacturer_selected)

            sql2 = f'''SELECT COUNT(DISTINCT a.emailId, a.systemInputOrder)
FROM appliances a 
RIGHT JOIN heater h ON a.systemInputOrder = h.systemInputOrder AND a.emailId = h.emailId
WHERE a.manufacturerName = "{manufacturer_selected}"'''.format(manufacturer_selected)

            sql3 = f'''SELECT COUNT(DISTINCT a.emailId, a.systemInputOrder)
FROM appliances a 
RIGHT JOIN heatpump hp ON a.systemInputOrder = hp.systemInputOrder AND a.emailId = hp.emailId
WHERE a.manufacturerName = "{manufacturer_selected}"'''.format(manufacturer_selected)

            sql4 = f'''SELECT COUNT(DISTINCT a.emailId, a.systemInputOrder)
            FROM appliances a 
            RIGHT JOIN waterheater wh ON a.systemInputOrder = wh.systemInputOrder AND a.emailId = wh.emailId
            WHERE a.manufacturerName = "{manufacturer_selected}"'''.format(manufacturer_selected)

            result1 = db.fetch(sql1)
            result2 = db.fetch(sql2)
            result3 = db.fetch(sql3)
            result4 = db.fetch(sql4)
            f = open('../Phase_3/input/top25_dict.json')
            input = json.load(f)
            f.close()
            input["drilldown table"]["table_param"]["rows"] = [["airconditioner", result1],["heater", result2],["heatpump", result3],["waterheater", result4]]
            dd = Top25DrilldownWidget()
            dd.top25_drilldown_widget(input)

        finaltree.bind("<Double-1>", item_clicked)
        self.root.mainloop()

