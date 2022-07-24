import csv
import math

rho = 180/math.pi
sN = 0.025
bogenlaenge_weitenlinie = 2.0


def polAn(xS, yS, k):
    global yA, xA, RI_betaN
    print('\n')
    print('KEY ' + str(k))
    print('xS ' + str(xS))
    print('yS ' + str(yS))
    k = k[0:3]
    if k == '1.2':
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
    print('xA ' + str(xA))
    print('yA ' + str(yA))
    tSA = math.atan2((yA - yS), (xA - xS))
    print('tSA ' + str(tSA))
    if RI_betaN == 1:
        betaN = math.radians(270)
    else:
        betaN = math.radians(90)
    print('RI_betaN ' + str(RI_betaN))
    print('betaN ' + str(betaN*180/math.pi))
    tSN = tSA + betaN
    print('tSN ' + str(tSN))
    yN = yS + sN * math.sin(tSN)
    xN = xS + sN * math.cos(tSN)

    xN, yN = round(xN, 3), round(yN, 3)
    print('yN ' + str(yN))
    print('xN ' + str(xN))

    return xN, yN


def weitenlinie(d, w):
    global string_lfdnr
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
        elif d == 3:
            r = 0.5 * 2.135
            xS, yS = koordinaten_import['2.1.0001']
            xS, yS = float(xS), float(yS)
            xA, yA = koordinaten_import['2.1.0002']
            xA, yA = float(xA), float(yA)
        else:       # Hammer, Kugel
            r = 0.5 * 2.135
            xS, yS = koordinaten_import['4.1.0001']
            xS, yS = float(xS), float(yS)
            xA, yA = koordinaten_import['4.1.0006']
            xA, yA = float(xA), float(yA)
    halbeBogenlaenge = 0.5 * ((alpha * (w + r))/rho)
    print('halbeBogenlaenge ' + str(halbeBogenlaenge))
    anzahlPunktHalbeBogenlaenge = math.floor(halbeBogenlaenge / bogenlaenge_weitenlinie)
    print('anzahlPunktHalbeBogenlaenge ' + str(anzahlPunktHalbeBogenlaenge))
    gamma = (bogenlaenge_weitenlinie * rho) / (w + r)
    print('gamma ' + str(gamma))

    tSA = math.atan2((yA - yS), (xA - xS))

    nr = -1 * anzahlPunktHalbeBogenlaenge
    lfdnr = 10
    for m in range(2 * anzahlPunktHalbeBogenlaenge + 1):
        betaN = nr * gamma
        tSN = tSA + betaN
        print('tSN ' + str(tSN))
        yN = yS + sN * math.sin(tSN)
        xN = xS + sN * math.cos(tSN)

        xN, yN = round(xN, 3), round(yN, 3)
        print('yN ' + str(yN))
        print('xN ' + str(xN))

        if lfdnr < 10:
            string_lfdnr = '0' + str(lfdnr)
        string_pnr = str(d) + '.4.' + str(weite*100) + string_lfdnr
        # 1.4.755001
        koordinaten_export[string_pnr] = xN, yN

        nr += 1
        lfdnr += 1

        # TODO Punktcodes erweitern auf cm-Genauigkeit


with open('Wurf-mm_delim-tab_ohneWeiten.pkt', newline='') as csvfile:
    coor = csv.reader(csvfile, delimiter='\t')
    koordinaten_import = {rows[0]: (rows[2], rows[3]) for rows in coor}

koordinaten_export = koordinaten_import

for key in koordinaten_import:      # Berechnung des exzentrischen Punktes
    if key[2] == '2' or key[2] == '3':
        x, y = koordinaten_import[key]
        x = float(x)
        y = float(y)
        xEx, yEx = polAn(x, y, key)
        koordinaten_import[key] = [xEx, yEx]

i, j = 0, 0
while i == 0:
    disziplin = input('Disziplin wählen: (1) Speer  (2) Diskus  (3) Hammer  (4) Kugel')
    if disziplin == 1 or disziplin == 2 or disziplin == 3 or disziplin == 4:
        while j == 0:
            weite = input('Weitenlinie eingeben: ')
            if isinstance(weite, float):
                weitenlinie(disziplin, weite)
                j = 1
            else:
                print('Float eingeben!')
        beenden = input('Berechnung Weitenlinien beenden? (1) Nein  (2) Ja')
        if beenden == 2:
            i = 1
    else:
        print('Int eingeben!')

fieldnames = ['PNR', 'Code', 'X', 'Y']
with open('Wurf-mm_exzentrum.pkt', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    for key in koordinaten_import:
        a, b = koordinaten_import[key]
        a, b = float(a), float(b)
        obj = [key, '1000', a, b]
        writer.writerow(obj)
