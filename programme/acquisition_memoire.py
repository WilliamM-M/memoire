from typing import Self
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import csv
import serial
import os
import multiprocessing as mp
from sklearn.semi_supervised import SelfTrainingClassifier

import preprocess
import process

#----Global variabls----
data = np.array([])
cond = False
save = False

#------Plot data-------
def plot_data():
    global cond, data
    
    if cond:
        a = s.readline()
        a = a.decode().strip()  # Convertir les données en chaîne de caractères et supprimer les espaces en début et fin
        print(a)
        if a:  # Vérifier si la chaîne ne contient que des chiffres
            value = float(a)
            
            if len(data) < 100:
                data = np.append(data, value)
            else:
                data[0:99] = data[1:100]
                data[99] = value
                
            lines.set_xdata(np.arange(0, len(data)))
            lines.set_ydata(data)
            
            canvas.draw()
            
            save_data(value)
            
    root.after(1, plot_data)
    
def plot_start():
    global cond
    cond = True
    s.reset_input_buffer()
    
def plot_stop():
    global cond
    cond = False
    
def save_data(value):
    if save:
        with open(get_entry_text(), 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([value])
        #print("Data saved to data.csv")
    #print("No record")
def saveAction():
    global save
    save = True
    print(save)
def get_entry_text():
    text = entry.get().strip()
    filename = text + ".csv"
    return filename
def lance2():

    processT = mp.Process(target=process.process1)
    processT.start()
        # Attendre la fin de l'exécution du processus avant de quitter l'application
    print('laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    processT.join()
    print("Processus de génération de graphiques terminé")

def analyse():
    # Fonction pour ouvrir la première interface
    
    def select_directory():
    # Fonction pour sélectionner le répertoire contenant les fichiers CSV
        repertoire = filedialog.askdirectory()
        if repertoire:
            # Obtenir la liste des fichiers CSV dans le répertoire sélectionné
            fichiers_csv = [fichier for fichier in os.listdir(repertoire) if fichier.endswith(".csv")]
            combobox_csv["values"] = fichiers_csv
        else:
            combobox_csv["values"] = []
    def get_combo_value():
        value = combobox_csv.get()  # Récupération de la valeur sélectionnée dans le Combobox
        print("Valeur sélectionnée :", value)  # Affichage de la valeur sélectionnée
    s.close()
    interface1 = tk.Toplevel()
    interface1.title("Interface 1")
    interface1.configure(background = 'light blue')
    interface1.geometry("800x600")

     # Label "Nom patient"
    label_nom = ttk.Label(interface1, text=data)
    label_nom.pack(pady=10, padx=10, anchor="w")
    # Zone de saisie de texte pour le nom du patient
    entry_nom = ttk.Entry(interface1)
    entry_nom.pack(pady=10, padx=10, anchor="w")
    # Zone graphique pour afficher les données ECG en temps réel
    graphique = ttk.Label(interface1, text="Zone graphique ECG")
    graphique.pack(pady=10, padx=10)
    # Bouton "Lancer l'enregistrement"
    btn = ttk.Button(interface1, text="Analyse Data", style="TButton", command=get_combo_value)
    btn.place(x=3, y=560)

    btn1 = ttk.Button(interface1, text="Analyse Data Test", command=lance2)
    btn1.place(x=100, y=560)

    # Create Combobox
    combobox_csv = ttk.Combobox(interface1, values=[], state="readonly")
    combobox_csv.place(x=150, y=560, width=150)
    combobox_csv.set("Choisir DATA")

    # Create directory selection button
    select_directory_button = ttk.Button(interface1, text="Sélectionner Répertoire", command=select_directory)
    select_directory_button.place(x=10, y=560)

    #preprocess.preprocess() #######################################################################
    

#_____Main GUI Code____
root = tk.Tk()
root.title('Assist_ECG_Analysis/ UNIKIN-POLY. William 2023')
root.configure(background = 'light blue')
root.geometry("800x600") # set the window size

#---------Create Plot object on GUI---------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

#ax = plt.axes(xlim=(0,100), ylim=(0, 120)); #displaying only 100 samples
ax.set_title('ECG Serial Data Acquisition');
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_xlim(0,100)
ax.set_ylim(-10,10)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root) # A tk.DrawingArea
canvas.get_tk_widget().place(x = 10,y = 140, width=780,height=400)
canvas.draw()

#-------Create button----------

label_nom = ttk.Label(root, text="Assistant d'Analyse ECG/UNIKIN")
label_nom.place(x=300, y=10)

label_nom = ttk.Label(root, text="Nom : ")
label_nom.place(x=10, y=100)
entry = ttk.Entry(root)
entry.place(x=60, y=100, width=150)

root.update();
start = ttk.Button(root, text="Start", style="TButton", command=plot_start)
start.place(x=400, y=100)

root.update();
stop = ttk.Button(root, text="Cancel", style="TButton", command=plot_stop)
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=100)

save = ttk.Button(root, text="Save Data", style="TButton", command=saveAction)
save.place(x=start.winfo_x() + start.winfo_reqwidth() + 120, y=100)

"""
label_nom = ttk.Label(root, text="Choose DATA : ") 
label_nom.place(x=10, y=560)

repertoire_courant = os.getcwd()
fichiers_csv = [fichier for fichier in os.listdir(repertoire_courant) if fichier.endswith(".csv")]
combobox_csv = ttk.Combobox(root, values=fichiers_csv)
combobox_csv.place(x=120, y=560, width=150)
combobox_csv.set("")
"""


comboValue = ttk.Button(root, text="Analyse Data", style="TButton", command=analyse)
comboValue.place(x=350, y=560)


#------Start serial port---------
s = serial.Serial('COM4',9600)
s.reset_input_buffer()

root.after(1, plot_data)
root.mainloop()

