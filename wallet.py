from classes import *
import os

# crea un objeto della classe Wallet
wallet = Wallet()

# legge i dati dal file csv
dir_path = os.path.dirname(os.path.realpath(__file__))
wallet_path = os.path.join(dir_path, "dati", "wallet_sim_sort_id.csv")

# se il percorso del file esiste, legge i dati
if os.path.exists(wallet_path):
    wallet.read_csv(wallet_path)

gui = WalletGUI(wallet)
gui.run()
