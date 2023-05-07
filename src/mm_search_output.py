from Phase_3.src.tkinter_widget import FullWidget


class MMSearchOutputWidget(FullWidget):

    def mm_search_output_widget(self, input):
        self.initialize_widget()
        self.root.title("Search")
        self._add_table(input["MM Search table"])