import DatabaseInteractions
import tkinter
from tkinter import ttk
from tkinter import *


class BlankForm:

    def __init__(self, title):

        self.title = title
        self.root = tkinter.Tk()
        self.root.resizable(height=False, width=False)


class MainForm(BlankForm):

    def build_form(self):

        self.root.wm_title(self.title)
        
        notebook = ttk.Notebook(self.root)
        page_1_summary = Frame(notebook)
        notebook.add(page_1_summary, text="Summary")
        self.summary_tab_builder(page_1_summary)
        notebook.pack()

        self.root.mainloop()

    def summary_tab_builder(self, note_page):

        # Define Widgets
        left_to_spend_frame = LabelFrame(note_page, text="Spending Money Remaining:")
        total_left_to_spend_entry = Entry(left_to_spend_frame)
        days_until_paid_entry = Entry(left_to_spend_frame)
        avg_left_to_spend = Entry(left_to_spend_frame)
        add_new_bill_button = Button(note_page, text="Add New Bill", command=self.add_new_bill_form_builder)

        # Pack Widgets
        left_to_spend_frame.pack()
        total_left_to_spend_entry.pack()
        days_until_paid_entry.pack()
        avg_left_to_spend.pack()
        add_new_bill_button.pack()

    def add_new_bill_form_builder(self):

        sub_root = Toplevel()
        sub_root.geometry("+" + str(self.root.winfo_x() + 50) + "+" + str(self.root.winfo_y() + 50))
        sub_root.resizable(height=False, width=False)

        # Define Widgets
        bill_name_frame = LabelFrame(sub_root, text="Name:")
        bill_name_entry = Entry(bill_name_frame)
        bill_amount_frame = LabelFrame(sub_root, text="Amount:")
        bill_amount_entry = Entry(bill_amount_frame)
        bill_notes_frame = LabelFrame(sub_root, text="Notes")
        bill_notes_text = Text(bill_notes_frame)
        add_bill_button = Button(sub_root, text="Add Bill",
                                 command=lambda: (DatabaseInteractions.add_new_bill(bill_name_entry.get(),
                                                                                    float(bill_amount_entry.get()),
                                                                                    bill_notes_text.get("1.0", "end-1c")
                                                                                    ),
                                                  sub_root.destroy()
                                                  )

                                 )

        # Pack Widgets
        bill_name_frame.pack()
        bill_name_entry.pack()
        bill_amount_frame.pack()
        bill_amount_entry.pack()
        bill_notes_frame.pack()
        bill_notes_text.pack()
        add_bill_button.pack()

