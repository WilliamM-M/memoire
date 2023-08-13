import numpy as np
import heartpy as hp
from heartpy.datautils import rolling_mean
from biosppy.signals import ecg

from reportlab.pdfgen import canvas
import multiprocessing as mp
####################################
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
####################################

def execute():
     process = mp.Process(target=process1)
     process.start()
        # Attendre la fin de l'exécution du processus avant de quitter l'application
     print('laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
     #process.join()
     print("Processus de génération de graphiques terminé")

def process1():
    # Charger les données ECG à partir du fichier CSV
    data = hp.get_data('donnees.csv', column_name='MLII_filtered')
    out = ecg.ecg(signal=data, sampling_rate=360)
    
    r_peaks = ecg.christov_segmenter(signal=data, sampling_rate=360)
    print(r_peaks)
    #############################
    print("templates :  ",out["templates"])
    ################################
    #Ppositions = ecg.getPPositions(out)
    #print("positions P : ", Ppositions)

    Qpositions = ecg.getQPositions(out)
    print("positions Q : ", Qpositions)
    Qpic = Qpositions[0][2]
    print("Qpic", Qpic)
    print("Qpic temps", Qpic*(1/360))
    Rpic = 662*(1/360)
    print("Qpic temps", 662*(1/360))

    QR = (Rpic-Qpic*(1/360))*1000
    print("QR temps", QR)



    Spositions = ecg.getSPositions(out)
    print("positions S : ", Spositions)

    #Tpositions = ecg.getTPositions(out)
    #print("positions T : ", Tpositions)
    ################################

    # Afficher les indices des pics R
    rpeaks_indices = out['rpeaks']
    print("Indices des pics R :", rpeaks_indices)



    # Fréquence d'échantillonnage
    frequence_echantillonnage = 360

    # Calculer les mesures à l'aide de heartpy
    working_data, measures = hp.process(data, sample_rate=frequence_echantillonnage)
    print(" Mesures  ",measures)

    # Accéder à chaque paramètre
    bpm = measures['bpm']
    ibi = measures['ibi']
    sdnn = measures['sdnn']
    sdsd = measures['sdsd']
    rmssd = measures['rmssd']
    pnn20 = measures['pnn20']
    pnn50 = measures['pnn50']
    hr_mad = measures['hr_mad']
    sd1 = measures['sd1']
    sd2 = measures['sd2']
    s = measures['s']
    sd1_sd2 = measures['sd1/sd2']
    breathing_rate = measures['breathingrate']
   
    #########################hp.plotter(working_data, measures)

    ##### Calcul de la variabilité de la fréquence cardiaque #####

    # Calculer les intervalles R-R (RR intervals) et la fréquence cardiaque
    rr_intervals = hp.analysis.calc_rr(rpeaks_indices, 360)  # Intervalles R-R en secondes
    # Calculer la fréquence cardiaque moyenne à partir des intervalles R-R
    print(rr_intervals)
    # Calculer la différence moyenne des intervalles R-R
    mean_rr_diff = np.mean(rpeaks_indices)
    heart_rate = 60 / mean_rr_diff

    # Afficher les intervalles R-R et la fréquence cardiaque
    print("Intervalles R-R (s) :", rr_intervals)
    print("Fréquence cardiaque (bpm) :", heart_rate)


    
   ########################################################################################################
    QRS = 102.777
    QR_ = 50

   # Création du document PDF
    doc = SimpleDocTemplate("exemple.pdf", pagesize=letter)

    def verifier_bpm(valeur_bpm):
      if valeur_bpm < 60:
          return "Bradycardie"
      elif valeur_bpm > 100:
          return "Tachycardie"
      else:
          return "Bon"

   # Liste des données pour le tableau
    bpm_obs = verifier_bpm(bpm)
    data = [['Numero', 'Paramètres', 'Valeur Normale', 'Valeur mesurée', 'Observation'],
         ['1', 'Fréquence cardiaque', '60 à 100 bpm',bpm, bpm_obs],
         ['2', 'Durée QRS', '80–100 ms [80–120 ms]',QRS, 'Bon'],
         ['3', 'PR', '120–200 ms','-', '-'],
         ['4', 'QR', '',QR_, ''],
         ['5', 'Durée P','< 120 ms','', ''],
         ['6', 'Ibi', '',ibi, ''],
         ['7', 'Sdnn', '',sdnn, ''],
         ['8', 'Sdsd', '',sdsd, ''],
         ['9', 'Rmssd', '',rmssd, ''],
         ['10', 'Pmm20', '',pnn20, ''],
         ['11', 'Pmm50', '',pnn50, ''],
         ['12', 'Hr_mad', '',hr_mad, ''],
         ['13', 'Sd1', '',sd1, ''],
         ['14', 'Sd2', '',sd2, ''],
         ['15', 'S', '',s, ''],
         ['16', 'Sd1/Sd2', '',sd1_sd2, ''],
         ]

   # Création du contenu
    content = []

   # Styles de paragraphe prédéfinis
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    description_style = styles['BodyText']

   # Ajout du premier titre
    title0_text = "UNIKIN/Polytechnique_Mémoire. William MUTOMBO"
    title0_paragraph = Paragraph(title0_text, title_style)
    content.append(title0_paragraph)

    title1_text = "RESULTATS ANALYSE ECG"
    title1_paragraph = Paragraph(title1_text, title_style)
    content.append(title1_paragraph)

   # Ajout du second titre
    title2_text = "Patient : "+ "Sujet Test"
    title2_paragraph = Paragraph(title2_text, title_style)
    content.append(title2_paragraph)

   # Ajout de la première notice
    notice_text = "Notice : ceci est un enregistrement."
    notice_paragraph = Paragraph(notice_text, description_style)
    content.append(notice_paragraph)

   # Ajout du tableau
    table = Table(data, colWidths=[120]*5, rowHeights=30)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('FONTSIZE', (0, 0), (-1, 0), 12),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                              ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                              ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                              ('FONTSIZE', (0, 1), (-1, -1), 10),
                              ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    content.append(table)

   # Ajout de la seconde notice
    notice2_text = "Ces résultats seront confirmés par un médecin spécialisé."
    notice2_paragraph = Paragraph(notice2_text, description_style)
    content.append(notice2_paragraph)

   # Génération du document PDF
    doc.build(content)

   ###################################################################################

    