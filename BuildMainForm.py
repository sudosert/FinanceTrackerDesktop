import DatabaseInteractions
import tkinter
from tkinter import ttk
from tkinter import *

selected_currency = "£"  # This will be a user selected variable that will change the currency label


class BlankForm:

    def __init__(self, title):

        self.title = title
        self.root = tkinter.Tk()
        self.root.resizable(height=False, width=False)


class MainForm(BlankForm):
    
    def __init__(self, title):

        # Global variables
        global selected_currency

        # Call to init of superclass to inherit values
        BlankForm.__init__(self, title)

        # Core Objects
        self.notebook = ttk.Notebook(self.root)
        self.page_1_summary = Frame(self.notebook)
        self.page_2_bills = Frame(self.notebook)

        # Widgets Variables
        self.bill_name_var = StringVar()
        self.bill_amount_var = StringVar()
        self.bill_paid_var = IntVar()
        
        # Summary Tab Widgets
        self.left_to_spend_frame = LabelFrame(self.page_1_summary, text="Spending Money Remaining:")
        self.total_left_to_spend_entry = Entry(self.left_to_spend_frame)
        self.days_until_paid_entry = Entry(self.left_to_spend_frame)
        self.avg_left_to_spend = Entry(self.left_to_spend_frame)
        self.add_new_bill_button = Button(self.page_1_summary, text="Add New Bill", 
                                          command=self.add_new_bill_form)
        
        # Bills Tab Widgets
        self.bills_to_pay_frame = LabelFrame(self.page_2_bills, text="To Pay:")
        self.bills_to_pay_listbox = Listbox(self.bills_to_pay_frame)
        self.bills_to_pay_listbox.bind("<<ListboxSelect>>",
                                       lambda x: self.on_list_select_binding(self.bills_to_pay_listbox))
        self.bills_paid_frame = LabelFrame(self.page_2_bills, text="Paid:")
        self.bills_paid_listbox = Listbox(self.bills_paid_frame)
        self.bills_paid_listbox.bind("<<ListboxSelect>>",
                                     lambda x: self.on_list_select_binding(self.bills_paid_listbox))
        self.bill_info_frame = LabelFrame(self.page_2_bills, text="Bill Info:")
        self.bill_name_entry = Entry(self.bill_info_frame, textvar=self.bill_name_var,
                                     state="readonly")  # Bill name is primary key in DB so should not be edited
        self.bill_amount_entry = Entry(self.bill_info_frame, textvar=self.bill_amount_var)
        self.save_changes_button = Button(self.bill_info_frame, text="Submit", command=self.save_changes_on_click)
        self.bill_paid_checkbutton = Checkbutton(self.bill_info_frame, text="Paid", var=self.bill_paid_var)
        self.bill_summary_frame = LabelFrame(self.page_2_bills, text="Summary:")
        self.bill_total_paid_entry = Entry(self.bill_summary_frame)
        self.bill_remains_to_pay_entry = Entry(self.bill_summary_frame)

    def build_form(self):

        #  Run Database Operations
        DatabaseInteractions.initial_db_setup()

        #  Set Window Attributes
        self.root.wm_title(self.title)
        
        #  Set Tab Attributes and Pack Tabs
        self.notebook.add(self.page_1_summary, text="Summary")
        self.notebook.add(self.page_2_bills, text="Bills")
        self.summary_tab_builder()
        self.bills_tab_builder()
        self.notebook.pack()

        #  Run Main Loop
        self.root.mainloop()

    def summary_tab_builder(self):

        # Pack Widgets
        self.left_to_spend_frame.pack()
        self.total_left_to_spend_entry.pack()
        self.days_until_paid_entry.pack()
        self.avg_left_to_spend.pack()
        self.add_new_bill_button.pack()

    def bills_tab_builder(self):

        # Pack Widgets
        self.bills_to_pay_frame.grid(row=0, column=0)
        self.bills_to_pay_listbox.pack()
        self.bills_paid_frame.grid(row=0, column=1)
        self.bills_paid_listbox.pack()
        self.bill_info_frame.grid(row=1, column=0, columnspan=2, sticky=W+E)
        self.bill_name_entry.pack()
        self.bill_amount_entry.pack()
        self.bill_paid_checkbutton.pack()
        self.save_changes_button.pack()
        self.bill_summary_frame.grid(row=2, column=0, columnspan=2, sticky=W+E)
        self.bill_total_paid_entry.pack()
        self.bill_remains_to_pay_entry.pack()

        #  Refresh Widget Values
        self.update_values()

    def update_values(self):  # Updates values in widgets
        list_of_bills = DatabaseInteractions.get_list_of_bills()
        self.populate_bill_list_box(list_of_bills, self.bills_to_pay_listbox, False)  # False for To Pay
        self.populate_bill_list_box(list_of_bills, self.bills_paid_listbox, True)  # True for Paid

    def on_list_select_binding(self, listbox):  # Updates entry boxes/checkboxes with selected bill data
        current_selection = listbox.curselection()
        if not current_selection:  # Prevent null selections being processed
            return
        bill_name = listbox.get(current_selection[0])
        bill_amount, bill_paid = self.retrieve_info_current_selection(bill_name)
        self.bill_name_var.set(bill_name)
        self.bill_amount_var.set((selected_currency + str(bill_amount)))
        self.bill_paid_var.set(bill_paid)

    def save_changes_on_click(self):
        DatabaseInteractions.update_selected_bill(self.bill_name_var.get(),
                                                  self.bill_amount_var.get().replace(selected_currency, ""),
                                                  self.bill_paid_var.get())
        self.update_values()

    @staticmethod
    def populate_bill_list_box(bill_list, list_box, paid_listbox):
        list_box.delete(0, END)  # Removes values already in listbox to prevent duplication
        if paid_listbox:  # Variable allows method to determine which listbox is being populated
            [list_box.insert(END, bill[0]) for bill in bill_list if bill[3]]
        else:
            [list_box.insert(END, bill[0]) for bill in bill_list if not bill[3]]

    @staticmethod
    def retrieve_info_current_selection(selection_text):
        amount, paid = DatabaseInteractions.get_selected_bill_info(selection_text)
        return tuple([amount, paid])


    def add_new_bill_form(self):

        new_sub_window = AddNewBillWindow("Add New Bill", self)
        new_sub_window.build_form()


