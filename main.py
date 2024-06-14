from wallet import *
from GUI import *
import os

# crea un objeto della classe Wallet
wallet = Wallet()

# legge i dati dal file csv
dir_path = os.path.dirname(os.path.realpath(__file__))
wallet_path = os.path.join(dir_path, "dati", "wallet.csv")

# plotta i dati del mese corrente
now = datetime.now()

df = pd.read_csv(wallet_path)

df = df[df["M"] == int(now.month)]
df = df[df["Y"] == int(now.year)]

df = df.reset_index(drop=True)
w = Wallet()
# w.read_df(df)
# w.plot()
# w.plot_time()
# w.plot_pie()
# w.plot_pie_with_all_categories()


# se il percorso del file esiste, legge i dati
if os.path.exists(wallet_path):
    wallet.read_csv(wallet_path)

gui = WalletGUI(wallet)
gui.run()
