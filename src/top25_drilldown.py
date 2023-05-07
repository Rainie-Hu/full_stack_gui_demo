from tkinter import *
from tkinter import ttk
from ttwidgets import TTButton
from Phase_3.src.tkinter_widget import FullWidget

class Top25DrilldownWidget(FullWidget):
    def top25_drilldown_widget(self,input):
        self.initialize_widget()
        self.root.title(input['drilldown_title'])
        self._add_table(input["drilldown table"])