class BlankSubWindow:

    def __init__(self, title, root_window):

        self.root_window = root_window  # Master window object, refer to this to use methods from main window class
        self.root = root_window.root
        self.title = title
        self.sub_root = Toplevel()
        self.sub_root.geometry("+" + str(self.root.winfo_x() + 50) + "+" + str(self.root.winfo_y() + 50))
        self.sub_root.resizable(height=False, width=False)
        self.sub_root.transient(self.root)  # Insures sub-window is always drawn on top of master
        self.sub_root.grab_set()  # Prevents root window from being interacted with while sub window is open


class AddNewBillWindow(BlankSubWindow):
    
    def __init__(self, title, root_window):
        
        #  Call to init of super class to inherit values
        BlankSubWindow.__init__(self, title, root_window)

        # Define Variables
        self.recurring_var = BooleanVar()

        # Define Frame Widgets
        self.bill_name_frame = LabelFrame(self.sub_root, text="Name:")
        self.bill_amount_frame = LabelFrame(self.sub_root, text="Amount:")
        self.bill_notes_frame = LabelFrame(self.sub_root, text="Notes")

        # Define Entry Widgets
        self.bill_name_entry = Entry(self.bill_name_frame)
        self.bill_amount_entry = Entry(self.bill_amount_frame)

        # Define Text Box Widgets
        self.bill_notes_text = Text(self.bill_notes_frame)

        # Define Checkbutton Widgets
        self.bill_recurring_checkbutton = Checkbutton(self.bill_amount_frame, text="Recurring",
                                                      variable=self.recurring_var)

        # Define Button Widgets
        self.add_bill_button = Button(self.sub_root, text="Add Bill", command=
                                      lambda: (DatabaseInteractions.add_new_bill(self.bill_name_entry.get(),
                                                                                 float(self.bill_amount_entry.get()),
                                                                                 self.bill_notes_text.get(
                                                                                     "1.0", "end-1c"),
                                                                                 self.recurring_var.get()
                                                                                 ),
                                               self.root_window.update_values(),
                                               self.sub_root.destroy()
                                               )

                                      )

    def build_form(self):

        self.bill_name_frame.pack()
        self.bill_name_entry.pack()
        self.bill_amount_frame.pack()
        self.bill_amount_entry.pack()
        self.bill_recurring_checkbutton.pack()
        self.bill_recurring_checkbutton.select()  # Ensures checkbox is already selected by default
        self.bill_notes_frame.pack()
        self.bill_notes_text.pack()
        self.add_bill_button.pack()
