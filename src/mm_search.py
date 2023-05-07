from Phase_3.src.tkinter_widget import FullWidget
from Phase_3.src.mm_search_output import MMSearchOutputWidget
from ttwidgets import TTButton
from database import DB
import json


class MMSearchWidget(FullWidget):
    def no_result_message_widget(self):
        input = {"text": "There is no result!"}
        self._add_form_text(input)
        self.root.mainloop()

    def trigger_multi_command(self, input_dict):
        self.parse_values("mm_search_string")
        f = open('../Phase_3/output/mm_search_string.json')
        data = json.load(f)
        f.close()
        data_string = "%" + data["String Input"] + "%"
        db = DB()
        sql = f'''SELECT DISTINCT manufacturerName, model FROM Appliances WHERE manufacturerName LIKE "{data_string}" OR model LIKE "{data_string}" ORDER BY manufacturerName, model'''.format(data_string, data_string)
        result = db.fetch(sql)
        if len(result) == 0:
            self.no_result_message_widget()
        pass
        input_dict['MM Search table']['table_param']['rows'] = result
        mms = MMSearchOutputWidget()
        mms.mm_search_output_widget(input_dict)


    def _add_menu_buttons_output(self, menu_dict):


        if 'menu_buttons_config' in menu_dict:
            for _, button_kwargs in menu_dict["menu_buttons_config"].items():
                forward_button = TTButton(self.root, command=lambda f=menu_dict: self.trigger_multi_command(f), **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def mm_search_widget(self, input_dict):
        self.initialize_widget()
        self.root.title("Search")
        self._add_label_entries(input_dict)
        self._add_menu_buttons_output(input_dict)
        self.root.mainloop()


