import csv
import math


def polAn(xS, yS, k):
    global yA, xA, RI_betaN
    print('\n')
    print('KEY ' + str(k))
    print('xS ' + str(xS))
    print('yS ' + str(yS))
    k = k[0:3]
    if k == '1.2':
        xA, yA = mydict['1.1.0005']
        RI_betaN = 0
    elif k == '1.3':
        xA, yA = mydict['1.1.0006']
        RI_betaN = 1
    elif k == '2.2' or '3.2':
        xA, yA = mydict['2.1.0003']
        RI_betaN = 0
    elif k == '2.3' or '3.3':
        xA, yA = mydict['2.1.0004']
        RI_betaN = 1
    elif k == '4.2':
        xA, yA = mydict['4.1.0002']
        RI_betaN = 0
    elif k == '4.3':
        xA, yA = mydict['4.1.0003']
        RI_betaN = 1

    xA, yA = float(xA), float(yA)
    print('xA ' + str(xA))
    print('yA ' + str(yA))
    sN = 0.025
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


with open('Wurf-mm_delim-tab.pkt', newline='') as csvfile:
    coor = csv.reader(csvfile, delimiter='\t')
    mydict = {rows[0]: (rows[2], rows[3]) for rows in coor}

print(mydict['1.2.0065'])

for key in mydict:
    if key[2] == '2' or key[2] == '3':
        x, y = mydict[key]
        x = float(x)
        y = float(y)
        xEx, yEx = polAn(x, y, key)
        mydict[key] = [xEx, yEx]

fieldnames = ['PNR', 'Code', 'X', 'Y']
with open('Wurf-mm_exzentrum.pkt', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    for key in mydict:
        a, b = mydict[key]
        a, b = float(a), float(b)
        obj = [key, '1000', a, b]
        writer.writerow(obj)
