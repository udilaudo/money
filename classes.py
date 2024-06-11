import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        plt.title("Expenses by Category")
        plt.xlabel("Category")
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
        plt.title("Expenses by Month")
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
