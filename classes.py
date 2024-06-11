import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

# datatime
from datetime import datetime

# Description: This file contains the class wallet, which is used to manage the wallet of the user.


class Wallet:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=["Amount", "Category", "Description", "Y", "M", "D", "Type"]
        )
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.amount = self.income - self.outcome
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )
        self.wallet_path = ""

    def add(
        self,
        amount: float,
        category: str,
        description: str,
        y: int,
        m: int,
        d: int,
        type: bool = 0,
    ):

        if type == 0:
            amount = -amount

        # non usare append, è lento
        self.df = pd.concat(
            [
                self.df,
                pd.DataFrame(
                    {
                        "Amount": [amount],
                        "Category": [category],
                        "Description": [description],
                        "Y": [y],
                        "M": [m],
                        "D": [d],
                        "Type": [type],
                    }
                ),
            ],
            ignore_index=True,
        )

        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.amount = self.income + self.outcome
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )

    def total(self):
        return self.df["Amount"].sum()

    def total_category(self, category):
        return self.df[self.df["Category"] == category]["Amount"].sum()

    def total_month(self, m):
        return self.df[self.df["M"] == m]["Amount"].sum()

    def list_category(self, category):
        return self.df[self.df["Category"] == category]

    def list_month(self, m):
        return self.df[self.df["M"] == m]

    def list_all(self):
        return self.df

    def list_income(self):
        return self.df[self.df["Type"] == 1]

    def list_outcome(self):
        return self.df[self.df["Type"] == 0]

    def get_income_category(self, category):
        return self.df[(self.df["Type"] == 1) & (self.df["Category"] == category)]

    def get_outcome_category(self, category):
        return self.df[(self.df["Type"] == 0) & (self.df["Category"] == category)]

    def sort_values_class(self, by, ascending=False):
        self.df = self.df.sort_values(by=by, ascending=ascending)

    def delete(self, index):
        self.df = self.df.drop(index)
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.amount = self.income + self.outcome
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )

    def read_csv(self, path):
        self.df = pd.read_csv(path)
        # sorta per data dalla piu recente alla meno recente
        self.df = self.df.sort_values(
            by=["Y", "M", "D", "Category", "Amount"], ascending=False
        )
        # sprta per amount dalla piu grande alla piu piccola

        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.amount = self.income + self.outcome
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )
        self.wallet_path = path

    def read_excel(self, path):
        self.df = pd.read_excel(path)
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.amount = self.income + self.outcome
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )
        self.wallet_path = path

    def read_df(self, df):
        self.df = df
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.amount = self.income + self.outcome
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )

    def plot(self):
        # plotta istogramma con colori diversi tra entrate e uscite

        # prendi solo il valore assoluto
        temp_df = self.df.copy()
        temp_df["Amount"] = temp_df["Amount"].abs()
        # somma le spese per categoria
        temp_df = temp_df.groupby(["Category", "Type"])["Amount"].sum().reset_index()

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        # vorrei che nella legenda ci fosse scritto "Income" e "Outcome" invece di 1 e 0
        sns.barplot(
            x="Category",
            y="Amount",
            data=temp_df,
            hue="Type",
            dodge=False,
            palette=["#FF6347", "#1E90FF"],
        )

        plt.title("Spese per Categorie")
        plt.xlabel("Categorie")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_time(self):
        temp_df = self.df.copy()
        temp_df["Amount"] = temp_df["Amount"].abs()
        # plotta andamento temporale delle entrate e delle uscite con istogramma mensile ma che tiene conto degli anni
        temp_df = temp_df.groupby(["M", "Y", "Type"])["Amount"].sum().reset_index()
        temp_df = temp_df.sort_values(by=["Y", "M"])

        # plot considerando anche gli anni, quindi il 3 gennaio 2022 è diverso dal 3 gennaio 2023
        # crea una colonna con la data completa
        temp_df["Date"] = temp_df["Y"].astype(str) + "-" + temp_df["M"].astype(str)
        temp_df["Date"] = pd.to_datetime(temp_df["Date"], format="%Y-%m")
        temp_df = temp_df.sort_values(by="Date")

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x="Date",
            y="Amount",
            data=temp_df,
            hue="Type",
            dodge=False,
            palette=["#FF6347", "#1E90FF"],
        )
        # controlla che categoria siano presenti

        plt.title("Spese nel Tempo")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def __repr__(self) -> str:
        return self.df.__repr__()

    def __str__(self) -> str:
        return self.df.__str__()

    def __len__(self):
        return self.df.__len__()

    def __iter__(self):
        return self.df.__iter__()


