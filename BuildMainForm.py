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

        DatabaseInteractions.initial_db_setup()

        self.root.wm_title(self.title)
        
        notebook = ttk.Notebook(self.root)
        page_1_summary = Frame(notebook)
        page_2_bills = Frame(notebook)
        notebook.add(page_1_summary, text="Summary")
        notebook.add(page_2_bills, text="Bills")
        self.summary_tab_builder(page_1_summary)
        self.bills_tab_builder(page_2_bills)
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

    def bills_tab_builder(self, note_page):

        # Define Widgets
        bills_to_pay_frame = LabelFrame(note_page, text="To Pay:")
        bills_to_pay_listbox = Listbox(bills_to_pay_frame)
        bills_paid_frame = LabelFrame(note_page, text="Paid:")
        bills_paid_listbox = Listbox(bills_paid_frame)
        bill_info_frame = LabelFrame(note_page, text="Bill Info:")
        bill_name_entry = Entry(bill_info_frame)
        bill_amount_entry = Entry(bill_info_frame)
        bill_paid_checkbutton = Checkbutton(bill_info_frame, text="Paid")
        bill_summary_frame = LabelFrame(note_page, text="Summary:")
        bill_total_paid_entry = Entry(bill_summary_frame)
        bill_remains_to_pay_entry = Entry(bill_summary_frame)

        # Pack Widgets
        bills_to_pay_frame.grid(row=0, column=0)
        bills_to_pay_listbox.pack()
        bills_paid_frame.grid(row=0, column=1)
        bills_paid_listbox.pack()
        bill_info_frame.grid(row=1, column=0, columnspan=2, sticky=W+E)
        bill_name_entry.pack()
        bill_amount_entry.pack()
        bill_paid_checkbutton.pack()
        bill_summary_frame.grid(row=2, column=0, columnspan=2, sticky=W+E)
        bill_total_paid_entry.pack()
        bill_remains_to_pay_entry.pack()

    def add_new_bill_form_builder(self):

        sub_root = Toplevel()
        sub_root.geometry("+" + str(self.root.winfo_x() + 50) + "+" + str(self.root.winfo_y() + 50))
        sub_root.resizable(height=False, width=False)

        recurring_var = BooleanVar()

        # Define Widgets
        bill_name_frame = LabelFrame(sub_root, text="Name:")
        bill_name_entry = Entry(bill_name_frame)
        bill_amount_frame = LabelFrame(sub_root, text="Amount:")
        bill_amount_entry = Entry(bill_amount_frame)
        bill_recurring_checkbutton = Checkbutton(bill_amount_frame, text="Recurring", variable=recurring_var,
                                                 onvalue=True, offvalue=False)
        bill_notes_frame = LabelFrame(sub_root, text="Notes")
        bill_notes_text = Text(bill_notes_frame)
        add_bill_button = Button(sub_root, text="Add Bill",
                                 command=lambda: (DatabaseInteractions.add_new_bill(bill_name_entry.get(),
                                                                                    float(bill_amount_entry.get()),
                                                                                    bill_notes_text.get("1.0", "end-1c"),
                                                                                    recurring_var.get()
                                                                                    ),
                                                  sub_root.destroy()
                                                  )

                                 )

        # Pack Widgets
        bill_name_frame.pack()
        bill_name_entry.pack()
        bill_amount_frame.pack()
        bill_amount_entry.pack()
        bill_recurring_checkbutton.pack()
        bill_recurring_checkbutton.select()  # Ensures checkbox is already selected by default
        bill_notes_frame.pack()
        bill_notes_text.pack()
        add_bill_button.pack()


