import tkinter as tk
from tkinter import ttk, messagebox
from classes import Wallet
from PIL import Image, ImageTk

# datatime
from datetime import datetime


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
        self.menu_bar.add_cascade(label="Ordina per", menu=self.sort_menu)

        self.sort_menu.add_command(
            label="Categoria",
            command=lambda: self.sort_values_gui("Category"),
        )
        self.sort_menu.add_command(
            label="Importo", command=lambda: self.sort_values_gui("Amount")
        )

        # seleziona range temporale
        self.time_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(
            label="Seleziona Range Temporale", menu=self.time_menu
        )
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

        self.description_label = tk.Label(self.add_expense_window, text="Description")
        self.description_label.pack()
        self.description_entry = tk.Entry(self.add_expense_window)
        self.description_entry.pack()

        self.date_label = tk.Label(self.add_expense_window, text="Date (YYYY-MM-DD)")
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

        self.submit_button = tk.Button(
            self.add_expense_window, text="Aggiungi", command=self.submit_expense
        )
        self.submit_button.pack()

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

    # def delete_expense(self):
    #    selected = self.tree.selection()
    #    print("AAAAAAAAAAAAAAAA", selected, selected[0])
    #    if selected:
    #        index = self.tree.index(selected)
    #        self.wallet.delete(index)
    #        self.wallet.df.to_csv("wallet.csv", index=False)
    #        self.view_expenses()
    #    else:
    #        messagebox.showinfo("Info", "Select an expense to delete.")

    def delete_expense(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            self.wallet.delete(index)
            self.wallet.df.to_csv("wallet.csv", index=False)
            self.view_expenses()
        else:
            messagebox.showinfo("Info", "Select an expense to delete.")

    def plot_static(self):
        expenses = self.wallet.df

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
        new_wallet = Wallet()
        new_wallet.read_df(expenses)

        new_wallet.plot()

    def plot_time(self):
        expenses = self.wallet.df

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
        new_wallet = Wallet()
        new_wallet.read_df(expenses)

        new_wallet.plot_time()

    def run(self):
        self.root.mainloop()


wallet = Wallet()  # Assuming Wallet is the class from classes.py
wallet.read_csv("wallet_sim.csv")

gui = WalletGUI(wallet)
gui.run()
