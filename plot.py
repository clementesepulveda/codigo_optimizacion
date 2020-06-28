import matplotlib.pyplot as plt
import numpy as np


def despachado(model, iter):
	"""
	Sacado y modificado de 
	https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_features.html
	"""

	D = [0, 0]
	for v in model.getVars():
		if v.varName[:3]=='D_1':
			D[0] += v.x
		if v.varName[:3]=='D_2':
			D[1] += v.x

	labels = 'Despacho Tipo 1', 'Despacho Tipo 2'
	sizes = [D[0], D[1]]
	explode = (0, 0.1)  # only "explode" the 2nd slice

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	plt.title(f'Porcentajes de Despacho de Clamshell Tipo 1 y 2 {iter})')
	print('Despacho',D)
	plt.show()

def trabajadores(model, iter):
	"""
	Sacado y modificado de
	https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py
	"""
	workers_t1 = [0]*28
	workers_t2 = [0]*28

	for v in model.getVars():
		if v.varName[0]=='T':
			t = v.varName.split(',')
			if t[1] == '1':
				workers_t1[int(t[-1])-1]+=v.x
			else:
				workers_t2[int(t[-1])-1]+=v.x

	N = 28
	menMeans = workers_t1
	womenMeans = workers_t2
	ind = np.arange(N)    # the x locations for the groups
	width = 0.5       # the width of the bars: can also be len(x) sequence

	p1 = plt.bar(ind, menMeans, width)
	p2 = plt.bar(ind, womenMeans, width,
	             bottom=menMeans)

	plt.ylabel('Cantidad Trabajadores')
	plt.xlabel('Dia')
	plt.title(f'Cantidad de Trabajadores por Dia ({iter})')
	plt.xticks(ind, [str(i+1) for i in range(28)])
	plt.legend((p1[0], p2[0]), ('Turno 1', 'Turno 2'))

	print("trabajadores", sum(workers_t1)/len(workers_t1),sum(workers_t2)/len(workers_t2))
	plt.show()

def donde_clam(model, iter):
	"""
	Sacado y modificado de
	https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py
	"""
	workers_t1 = [0,0,0,0]

	for v in model.getVars():
		if v.varName[0]=='D':
			workers_t1[int(v.varName[3:4])-1]+=v.x

	N = 4
	menMeans = workers_t1
	ind = np.arange(N)    # the x locations for the groups
	width = 0.80       # the width of the bars: can also be len(x) sequence

	p1 = plt.bar(ind, menMeans, width)

	plt.ylabel('Cantidad de Clamshells')
	plt.xlabel('Mercado')
	plt.title(f'Cantidad de Clamshells por Mercado({iter})')
	plt.xticks(ind, ('NorteAmerica','Asia',"Europa",'IQF'))

	print("Mercados ",workers_t1)
	plt.show()

def almacenar(model, iter):
	"""
	Sacado y modificado de
	https://matplotlib.org/gallery/lines_bars_and_markers/categorical_variables.html#sphx-glr-gallery-lines-bars-and-markers-categorical-variables-py
	"""
	workers_t1 = [1]*28

	for v in model.getVars():
		if v.varName[0]=='A':
			t = v.varName[4:]
			workers_t1[int(t)-1]+=v.x


	cat = workers_t1
	activity = [i+1 for i in range(28)]

	fig, ax = plt.subplots()
	ax.plot(activity, cat, label="cat")
	plt.ylabel('Cantidad de Clamshells')
	plt.xlabel('Dia')
	plt.title(f'Cantidad de Clamshells Almacenados cada Dia ({iter})')
	plt.xticks(np.arange(28), activity)

	print("Almacenar",sum(cat)/len(cat))
	plt.show()

def producidos(model, iter):
	"""
	Sacado y modificado de
	https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py
	"""
	m1 = [0]*28
	m2 = [0]*28
	m3 = [0]*28
	m4 = [0]*28

	for v in model.getVars():
		if v.varName[0]=='C':
			t = v.varName[3:]
			if t[0] == '1':
				m1[int(t[2:])-1]+=v.x
			if t[0]== "2":
				m2[int(t[2:])-1]+=v.x
			if t[0]== "3":
				m3[int(t[2:])-1]+=v.x
			if t[0]== "4":
				m4[int(t[2:])-1]+=v.x

	N = 28
	ind = np.arange(N)    # the x locations for the groups
	width = 0.5       # the width of the bars: can also be len(x) sequence

	p1 = plt.bar(ind, m1, width)
	p2 = plt.bar(ind, m2, width,bottom=m1)
	p3 = plt.bar(ind, m3, width,bottom=[m1[i]+m2[i] for i in range(28)])
	p4 = plt.bar(ind, m4, width,bottom=[m1[i]+m2[i]+m3[i] for i in range(28)])

	plt.ylabel(f'Cantidad Clamshells ({iter})')
	plt.xlabel('Dia')
	plt.title('Cantidad de Clamshells Producidos para Cada Mercado')
	plt.xticks(ind, [str(i+1) for i in range(28)])
	plt.legend((p1[0], p2[0], p3[0], p4[0]), ('NorteAmerica',
											  'Asia',
											  'Europa',
											  'IQF'))
	print("Producidos", (sum(m1)+sum(m2)+sum(m3)+sum(m4))/28)
	plt.show()

def plot(m, iter):
	despachado(m, iter)
	trabajadores(m, iter)
	donde_clam(m, iter)
	almacenar(m, iter)