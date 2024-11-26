import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
from datetime import datetime, timedelta


# Description: This file contains the class wallet, which is used to manage the wallet of the user.
class Wallet:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=[
                "ID",
                "Amount",
                "Category",
                "Description",
                "Y",
                "M",
                "D",
                "Conto",
                "Type",
            ]
        )
        # Type 0 = spesa, Type 1 = entrata, Type 2 = saldo iniziale uscita, Type 3 = saldo iniziale entrata, Type 4 = giroconto
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
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
        self.wallet_name = ""

    def add(
        self,
        amount: float,
        category: str,
        description: str,
        y: int,
        m: int,
        d: int,
        conto: str = "Conto",
        type: bool = 0,
    ):

        if type == 0:
            amount = -amount

        # aumenta di 1 l'indice ID di ogni riga
        self.df["ID"] = self.df["ID"].apply(lambda x: x + 1)

        # non usare append, è lento
        self.df = pd.concat(
            [
                self.df,
                pd.DataFrame(
                    {
                        "ID": [0],
                        "Amount": [amount],
                        "Category": [category],
                        "Description": [description],
                        "Y": [y],
                        "M": [m],
                        "D": [d],
                        "Conto": [conto],
                        "Type": [type],
                    }
                ),
            ],
            ignore_index=True,
        )

        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
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
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )

    def filter_dataset_from_date(self, n_days_ago: int) -> pd.DataFrame:
        # Data attuale
        now = datetime.now()
        year, month, day = now.year, now.month, now.day

        thirty_days_ago = now - timedelta(days=n_days_ago)
        # plotta i dati del mese corrente
        self.df = self.df[self.df["Y"] >= int(thirty_days_ago.year)]
        self.df = self.df[self.df["M"] >= int(thirty_days_ago.month)]
        if thirty_days_ago.year == now.year:
            self.df = self.df[self.df["M"] >= int(thirty_days_ago.month)]
        else:
            self.df = self.df[
                (
                    (
                        (self.df["M"] >= thirty_days_ago.day)
                        & (self.df["Y"] == thirty_days_ago.month)
                    )
                    | ((self.df["M"] <= now.day) & (self.df["Y"] == now.month))
                )
            ]
        if thirty_days_ago.month == now.month:
            self.df = self.df[self.df["D"] >= int(thirty_days_ago.day)]
        self.df = self.df[
            (
                (
                    (self.df["D"] >= thirty_days_ago.day)
                    & (self.df["M"] == thirty_days_ago.month)
                )
                | ((self.df["D"] <= now.day) & (self.df["M"] == now.month))
            )
        ]

        self.df = self.df.reset_index(drop=True)

    def giroconto(
        self,
        amount,
        conto_out,
        conto_in,
        y,
        m,
        d,
        y_firts=2023,
        m_first=12,
        d_first=31,
    ):
        category = "Saldo"
        description = f"da {conto_out} a {conto_in}"
        self.add(amount, "Giroconto", description, y, m, d, None, 4)

        self.add(
            -amount, category, description, y_firts, m_first, d_first, conto_out, 2
        )
        self.add(amount, category, description, y_firts, m_first, d_first, conto_in, 3)

        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
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
        #
        self.df = self.df.reset_index(drop=True)
        # riordina gli ID
        self.df["ID"] = self.df.index
        # sprta per amount dalla piu grande alla piu piccola

        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
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
        self.wallet_name = path.split("/")[-1]

    def read_excel(self, path):
        self.df = pd.read_excel(path)
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
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
        self.wallet_name = path.split("/")[-1]

    def read_df(self, df):
        self.df = df
        self.outcome = self.df[self.df["Type"] == 0]["Amount"].sum()
        self.income = self.df[self.df["Type"] == 1]["Amount"].sum()
        self.inital_saldo_out = self.df[(self.df["Type"] == 2)]["Amount"].sum()
        self.inital_saldo_in = self.df[(self.df["Type"] == 3)]["Amount"].sum()
        self.amount = (
            self.income - self.outcome + self.inital_saldo_in - self.inital_saldo_out
        )
        self.categories = self.df["Category"].unique()
        self.start_date = (
            self.df["Y"].min(),
            self.df[self.df["Y"] == self.df["Y"].min()]["M"].min(),
        )
        self.end_date = (
            self.df["Y"].max(),
            self.df[self.df["Y"] == self.df["Y"].max()]["M"].max(),
        )

    def plot(self, show=True):
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

        plt.title("Expenses by Category")
        plt.xlabel("Categories")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("./plots/category_bar_plot.png")

        # non voglio farlo vedere neanche se plt.show() è chiamato in seguito ad altre funzioni
        if show:
            plt.show()
        else:
            plt.close()

    def plot_time(self, show=True):
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

        # cancella il giorno dalla data
        temp_df["Date"] = temp_df["Date"].dt.to_period("M")

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

        plt.title("Expenses Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("./plots/time_bar_plot.png")
        if show:
            plt.show()
        else:
            plt.close()

    def plot_pie(self, show=True):
        # plotta un grafico a torta con le entrate e le uscite
        # se ci sono sia entrate che uscite
        if (self.income + self.inital_saldo_in) != 0 and (
            self.outcome + self.inital_saldo_out
        ) != 0:
            temp_df = self.df.copy()
            temp_df["Amount"] = temp_df["Amount"].abs()
            temp_df = temp_df.groupby("Type")["Amount"].sum().reset_index()

            plt.figure(figsize=(10, 6))
            plt.pie(
                temp_df["Amount"],
                labels=["Income", "Outcome"],
                autopct="%1.1f%%",
                colors=["#1E90FF", "#FF6347"],
            )
            plt.title("Income and Outcome")
            plt.savefig("./plots/in_out_pie_plot.png")
            if show:
                plt.show()
            else:
                plt.close()
        elif (self.outcome + self.inital_saldo_out) == 0:
            # fare un grafico a torta solo con le entrate con una torta piena al 100%
            plt.figure(figsize=(10, 6))
            plt.pie([1], labels=["Income"], autopct="%1.1f%%", colors=["#1E90FF"])
            plt.title("Entrate e Uscite")
            plt.savefig("./plots/in_out_pie_plot.png")
            if show:
                plt.show()
            else:
                plt.close()

        elif (self.income + self.inital_saldo_in) == 0:
            # fare un grafico a torta solo con le uscite con una torta piena al 100%
            plt.figure(figsize=(10, 6))
            plt.pie([1], labels=["Outcome"], autopct="%1.1f%%", colors=["#FF6347"])
            plt.title("Income and Outcome")
            plt.savefig("./plots/in_out_pie_plot.png")
            if show:
                plt.show()
            else:
                plt.close()

    def plot_pie_with_all_categories(self, show=True):
        # plotta un grafico a torta con tutte le categorie diverse di spese
        temp_df = self.df.copy()
        temp_df["Amount"] = temp_df["Amount"].abs()
        temp_df = temp_df.groupby("Category")["Amount"].sum().reset_index()

        color_cycler = cycler(color=plt.get_cmap("tab10").colors)
        colors = [
            "green" if category == "Entrate" else color_cycler.by_key()["color"][i % 10]
            for i, category in enumerate(temp_df["Category"])
        ]

        plt.figure(figsize=(10, 6))
        plt.pie(
            temp_df["Amount"],
            labels=temp_df["Category"],
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,  # Usa la lista di colori
        )
        plt.title("Expenses by Category")
        plt.savefig("./plots/category_pie_plot.png")
        if show:
            plt.show()
        else:
            plt.close()

    def plot_pie_conto(self, show=True):
        # plotta un grafico a torta con tutte le categorie diverse di spese
        temp_df = self.df.copy()
        temp_df["Amount"] = temp_df["Amount"].abs()
        temp_df = temp_df.groupby("Conto")["Amount"].sum().reset_index()

        color_cycler = cycler(color=plt.get_cmap("tab10").colors)
        colors = [
            "green" if category == "Entrate" else color_cycler.by_key()["color"][i % 10]
            for i, category in enumerate(temp_df["Conto"])
        ]

        plt.figure(figsize=(10, 6))
        plt.pie(
            temp_df["Amount"],
            labels=temp_df["Conto"],
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,  # Usa la lista di colori
        )
        plt.title("Expenses Across Different Accounts")
        plt.savefig("./plots/conto_pie_plot.png")
        if show:
            plt.show()
        else:
            plt.close()

    def __repr__(self) -> str:
        return self.df.__repr__()

    def __str__(self) -> str:
        return self.df.__str__()

    def __len__(self):
        return self.df.__len__()

    def __iter__(self):
        return self.df.__iter__()
