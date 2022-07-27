import csv
import math

rho = 180/math.pi
offset = 0.025


def exzentrumSektor(xS, yS, k):     # Punkte der Sektorlinien werden um dem Offset nach außen versetzt
    global yA, xA, RI_betaN
    k = k[0:3]
    if k == '1.2':      # Bestimmung Anschlusspunkt des folgenden polaren Anhängens je nach Disziplin und Sektorlinie
        xA, yA = koordinaten_import['1.1.0005']
        RI_betaN = 0
    elif k == '1.3':
        xA, yA = koordinaten_import['1.1.0006']
        RI_betaN = 1
    elif k == '2.2' or '3.2':
        xA, yA = koordinaten_import['2.1.0003']
        RI_betaN = 0
    elif k == '2.3' or '3.3':
        xA, yA = koordinaten_import['2.1.0004']
        RI_betaN = 1
    elif k == '4.2':
        xA, yA = koordinaten_import['4.1.0002']
        RI_betaN = 0
    elif k == '4.3':
        xA, yA = koordinaten_import['4.1.0003']
        RI_betaN = 1

    xA, yA = float(xA), float(yA)
    tSA = math.atan2((yA - yS), (xA - xS))      # Richtungswinkel Standpunkt (Pkt Sektorlinie) zu Anschlusspunkt
    if RI_betaN == 1:       # Rechte Sektorlinie --> Punkt nach rechts verschieben
        betaN = math.radians(270)
    else:       # Linke Sektorlinie --> Punkt nach rechts verschieben
        betaN = math.radians(90)
    tSN = tSA + betaN       # Richtungswinkel des Neupunktes (exzentrischer Punkt)
    yN = yS + offset * math.sin(tSN)        # Polares Anhängen y-Koordiante
    xN = xS + offset * math.cos(tSN)        # Polares Anhängen x-Koordiante

    xN, yN = round(xN, 3), round(yN, 3)     # Runden auf 3 NKS

    return xN, yN


def weitenlinie(d, w):      # Berechnung der Weitenlinien
    global string_lfdnr

    # Definition des Öffnungswinkels (abhängig von Disziplin), Radius sowie Koordinaten von Mittelpunkt des
    # Kreises (Standpunkt S) und eines Punktes in der Sektorachse (Anschlusspunkt A) für polares Anhängen
    if d == 1:      # Speer
        alpha = 28.96
        r = 8.0
        xS, yS = koordinaten_import['1.1.0001']
        xS, yS = float(xS), float(yS)
        xA, yA = koordinaten_import['1.1.0007']
        xA, yA = float(xA), float(yA)
    else:   # Diskus, Hammer, Kugel
        alpha = 34.92
        if d == 2:  # Diskus
            r = 1.25
            xS, yS = koordinaten_import['2.1.0001']
            xS, yS = float(xS), float(yS)
            xA, yA = koordinaten_import['2.1.0002']
            xA, yA = float(xA), float(yA)
        elif d == 3:    # Hammer
            r = 0.5 * 2.135
            xS, yS = koordinaten_import['2.1.0001']
            xS, yS = float(xS), float(yS)
            xA, yA = koordinaten_import['2.1.0002']
            xA, yA = float(xA), float(yA)
        else:       # Kugel
            r = 0.5 * 2.135
            xS, yS = koordinaten_import['4.1.0001']
            xS, yS = float(xS), float(yS)
            xA, yA = koordinaten_import['4.1.0006']
            xA, yA = float(xA), float(yA)

    if d == 4:      # Punktabstand auf dem Bogen der Weitenlinie wird durch User bestimmt
        bogenlaenge_weitenlinie = user_bogenlaenge_kugel
    else:
        bogenlaenge_weitenlinie = user_bogenlaenge_langwurf

    halbeBogenlaenge = 0.5 * ((alpha * (w + r))/rho)        # Berechnung der halben Bogenlänge der Weitenlinie
    anzahlPunktHalbeBogenlaenge = math.floor(halbeBogenlaenge / bogenlaenge_weitenlinie)    # Pkte auf WL // Bogenlänge
    gamma = bogenlaenge_weitenlinie / (w + r)       # Winkel zw. Sektorachse und durch Bogenlänge definerten Pkt auf WL

    tSA = math.atan2((yA - yS), (xA - xS))      # Richtungswinkel Standpunkt - Anschlusspunkt

    nr = -1 * anzahlPunktHalbeBogenlaenge       # Nr. des Pkts auf WL um links und rechts der Achse berechnen zu können
    lfdnr = 1
    anzahlPunkteWeitenlinie = 2 * anzahlPunktHalbeBogenlaenge + 1       # Anzahl Punkte auf WL inkl. Punkt auf Achse

    for m in range(anzahlPunkteWeitenlinie + 2):        # Berechnung der Koordinaten der WL-Punkte
        if lfdnr == 1:      # erster Punkt der WL soll auf linker Sektorlinie liegen
            betaN = -math.radians(0.5 * alpha)
            nr -= 1
        elif lfdnr == (anzahlPunkteWeitenlinie + 2):        # letzter Punkt der WL soll auf rechter Sektorlinie liegen
            betaN = math.radians(0.5 * alpha)
        else:       # Winkel in Abhängigkeit der Sektorachse (Nullrichtung), wenn negativ dann links der Achse
            betaN = nr * gamma

        tSN = tSA - betaN       # Richtungswinkel für Neupunkt (Punkt auf WL)
        yN = yS + (w + r + offset) * math.sin(tSN)
        xN = xS + (w + r + offset) * math.cos(tSN)

        # if: Punkt der Weitenlinie der auf Sektorlinie liegt mit Offset Sektorlinie berechnen
        if lfdnr == 1:
            xN, yN = exzPktWeitenlinieXSektor(xN, yN, d, 0)
        elif lfdnr == anzahlPunkteWeitenlinie + 2:
            xN, yN = exzPktWeitenlinieXSektor(xN, yN, d, 1)

        xN, yN = round(xN, 3), round(yN, 3)

        if lfdnr < 10:      # bei einstelliger Lfdnr. wird '0' ergänzt, um immer eine gleiche Stellenanzahl zu haben
            string_lfdnr = '0' + str(lfdnr)
        else:
            string_lfdnr = str(lfdnr)

        string_pnr = str(d) + '.4.' + str(int(weite*100)) + string_lfdnr        # Zusammenbau der Punktnummer
        koordinaten_export[string_pnr] = xN, yN     # Abspeichern der Punktnummer und der Koordinaten

        nr += 1
        lfdnr += 1


