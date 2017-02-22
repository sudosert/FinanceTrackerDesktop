import tkinter
import DatabaseInteractions
from tkinter import *


class BlankForm:

    def __init__(self, title, width, height):

        self.title = title
        self.width = width
        self.height = height


class MainForm(BlankForm):

    def build_form(self):

        root = tkinter.Tk()

        root.wm_title(self.title)