import csv

CTDAD_TRABAJADORES = 54*2      	# n
CTDAD_TIPOS_TRABAJADORES = 2 	# m
CTDAD_TIPOS_CLAMSHELLS = 2   	# k
CTDAD_MERCADOS = 4           	# i
CTDAD_DIAS = 28              	# d
CTDAD_TURNOS = 2             	# t
 
#QA, QC, QF
QA = []
QC = []
CF = []
with open('DATOS/otros_parametros_old.csv', 'r', encoding='utf-8') as otros:
	otros = [i for i in csv.reader(otros)]
	QA.append(int(otros[1][0]))
	QC.append(int(otros[1][1]))
	CF.append(int(otros[1][2]))
with open('DATOS/otros_parametros.csv', 'r', encoding='utf-8') as otros:
	otros = [i for i in csv.reader(otros)]
	QA.append(int(otros[1][0]))
	QC.append(int(otros[1][1]))
	CF.append(int(otros[1][2]))

#CCD
with open('DATOS/cc_d.csv', 'r',encoding='utf-8-sig') as ccd:
	CCD = [i[0].lstrip() for i in csv.reader(ccd)]
	CCD = [int(i) for i in CCD]

#CCK
CCK_LIST = []
with open('DATOS/ck_k_old.csv', 'r',encoding='utf-8-sig') as cck:
	CCK = [i[0].lstrip() for i in csv.reader(cck)]
	CCK = [int(i) for i in CCK]
	CCK_LIST.append(CCK)
with open('DATOS/ck_k.csv', 'r',encoding='utf-8-sig') as cck:
	CCK = [i[0].lstrip() for i in csv.reader(cck)]
	CCK = [int(i) for i in CCK]
	CCK_LIST.append(CCK)

#CT
with open('DATOS/ct_m.csv', 'r',encoding='utf-8-sig') as ctm:
	CT = [i[0].lstrip() for i in csv.reader(ctm)]
	CT = [int(i) for i in CT]

#FM
with open('DATOS/f_m.csv', 'r',encoding='utf-8-sig') as fm:
	FM = [i[0].lstrip() for i in csv.reader(fm)]
	FM = [float(i) for i in FM]

#QT
QT_LIST = []
with open('DATOS/qt_m_old.csv', 'r',encoding='utf-8-sig') as qtm:
	QT = [i for i in csv.reader(qtm)]
	QT = [int(i) for i in QT[0]]
	QT_LIST.append(QT)
with open('DATOS/qt_m.csv', 'r',encoding='utf-8-sig') as qtm:
	QT = [i for i in csv.reader(qtm)]
	QT = [int(i) for i in QT[0]]
	QT_LIST.append(QT)

#QD
with open('DATOS/qd_NEW.csv', 'r',encoding='utf-8-sig') as qd:
	temp = [i for i in csv.reader(qd)]
	QD = [[] for _ in range(CTDAD_MERCADOS)]
	for i in range(len(temp)):
		for d in range(len(temp[0])):
			QD[d].append(float(temp[i][d]))

#PC
PC_LIST = []

PC=[[] for _ in range(CTDAD_TIPOS_CLAMSHELLS)]
for i in range(CTDAD_TIPOS_CLAMSHELLS):
	with open('DATOS/pc'+str(i+1)+'_NEW_old.csv', 'r',encoding='utf-8-sig') as pc:
		temp = [i for i in csv.reader(pc)]
		PC[i] = [[] for _ in range(CTDAD_MERCADOS)]
		for x in range(len(temp)):
			for d in range(len(temp[0])):
				PC[i][d].append(float(temp[x][d]))
PC_LIST.append(PC)
PC=[[] for _ in range(CTDAD_TIPOS_CLAMSHELLS)]
for i in range(CTDAD_TIPOS_CLAMSHELLS):
	with open('DATOS/pc'+str(i+1)+'_NEW.csv', 'r',encoding='utf-8-sig') as pc:
		temp = [i for i in csv.reader(pc)]
		PC[i] = [[] for _ in range(CTDAD_MERCADOS)]
		for x in range(len(temp)):
			for d in range(len(temp[0])):
				PC[i][d].append(float(temp[x][d]))
PC_LIST.append(PC)