def exzPktWeitenlinieXSektor(xS, yS, d, p):     # Erneute Verschiebung der Punkte auf WL die auch auf Sektorlinie liegen

    # Definition der Anschlusspunkte je nach Disziplin und Sektorlinie
    if d == 1 and p == 0:
        xA, yA = koordinaten_import['1.1.0005']
    elif d == 1 and p == 1:
        xA, yA = koordinaten_import['1.1.0006']
    elif d == 2 or d == 3 and p == 0:
        xA, yA = koordinaten_import['2.1.0003']
    elif d == 2 or d == 3 and p == 1:
        xA, yA = koordinaten_import['2.1.0004']
    elif d == 4 and p == 0:
        xA, yA = koordinaten_import['4.1.0002']
    else:   # d == 4 and p == 1:
        xA, yA = koordinaten_import['4.1.0003']

    xA, yA = float(xA), float(yA)
    tSA = math.atan2((yA - yS), (xA - xS))

    if p == 0:
        betaN = math.radians(270)
    else:
        betaN = math.radians(90)

    tSN = tSA - betaN
    yN = yS + offset * math.sin(tSN)
    xN = xS + offset * math.cos(tSN)

    return xN, yN


# Import der Soll-Koordinaten (Kreis, Sektorlinien, Sektorachse)
with open('Wurf-mm_delim-tab_ohneWeiten.pkt', newline='') as csvfile:
    coor = csv.reader(csvfile, delimiter='\t')
    koordinaten_import = {rows[0]: (rows[2], rows[3]) for rows in coor}

koordinaten_export = koordinaten_import

i = 0
while i == 0:
    offset = input('Offset in [cm] eingeben: ')
    try:
        offset = float(offset)
        offset = offset / 100
        print('Offset ' + str(offset))
        i = 1
    except ValueError:
        print('Gleitkomma benötigt!')

user_bogenlaenge_langwurf = input('Bogenlänge der Weitenlinien für Langwürfe eingeben (Gleitkomma, z.B. "2.0" [m]): ')
try:
    user_bogenlaenge_langwurf = float(user_bogenlaenge_langwurf)
except ValueError:
    print('Gleitkomma du Idiot! Nichts anderes')

user_bogenlaenge_kugel = input('Bogenlänge der Weitenlinien für Kugel eingeben (Gleitkomma, z.B. "1.0" [m]): ')
try:
    user_bogenlaenge_kugel = float(user_bogenlaenge_kugel)
except ValueError:
    print('Gleitkomma du Idiot! Nichts anderes')


for key in koordinaten_export:      # Berechnung des exzentrischen Punktes
    if key[2] == '2' or key[2] == '3':      # dritte [2] Stelle definiert in der Importdatei Punkte der Sektorlinien
        x, y = koordinaten_export[key]
        x, y = float(x), float(y)
        xEx, yEx = exzentrumSektor(x, y, key)
        koordinaten_export[key] = [xEx, yEx]

i = 0
while i == 0:
    j = 0
    disziplin = int(input('Disziplin wählen: (1) Speer  (2) Diskus  (3) Hammer  (4) Kugel  (5) BEENDEN '))

    if disziplin == 1:
        string_disziplin = 'Speer'
    elif disziplin == 2:
        string_disziplin = 'Diskus'
    elif disziplin == 3:
        string_disziplin = 'Hammer'
    else:
        string_disziplin = 'Kugel'

    if disziplin == 1 or disziplin == 2 or disziplin == 3 or disziplin == 4:
        while j == 0:
            weite = input(f'Weitenlinie für {string_disziplin} eingeben (0 für Beenden): ')
            try:
                weite = float(weite)
                if weite == 0:
                    j = 1
                else:
                    weitenlinie(disziplin, weite)
            except ValueError:
                print('Float eingeben!')
    elif disziplin == 5:
        i = 1
    else:
        print('Int eingeben!')

# Export der neuen Koordinaten
fieldnames = ['PNR', 'Code', 'X', 'Y']
with open('Wurf-mm_exzentrum.pkt', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    for key in koordinaten_export:
        a, b = koordinaten_export[key]
        a, b = float(a), float(b)
        obj = [key, '1000', a, b]
        writer.writerow(obj)
