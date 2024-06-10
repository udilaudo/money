import tkinter as tk
from tkinter import ttk, messagebox
from classes import Wallet
import pandas as pd
# datatime
from datetime import datetime

    

class WalletGUI:
    def __init__(self, wallet):
        self.wallet: Wallet = wallet
        self.root = tk.Tk()
        self.tree = ttk.Treeview(self.root)



        # set dimensions della tabella
        self.tree["columns"] = list(self.wallet.df.columns)
        self.tree["show"] = "headings"
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)
        
        # pack the treeview
        self.tree.pack()
        self.root.title("Wallet")

        self.add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.view_expenses_button = tk.Button(self.root, text="View Expenses", command=self.view_expenses)
        self.view_expenses_button.pack()

        self.view_plot = tk.Button(self.root, text="Grafico Categorie", command=self.plot_static)
        self.view_plot.pack()

        self.view_plot_time = tk.Button(self.root, text="Grafico Temporale", command=self.plot_time)
        self.view_plot_time.pack()
        
        # aggiungi un menu per selezionare la categoria sopra la tabella
        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.pack(side=tk.LEFT)

        self.category_var_ok = tk.StringVar(self.root)
        self.category_var_ok.set("All")  # default value
        self.category_options = ["All"] + ["Spesa", "Sport", "Mangiare Fuori", "Auto", "Casa", "Altro", "Entrate", "Uscite"]
        self.category_menu = tk.OptionMenu(self.root, self.category_var_ok, *self.category_options)
        self.category_menu.pack(side=tk.LEFT)

        self.month_var = tk.StringVar(self.root)
        self.month_var.set("All")  # default value
        # month_options tutti i mesi tra il piu vecchio mese e il piu recente mese presenti considerando anche gli anni. tipo 2023-9 , 2023-10, 2023-11, 2023-12, 2024-1, 2024-2, 2024-3
        self.month_options = ["All"] + [f"{year}-{month}" for year in range(self.wallet.df['Y'].min(), self.wallet.df['Y'].max() + 1) for month in range(1, 13)]
        self.month_menu = tk.OptionMenu(self.root, self.month_var, *self.month_options)
        self.month_menu.pack(side=tk.RIGHT) 
        self.month_label = tk.Label(self.root, text="Month:")
        self.month_label.pack(side=tk.RIGHT)       

        # crea una scritta per far capire a cosa serve il menu
        

        self.year_var = tk.StringVar(self.root)
        self.year_var.set("All")
        self.year_options = ["All"] + list(self.wallet.df['Y'].unique())
        self.year_menu = tk.OptionMenu(self.root, self.year_var, *self.year_options)
        self.year_menu.pack(side=tk.RIGHT)
        self.year_label = tk.Label(self.root, text="Year:")
        self.year_label.pack(side=tk.RIGHT)

        expenses = self.wallet.df
        if expenses.empty:
            messagebox.showinfo("Info", "No expenses found.")
        else:
            self.tree['columns'] = list(expenses.columns)
            for column in self.tree['columns']:
                self.tree.heading(column, text=column)

            for index, row in expenses.iterrows():
                self.tree.insert('', 'end', values=list(row))

        # aggiungi un label per il totale delle spese
        self.total_expenses_label = tk.Label(self.root, text=f"Totale: {self.wallet.amount}")
        self.total_expenses_label.pack()
        self.total_expenses_label_in = tk.Label(self.root, text=f"Totale Entrate: {self.wallet.income}")
        self.total_expenses_label_in.pack()
        self.total_expenses_label_out = tk.Label(self.root, text=f"Totale Uscite: {self.wallet.outcome}")
        self.total_expenses_label_out.pack()



    def add_expense(self):
        self.add_expense_window = tk.Toplevel(self.root)
        self.add_expense_window.title("Add Expense")
    
        self.amount_label = tk.Label(self.add_expense_window, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.add_expense_window)
        self.amount_entry.pack()
    
        self.category_label = tk.Label(self.add_expense_window, text="Category")
        self.category_label.pack()

        self.category_var = tk.StringVar(self.add_expense_window)
        self.category_var.set("Spesa")  # default value
        self.category_options = ["Spesa", "Sport", "Mangiare Fuori", "Auto", "Casa", "Altro", "Entrate"]
        self.category_menu = tk.OptionMenu(self.add_expense_window, self.category_var, *self.category_options)
        self.category_menu.pack()
    
        self.description_label = tk.Label(self.add_expense_window, text="Description")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.add_expense_window)
        self.description_entry.pack()
    
        self.date_label = tk.Label(self.add_expense_window, text="Date (YYYY-MM-DD)")
        self.date_label.pack()

        self.date_entry = tk.Entry(self.add_expense_window)
        self.date_entry.pack()
    
        self.submit_button = tk.Button(self.add_expense_window, text="Submit", command=self.submit_expense)
        self.submit_button.pack()

        self.type_label = tk.Label(self.add_expense_window, text="Type")
        self.type_label.pack()

        self.type_var = tk.StringVar(value="expense")
        self.expense_radiobutton = tk.Radiobutton(self.add_expense_window, text="Expense", variable=self.type_var, value="expense")
        self.expense_radiobutton.pack()
        self.income_radiobutton = tk.Radiobutton(self.add_expense_window, text="Income", variable=self.type_var, value="income")
        self.income_radiobutton.pack()

        self.submit_button = tk.Button(self.add_expense_window, text="Submit", command=self.submit_expense)
        self.submit_button.pack()

    def submit_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_var.get()
        description = self.description_entry.get()
        date = self.date_entry.get()
        if date:
            year, month, day = map(int, date.split('-'))
        else:
            now = datetime.now()
            year, month, day = now.year, now.month, now.day
    
        self.wallet.add(amount, category, description, year, month, day)
        self.add_expense_window.destroy()

        self.wallet.df.to_csv('wallet.csv', index=False)


    def view_expenses(self):
        # pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = self.wallet.df

        #if self.category_var_ok.get() != "All":
        #    expenses = expenses[expenses['Category'] == self.category_var_ok.get()]
        if self.category_var_ok.get() == "Entrate":
            expenses = expenses[expenses['Type'] == 1]
        elif self.category_var_ok.get() == "Uscite":
            expenses = expenses[expenses['Type'] == 0]
        elif self.category_var_ok.get() != "All":
            expenses = expenses[expenses['Category'] == self.category_var_ok.get()]

        if self.month_var.get() != "All":
            expenses = expenses[(expenses['Y'] == int(self.month_var.get().split('-')[0])) & (expenses['M'] == int(self.month_var.get().split('-')[1]))]

        if self.year_var.get() != "All":
            expenses = expenses[expenses['Y'] == int(self.year_var.get())]

        if expenses.empty:
            messagebox.showinfo("Info", "No expenses found.")
        else:
            self.tree['columns'] = list(expenses.columns)
            for column in self.tree['columns']:
                self.tree.heading(column, text=column)

            for index, row in expenses.iterrows():
                self.tree.insert('', 'end', values=list(row))

    

        # cancella il vecchio label e aggiungi il nuovo
        self.total_expenses_label.destroy()

        self.total_expenses_label = tk.Label(self.root, text=f"Totale: {expenses['Amount'].sum()}")
        self.total_expenses_label.pack()
        self.total_expenses_label_in.destroy()
        self.total_expenses_label_in = tk.Label(self.root, text=f"Totale Entrate: {expenses[expenses['Type'] == 1]['Amount'].sum()}")
        self.total_expenses_label_in.pack()
        self.total_expenses_label_out.destroy()
        self.total_expenses_label_out = tk.Label(self.root, text=f"Totale Uscite: {expenses[expenses['Type'] == 0]['Amount'].sum()}")
        self.total_expenses_label_out.pack()
        
    def plot_static(self):
        expenses = self.wallet.df

        if self.category_var_ok.get() == "Entrate":
            expenses = expenses[expenses['Type'] == 1]
        elif self.category_var_ok.get() == "Uscite":
            expenses = expenses[expenses['Type'] == 0]
        elif self.category_var_ok.get() != "All":
            expenses = expenses[expenses['Category'] == self.category_var_ok.get()]

        if self.month_var.get() != "All":
            expenses = expenses[(expenses['Y'] == int(self.month_var.get().split('-')[0])) & (expenses['M'] == int(self.month_var.get().split('-')[1]))]

        if self.year_var.get() != "All":
            expenses = expenses[expenses['Y'] == int(self.year_var.get())]
        new_wallet = Wallet()
        new_wallet.read_df(expenses)

        new_wallet.plot()

    def plot_time(self):
        expenses = self.wallet.df

        if self.category_var_ok.get() == "Entrate":
            expenses = expenses[expenses['Type'] == 1]
        elif self.category_var_ok.get() == "Uscite":
            expenses = expenses[expenses['Type'] == 0]
        elif self.category_var_ok.get() != "All":
            expenses = expenses[expenses['Category'] == self.category_var_ok.get()]

        if self.month_var.get() != "All":
            expenses = expenses[(expenses['Y'] == int(self.month_var.get().split('-')[0])) & (expenses['M'] == int(self.month_var.get().split('-')[1]))]

        if self.year_var.get() != "All":
            expenses = expenses[expenses['Y'] == int(self.year_var.get())]
        new_wallet = Wallet()
        new_wallet.read_df(expenses)

        new_wallet.plot_time()


    def run(self):
        self.root.mainloop()

wallet = Wallet()  # Assuming Wallet is the class from classes.py
wallet.read_csv('wallet.csv')
print(wallet.df)
print(wallet.amount)



gui = WalletGUI(wallet)
gui.run()
