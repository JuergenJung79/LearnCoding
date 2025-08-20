import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

CSV_FILE = 'daten.csv'

# CSV initialisieren
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Datum', 'Gewicht', 'Kacka'])

# Daten speichern
def daten_speichern():
    datum = entry_datum.get()
    gewicht = entry_gewicht.get()
    kacka = var_kacka.get()

    try:
        datetime.strptime(datum, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Fehler", "Ungültiges Datum. Format: YYYY-MM-DD")
        return

    try:
        gewicht = float(gewicht)
    except ValueError:
        messagebox.showerror("Fehler", "Ungültiges Gewicht.")
        return

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datum, gewicht, 'ja' if kacka else 'nein'])

    messagebox.showinfo("Erfolg", "Daten gespeichert.")
    entry_datum.delete(0, tk.END)
    entry_gewicht.delete(0, tk.END)
    var_kacka.set(False)

# Daten visualisieren
def daten_visualisieren():
    daten = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                datum = datetime.strptime(row['Datum'], "%Y-%m-%d")
                gewicht = float(row['Gewicht'])
                kacka = 1 if row['Kacka'].lower() == 'ja' else 0
                daten.append((datum, gewicht, kacka))
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Noch keine Daten gespeichert.")
        return

    if not daten:
        messagebox.showinfo("Info", "Keine Daten zum Anzeigen.")
        return

    daten.sort(key=lambda x: x[0])
    daten_liste, gewicht_liste, kacka_liste = zip(*daten)

    plt.figure(figsize=(10, 5))
    plt.plot(daten_liste, gewicht_liste, marker='o', label='Gewicht (kg)')

    kacka_daten = [d for i, d in enumerate(daten_liste) if kacka_liste[i] == 1]
    kacka_gewicht = [gewicht_liste[i] for i, d in enumerate(daten_liste) if kacka_liste[i] == 1]
    plt.scatter(kacka_daten, kacka_gewicht, color='red', label='Kacka = ja')

    plt.xlabel("Datum")
    plt.ylabel("Gewicht (kg)")
    plt.title("Gewichtsentwicklung mit Kacka-Marker")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# GUI Aufbau
init_csv()
root = tk.Tk()
root.title("Gewichts- und Kacka-Tracker")

# Widgets
frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="Datum (YYYY-MM-DD):").grid(row=0, column=0, sticky='w')
entry_datum = ttk.Entry(frame, width=20)
entry_datum.grid(row=0, column=1)

ttk.Label(frame, text="Gewicht (kg):").grid(row=1, column=0, sticky='w')
entry_gewicht = ttk.Entry(frame, width=20)
entry_gewicht.grid(row=1, column=1)

var_kacka = tk.BooleanVar()
check_kacka = ttk.Checkbutton(frame, text="Kacka gemacht?", variable=var_kacka)
check_kacka.grid(row=2, columnspan=2, pady=(10, 10))

ttk.Button(frame, text="Daten speichern", command=daten_speichern).grid(row=3, column=0, pady=5)
ttk.Button(frame, text="Visualisieren", command=daten_visualisieren).grid(row=3, column=1, pady=5)

ttk.Button(frame, text="Beenden", command=root.quit).grid(row=4, columnspan=2, pady=(10, 0))

root.mainloop()
