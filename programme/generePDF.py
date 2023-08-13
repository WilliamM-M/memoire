from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Création du document PDF
doc = SimpleDocTemplate("exemple.pdf", pagesize=letter)

# Liste des données pour le tableau
data = [['Numero', 'Paramètres', 'Valeur Normale', 'Valeur mesurée', 'Observation'],
        ['1', 'Fréquence cardiaque', 'Ligne 2','Ligne 2', 'Ligne 2'],
        ['2', 'Ibi', 'Ligne 3','Ligne 3', 'Ligne 5'],
        ['3', 'Sdnn', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['4', 'Sdsd', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['5', 'Rmssd', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['6', 'Pmm20', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['7', 'Pmm50', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['8', 'Hr_mad', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['9', 'Sd1', 'Ligne 4','Ligne 4', 'Ligne 4'],
        ['10', 'Sd2', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['11', 'S', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['12', 'Sd1/Sd2', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['13', 'Durée QRS', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['14', 'PR', 'Ligne 5','Ligne 5', 'Ligne 5'],
        ['15', 'QR', 'Ligne 5','Ligne 5', 'Ligne 5'],]

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
title2_text = "Malade : "+ "William MUTOMBO"
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