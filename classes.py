import pandas as pd

# Description: This file contains the class wallet, which is used to manage the wallet of the user.

class Wallet:
    def __init__(self):
        self.df = pd.DataFrame(columns=['Amount', 'Category', 'Description','Y', 'M', 'D','Type'])
        self.outcome = self.df[self.df['Type'] == 0]['Amount'].sum()
        self.income = self.df[self.df['Type'] == 1]['Amount'].sum()
        self.amount = self.income - self.outcome
        self.categories = self.df['Category'].unique()
        self.start_date = (self.df['Y'].min(), self.df[self.df['Y'] == self.df['Y'].min()]['M'].min())
        self.end_date = (self.df['Y'].max(), self.df[self.df['Y'] == self.df['Y'].max()]['M'].max())


    
    def add(self, amount: float, category: str, description: str , y: int, m: int, d: int, type: bool = 0):

        if type == 0:
            amount = -amount

        # non usare append, è lento
        self.df = pd.concat([self.df, pd.DataFrame({'Amount': [amount], 'Category': [category], 'Description': [description], 'Y': [y], 'M': [m], 'D': [d], 'Type': [type]})], ignore_index=True)

        self.outcome = self.df[self.df['Type'] == 0]['Amount'].sum()
        self.income = self.df[self.df['Type'] == 1]['Amount'].sum()
        self.amount = self.income - self.outcome
        self.categories = self.df['Category'].unique()
        self.start_date = (self.df['Y'].min(), self.df[self.df['Y'] == self.df['Y'].min()]['M'].min())
        self.end_date = (self.df['Y'].max(), self.df[self.df['Y'] == self.df['Y'].max()]['M'].max())
        

    def total(self):
        return self.df['Amount'].sum()
    
    def total_category(self, category):
        return self.df[self.df['Category'] == category]['Amount'].sum()
    
    def total_month(self, m):
        return self.df[self.df['M'] == m]['Amount'].sum()
    
    def list_category(self, category):
        return self.df[self.df['Category'] == category]
    
    def list_month(self, m):
        return self.df[self.df['M'] == m]
    
    def list_all(self):
        return self.df
    
    def list_income(self):
        return self.df[self.df['Type'] == 1]
    
    def list_outcome(self):
        return self.df[self.df['Type'] == 0]
    
    def __repr__(self) -> str:
        return self.df.__repr__()
    
    def __str__(self) -> str:
        return self.df.__str__()

    def __len__(self):
        return self.df.__len__()
    
    def __iter__(self):
        return self.df.__iter__()

    