#! ----------------------------------GUI-------------------------------------


class WalletGUI:
    def __init__(self, wallet):
        # wallet è un'istanza della classe Wallet
        self.wallet: Wallet = wallet
        self.root = tk.Tk()
        self.root.configure(bg="lightgrey")
        style = ttk.Style()
        style.theme_use("clam")
        self.tree = ttk.Treeview(self.root)

        self.img = Image.open("/home/umberto/prog/money/profile_picture.ico")
        self.img = ImageTk.PhotoImage(self.img)
        self.root.tk.call("wm", "iconphoto", self.root._w, self.img)

        # tabella temporanea mostrata
        self.expenses_show = self.wallet.df

        # ---------------------------TABELLA----------------------------

        # set dimensions della tabella
        self.tree["columns"] = list(self.wallet.df.columns)
        self.tree["show"] = "headings"
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)

        # pack the treeview
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.root.title("Wallet")

        # ---------------------------BOTTONS----------------------------

        # Create a new frame for the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        # Bottone per aggiungere una spesa
        self.add_expense_button = tk.Button(
            self.button_frame, text="Nuova Spesa", command=self.add_expense
        )
        self.add_expense_button.configure(bg="lightgreen")
        self.add_expense_button.grid(row=0, column=0)  # Change this line

        # Bottone per visualizzare le spese
        self.view_expenses_button = tk.Button(
            self.button_frame, text="Visualizza Spese", command=self.view_expenses
        )
        self.view_expenses_button.grid(row=1, column=1)  # Change this line

        # Bottone per cancellare una spesa
        self.delete_expense_button = tk.Button(
            self.button_frame, text="Cancella Spesa", command=self.delete_expense
        )
        self.delete_expense_button.configure(bg="pink")
        self.delete_expense_button.grid(row=0, column=1)  # Change this line

        # Bottone per visualizzare tutte le spese
        self.default_botton = tk.Button(
            self.button_frame, text="Visualizza tutto", command=self.default_view
        )
        self.default_botton.grid(row=1, column=0)  # Change this line

        # ---------------------------BARRA DEI MENU----------------------------

        # GRAFICI

        self.menu_bar = tk.Menu(self.root)
        # Create a new 'Options' menu
        self.options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Grafici", menu=self.options_menu)

        # Add buttons to the 'Options' menu
        self.options_menu.add_command(
            label="Grafico Categorie", command=self.plot_static
        )
        self.options_menu.add_command(label="Grafico Temporale", command=self.plot_time)

        # Set the menu bar
        self.root.config(menu=self.menu_bar)

        # ordina per...
        self.sort_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ordina per...", menu=self.sort_menu)

        self.sort_menu.add_command(
            label="Categoria",
            command=lambda: self.sort_values_gui("Category"),
        )
        self.sort_menu.add_command(
            label="Importo", command=lambda: self.sort_values_gui("Amount")
        )

        # seleziona range temporale
        self.time_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Range Temporale", menu=self.time_menu)
        self.time_menu.add_command(
            label="Seleziona range", command=lambda: self.select_time()
        )

        # ---------------------------MENU----------------------------

        # aggiungi un menu per selezionare la categoria sopra la tabella
        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.pack(side=tk.LEFT)

        self.category_var_ok = tk.StringVar(self.root)
        self.category_var_ok.set("All")  # default value
        self.category_options = ["All"] + [
            "Spesa",
            "Sport",
            "Mangiare Fuori",
            "Auto",
            "Casa",
            "Bollette",
            "Altro",
            "Entrate",
            "Uscite",
        ]
        self.category_menu = tk.OptionMenu(
            self.root, self.category_var_ok, *self.category_options
        )
        self.category_menu.pack(side=tk.LEFT)

        self.month_var = tk.StringVar(self.root)
        self.month_var.set(datetime.now().month)
        # da 1 a 12
        self.month_options = ["All"] + list(range(1, 13))
        self.month_menu = tk.OptionMenu(self.root, self.month_var, *self.month_options)
        self.month_menu.pack(side=tk.RIGHT)
        self.month_label = tk.Label(self.root, text="Month:")
        self.month_label.pack(side=tk.RIGHT)

        # crea una scritta per far capire a cosa serve il menu

        self.year_var = tk.StringVar(self.root)
        # self.year_var.set("All")
        self.year_var.set(datetime.now().year)
        self.year_options = ["All"] + list(self.wallet.df["Y"].unique())
        self.year_menu = tk.OptionMenu(self.root, self.year_var, *self.year_options)
        self.year_menu.pack(side=tk.RIGHT)
        self.year_label = tk.Label(self.root, text="Year:")
        self.year_label.pack(side=tk.RIGHT)

        # ---------------------------LABELS----------------------------
        expenses = self.wallet.df
        expenses = self.draw_table(expenses)
        # Disegna la tabella
        # Create a new frame for the labels
        self.label_frame = tk.LabelFrame(self.root, text="Totals", padx=10, pady=10)
        self.label_frame.pack(padx=10, pady=10)
        self.write_totals(expenses)

    # ---------------------------FUNZIONI----------------------------

    def write_totals(self, expenses):
        # Add labels to the frame
        self.total_expenses_label = tk.Label(
            self.label_frame,
            text=f"Totale: {expenses['Amount'].sum()}",
            fg="red",
            font=("Helvetica", 12, "bold"),
        )
        self.total_expenses_label.pack()

        self.total_expenses_label_in = tk.Label(
            self.label_frame,
            text=f"Totale Entrate: {expenses[expenses['Type'] == 1]['Amount'].sum()}",
            font=("Helvetica", 12, "bold"),
        )
        self.total_expenses_label_in.pack()

        self.total_expenses_label_out = tk.Label(
            self.label_frame,
            text=f"Totale Uscite: {expenses[expenses['Type'] == 0]['Amount'].sum()}",
            font=("Helvetica", 12, "bold"),
        )
        self.total_expenses_label_out.pack()

        self.total_len = tk.Label(
            self.label_frame,
            text=f"Numero di spese: {len(expenses)}",
            font=("Helvetica", 12, "bold"),
        )
        self.total_len.pack()

    def select_time(self):
        self.add_windows_range = tk.Toplevel(self.root)
        self.add_windows_range.title("Seleziona Range Temporale")
        self.add_windows_range.geometry("400x200")

        self.title = tk.Label(
            self.add_windows_range, text="Seleziona il range temporale che preferisci:"
        )
        self.title.pack()

        self.month_label = tk.Label(self.add_windows_range, text="Da:")
        self.month_label.pack(side=tk.LEFT)

        self.month_var_range = tk.StringVar(self.add_windows_range)
        self.month_var_range.set("1")
        self.month_options = list(range(1, 13))
        self.month_menu_range = tk.OptionMenu(
            self.add_windows_range, self.month_var_range, *self.month_options
        )
        self.month_menu_range.pack(side=tk.LEFT)

        self.year_var_range = tk.StringVar(self.add_windows_range)
        self.year_var_range.set("2024")
        self.year_options = list(range(2020, 2025))
        self.year_menu_range = tk.OptionMenu(
            self.add_windows_range, self.year_var_range, *self.year_options
        )
        self.year_menu_range.pack(side=tk.LEFT)

        self.month_label = tk.Label(self.add_windows_range, text="a:")
        self.month_label.pack(side=tk.LEFT)

        self.month_var_range_end = tk.StringVar(self.add_windows_range)
        self.month_var_range_end.set("1")
        self.month_options = list(range(1, 13))
        self.month_menu_range_end = tk.OptionMenu(
            self.add_windows_range, self.month_var_range_end, *self.month_options
        )
        self.month_menu_range_end.pack(side=tk.LEFT)

        self.year_var_range_end = tk.StringVar(self.add_windows_range)
        self.year_var_range_end.set("2024")
        self.year_options = list(range(2020, 2025))
        self.year_menu_range_end = tk.OptionMenu(
            self.add_windows_range, self.year_var_range_end, *self.year_options
        )
        self.year_menu_range_end.pack(side=tk.LEFT)

        self.ok_button = tk.Button(
            self.add_windows_range, text="Filtra", command=self.select_time_ok
        )
        self.ok_button.pack(side=tk.BOTTOM)

    def select_time_ok(self):
        self.add_windows_range.destroy()
        self.month_var.set("All")
        self.year_var.set("All")

        # pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = self.wallet.df
        expenses = expenses[
            (expenses["Y"] >= int(self.year_var_range.get()))
            & (expenses["Y"] <= int(self.year_var_range_end.get()))
            & (expenses["M"] >= int(self.month_var_range.get()))
            & (expenses["M"] <= int(self.month_var_range_end.get()))
        ]
        expenses = self.draw_table(expenses)
        # cancella il vecchio label e aggiungi il nuovo
        for widget in self.label_frame.winfo_children():
            widget.destroy()

        self.write_totals(expenses)

    def add_expense(self):
        self.add_expense_window = tk.Toplevel(self.root)
        self.add_expense_window.title("Nuova Spesa")
        # set the size of the window

        self.add_expense_window.geometry("300x290")

        self.amount_label = tk.Label(self.add_expense_window, text="Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.add_expense_window)
        self.amount_entry.pack()

        self.category_label = tk.Label(self.add_expense_window, text="Category")
        self.category_label.pack()

        self.category_var = tk.StringVar(self.add_expense_window)
        self.category_var.set("Spesa")  # default value
        self.category_options = [
            "Spesa",
            "Sport",
            "Mangiare Fuori",
            "Auto",
            "Casa",
            "Bollette",
            "Altro",
            "Entrate",
        ]
        self.category_menu = tk.OptionMenu(
            self.add_expense_window, self.category_var, *self.category_options
        )
        self.category_menu.pack()

        self.description_label = tk.Label(self.add_expense_window, text="Description *")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.add_expense_window)
        self.description_entry.pack()

        self.date_label = tk.Label(self.add_expense_window, text="Date (YYYY-MM-DD) *")
        self.date_label.pack()

        self.date_entry = tk.Entry(self.add_expense_window)
        self.date_entry.pack()

        self.type_label = tk.Label(self.add_expense_window, text="Type")
        self.type_label.pack()

        self.type_var = tk.StringVar(value="expense")
        self.expense_radiobutton = tk.Radiobutton(
            self.add_expense_window,
            text="In uscita",
            variable=self.type_var,
            value="expense",
        )
        self.expense_radiobutton.pack()
        self.income_radiobutton = tk.Radiobutton(
            self.add_expense_window,
            text="In entrata",
            variable=self.type_var,
            value="income",
        )
        self.income_radiobutton.pack()

        self.information = tk.Label(self.add_expense_window, text="* opzionale")
        # sposta un po in basso il label

        self.information.pack(pady=10)

        self.submit_button = tk.Button(
            self.add_expense_window, text="Aggiungi", command=self.submit_expense
        )
        self.submit_button.configure(bg="lightgreen")
        self.submit_button.pack(side=tk.BOTTOM)

    def submit_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_var.get()
        description = self.description_entry.get()
        date = self.date_entry.get()
        if date:
            year, month, day = map(int, date.split("-"))
        else:
            now = datetime.now()
            year, month, day = now.year, now.month, now.day

        self.wallet.add(amount, category, description, year, month, day)
        self.add_expense_window.destroy()

        self.wallet.df.to_csv("wallet.csv", index=False)
        self.view_expenses()

    def view_expenses(self):
        # pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = self.wallet.df

        expenses = self.draw_table(expenses)

        # cancella il vecchio label e aggiungi il nuovo
        for widget in self.label_frame.winfo_children():
            widget.destroy()

        self.write_totals(expenses)

    def draw_table(self, expenses):

        if self.category_var_ok.get() == "Entrate":
            expenses = expenses[expenses["Type"] == 1]
        elif self.category_var_ok.get() == "Uscite":
            expenses = expenses[expenses["Type"] == 0]
        elif self.category_var_ok.get() != "All":
            expenses = expenses[expenses["Category"] == self.category_var_ok.get()]

        if self.month_var.get() != "All":
            expenses = expenses[expenses["M"] == int(self.month_var.get())]

        if self.year_var.get() != "All":
            expenses = expenses[expenses["Y"] == int(self.year_var.get())]

        if expenses.empty:
            messagebox.showinfo("Info", "No expenses found.")
        else:
            self.tree["columns"] = list(expenses.columns)
            for column in self.tree["columns"]:
                self.tree.heading(column, text=column)

            for index, row in expenses.iterrows():
                self.tree.insert("", "end", values=list(row))

        self.expenses_show = expenses

        return expenses

    def default_view(self):
        self.month_var.set("All")
        self.year_var.set("All")
        self.view_expenses()

    def sort_values_gui(self, column):

        # pulisci la tabella
        for item in self.tree.get_children():
            self.tree.delete(item)

        expenses = self.wallet.df
        new_wallet = Wallet()
        new_wallet.read_df(expenses)
        new_wallet.sort_values_class(column, ascending=False)

        expenses = new_wallet.df

        expenses = self.draw_table(expenses)

    def delete_expense(self):

        # prendi il numero della riga selezionata
        selected = self.tree.selection()

        # open a dialog box to confirm the deletion
        if not selected:
            messagebox.showerror("Errore", "Nessuna riga selezionata")
            return

        row_index = self.tree.item(selected[0])["values"][0]
        self.delete_window = tk.Toplevel(self.root)
        self.delete_window.title("Sei sicuro?")
        self.delete_window.geometry("200x100")
        self.yes_button = tk.Button(
            self.delete_window,
            text="Si",
            command=lambda: self.delete_expense_ok(row_index=row_index),
        )
        self.yes_button.configure(bg="lightgreen")
        self.yes_button.pack(expand=True)
        self.no_button = tk.Button(
            self.delete_window, text="No", command=self.delete_expense_cancel
        )
        self.no_button.configure(bg="pink")
        self.no_button.pack(expand=True)

    def delete_expense_cancel(self):
        self.delete_window.destroy()

    def delete_expense_ok(self, row_index):
        self.wallet.delete(row_index)
        self.wallet.df.to_csv(self.wallet.wallet_path, index=False)
        self.view_expenses()
        self.delete_window.destroy()

    def plot_static(self):
        expenses = self.expenses_show

        new_wallet = Wallet()
        new_wallet.read_df(expenses)

        new_wallet.plot()

    def plot_time(self):
        expenses = self.expenses_show

        new_wallet = Wallet()
        new_wallet.read_df(expenses)

        new_wallet.plot_time()

    def run(self):
        self.root.mainloop()
