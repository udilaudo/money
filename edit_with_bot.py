# Stati per la conversazione
from datetime import datetime, timedelta
import os
import pandas as pd
from tabulate import tabulate
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    filters,
)
from wallet import Wallet


# Token del bot
TOKEN = os.getenv("TELEGRAM_TOKEN_WALLET")

# Chat ID autorizzato
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Percorso del file csv
CSV_FILE_PATH = "/home/umberto/prog/money/dati/my_wallet.csv"

# Data attuale
now = datetime.now()
year, month, day = now.year, now.month, now.day

start_date = now - timedelta(days=30)

# Stati per la conversazione
START, COLUMN1, COLUMN2, COLUMN3, COLUMN4, DATI = range(6)

# ---------------------------- Funzioni ----------------------------


def is_authorized(chat_id: int) -> bool:
    return str(chat_id) == AUTHORIZED_CHAT_ID


async def start(update: Update, context: CallbackContext) -> int:
    if not is_authorized(update.effective_chat.id):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("Aggiungi spesa", callback_data="modifica")],
        [InlineKeyboardButton("Aggiungi entrata", callback_data="entrata")],
        [InlineKeyboardButton("Visualizza Dati", callback_data="dati")],
        [InlineKeyboardButton("Grafico In-Out", callback_data="grafico_totale")],
        [InlineKeyboardButton("Grafico Uscite", callback_data="grafico_solo_uscite")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Scegli un'opzione:", reply_markup=reply_markup)
    return START


async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # salva il risultato della query
    context.user_data["query"] = query

    if query.data == "modifica":
        await query.edit_message_text(text="Quanto hai speso?")
        return COLUMN1
    elif query.data == "entrata":
        await query.edit_message_text(text="Quanto hai ricevuto?")
        return COLUMN1
    elif query.data == "dati":
        # legge i dati dal file csv
        df = pd.read_csv(CSV_FILE_PATH)

        # plotta i dati degli ultimi 30 giorni
        df = df[df["Y"] >= int(start_date.year)]
        df = df[df["M"] >= int(start_date.month)]
        df = df[df["D"] >= int(start_date.day)]

        df = df.reset_index(drop=True)

        # elimina le colonne ID e Type
        df = df.drop(columns=["ID", "Type"])

        table = tabulate(df, headers="keys", tablefmt="pretty", showindex="never")

        await query.message.reply_text(f"```\n{table}\n```", parse_mode="MarkdownV2")

        return ConversationHandler.END
    elif query.data == "grafico_totale":
        # legge i dati dal file csv
        df = pd.read_csv(CSV_FILE_PATH)

        # plotta i dati del mese corrente
        df = df[df["Y"] >= int(start_date.year)]
        df = df[df["M"] >= int(start_date.month)]
        df = df[df["D"] >= int(start_date.day)]

        df = df.reset_index(drop=True)

        w = Wallet()
        w.read_df(df)
        w.plot_pie_with_all_categories(show=False)

        # calcola il totale delle spese in uscita
        total_out = round(w.outcome, 2)
        total_in = round(w.income, 2)
        saldo = total_in - total_out

        # invia il grafico
        await query.message.reply_photo(
            photo=open("./plots/category_pie_plot.png", "rb"),
            caption=f"Uscite: {total_out} € \nEntrate: {total_in} € \nSaldo: {saldo} €",
        )

        return ConversationHandler.END

    elif query.data == "grafico_solo_uscite":
        # legge i dati dal file csv
        df = pd.read_csv(CSV_FILE_PATH)

        # plotta i dati del mese corrente
        df = df[df["Y"] >= int(start_date.year)]
        df = df[df["M"] >= int(start_date.month)]
        df = df[df["D"] >= int(start_date.day)]

        # elimina le entrate
        df = df[df["Type"] == 0]

        df = df.reset_index(drop=True)

        w = Wallet()
        w.read_df(df)
        w.plot_pie_with_all_categories(show=False)

        # calcola il totale delle spese in uscita
        total_out = round(w.outcome, 2)
        # calcola le spese per ogni categoria
        all_tot = []
        for category in w.categories:
            tot = round(w.df[w.df["Category"] == category]["Amount"].sum(), 2)
            all_tot.append((category, tot))

        all_tot = sorted(all_tot, key=lambda x: x[1])

        string_to_print = ""
        for cat, tot in all_tot:
            string_to_print += f"{cat}: {tot} € \n"

        # invia il grafico
        await query.message.reply_photo(
            photo=open("./plots/category_pie_plot.png", "rb"),
            caption=f"Uscite totali: {total_out} € \n{string_to_print}",
        )

        return ConversationHandler.END


async def column1(update: Update, context: CallbackContext) -> int:
    if not is_authorized(update.effective_chat.id):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return ConversationHandler.END

    context.user_data["column1"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Spesa", callback_data="Spesa")],
        [InlineKeyboardButton("Sport", callback_data="Sport")],
        [InlineKeyboardButton("Mangiare fuori", callback_data="Mangiare fuori")],
        [InlineKeyboardButton("Auto", callback_data="Auto")],
        [InlineKeyboardButton("Casa", callback_data="Casa")],
        [InlineKeyboardButton("Bollette", callback_data="Bollette")],
        [InlineKeyboardButton("Altro", callback_data="Altro")],
        [InlineKeyboardButton("Entrate", callback_data="Entrate")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Seleziona la categoria:", reply_markup=reply_markup
    )
    return COLUMN2


async def column2(update: Update, context: CallbackContext) -> int:
    query_category = update.callback_query
    await query_category.answer()

    # context.user_data["column2"] = update.message.text
    context.user_data["column2"] = update.callback_query.data
    await query_category.edit_message_text(text="Inserisci la descrizione:")
    return COLUMN3


async def column3(update: Update, context: CallbackContext) -> int:
    if not is_authorized(update.effective_chat.id):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return ConversationHandler.END

    context.user_data["column3"] = update.message.text

    keyboard = [
        [InlineKeyboardButton("Evolution", callback_data="evolution")],
        [InlineKeyboardButton("Bancoposta", callback_data="bancoposta")],
        [InlineKeyboardButton("Contanti", callback_data="contanti")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Con cosa hai pagato?", reply_markup=reply_markup)
    return COLUMN4


async def column4(update: Update, context: CallbackContext) -> int:
    if not is_authorized(update.effective_chat.id):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return ConversationHandler.END

    query_conto = update.callback_query
    await query_conto.answer()

    # context.user_data["column2"] = update.message.text
    context.user_data["column4"] = update.callback_query.data

    if context.user_data["query"].data == "modifica":
        costo = -int(context.user_data["column1"])
        tipo = 0
    elif context.user_data["query"].data == "entrata":
        costo = int(context.user_data["column1"])
        tipo = 1

    new_row = {
        "ID": 0,
        "Amount": costo,
        "Category": context.user_data["column2"],
        "Description": context.user_data["column3"],
        "Y": year,
        "M": month,
        "D": day,
        "Conto": context.user_data["column4"],
        "Type": tipo,
    }

    # Assicurati che il file esista e abbia la struttura corretta
    if os.path.exists(CSV_FILE_PATH):
        df = pd.read_csv(CSV_FILE_PATH)
    else:
        df = pd.DataFrame(
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

    df = df.append(new_row, ignore_index=True)

    # riordina il dataframe per Y, M, D e rinomina gli indici da 0 a n
    df = df.sort_values(by=["Y", "M", "D", "Category", "Amount"], ascending=False)
    df["ID"] = range(0, len(df))

    # rinomina gli indici da 0 a n
    df = df.reset_index(drop=True)

    df.to_csv(CSV_FILE_PATH, index=False)

    # riepilogo spesa
    await query_conto.edit_message_text(
        text=f"Spesa aggiunta: {context.user_data['column1']}€, {context.user_data['column2']}, {context.user_data['column3']}, {context.user_data['column4']}"
    )
    return ConversationHandler.END


async def dati(update: Update, context: CallbackContext) -> int:
    pass


async def cancel(update: Update, context: CallbackContext) -> int:
    if not is_authorized(update.effective_chat.id):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return ConversationHandler.END

    await update.message.reply_text("Operazione annullata.")
    return ConversationHandler.END


# ---------------------------- Main ----------------------------


def main():
    application = Application.builder().token(TOKEN).build()

    # Gestore di conversazione
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [CallbackQueryHandler(button)],
            COLUMN1: [MessageHandler(filters.TEXT & ~filters.COMMAND, column1)],
            COLUMN2: [CallbackQueryHandler(column2)],
            COLUMN3: [MessageHandler(filters.TEXT & ~filters.COMMAND, column3)],
            COLUMN4: [CallbackQueryHandler(column4)],
            DATI: [MessageHandler(filters.TEXT & ~filters.COMMAND, dati)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()