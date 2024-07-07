import os

from GUI import *
from wallet import *


# legge i dati dal file csv
dir_path = os.path.dirname(os.path.realpath(__file__))
wallet_path = os.path.join(dir_path, "dati", "my_wallet.csv")

# plotta i dati del mese corrente
now = datetime.now()
df = pd.read_csv(wallet_path)

df = df[df["M"] == int(now.month)]
df = df[df["Y"] == int(now.year)]

df = df.reset_index(drop=True)
w = Wallet()
w.read_df(df)
# w.plot(show=False)
# w.plot_time(show=False)
# w.plot_pie(show=False)
# w.plot_pie_with_all_categories(show=False)

del df, w

# crea un objeto della classe Wallet
wallet = Wallet()

# se il percorso del file esiste, legge i dati
if os.path.exists(wallet_path):
    wallet.read_csv(wallet_path)

gui = WalletGUI(wallet)
gui.run()
