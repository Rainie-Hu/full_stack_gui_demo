from Phase_3.src.tkinter_widget import FullWidget
from ttwidgets import TTButton
from Phase_3.src.main_screen import MainScreen
import json


class WrappingUpWidget(FullWidget):
    def _add_menu_buttons_next(self, menu_dict):
        dd = MainScreen()
        if 'perm_button_params' in menu_dict:
            for _, button_kwargs in menu_dict["perm_button_params"].items():
                f = open('../Phase_3/input/main_screen.json')
                main_input = json.load(f)
                f.close()
                forward_button = TTButton(self.root, command=lambda f=main_input: dd.show_main_screen(f),
                                          **button_kwargs['button'])
                forward_button.grid(**button_kwargs['grid'])

    def wrapping_up_widget(self, input):

        self._add_form_title(input)
        self._add_form_text(input)
        self._add_menu_buttons_next(input)
        self.root.mainloop()
