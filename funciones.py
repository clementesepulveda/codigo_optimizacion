from gurobipy import GRB, Model, LinExpr
import csv
from data import *

# VARIABLES
def crear_vars_clamshells_con_t(model, nombre):
	# retorna lista de variables con subindices[k][i][t][d]

	variables = []
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		k_list = []
		for i in range(CTDAD_MERCADOS):
			i_list = []
			for t in range(CTDAD_TURNOS):
				t_list = []
				for d in range(CTDAD_DIAS):
					t_list.append(model.addVar(lb=0,vtype=GRB.CONTINUOUS,
									   	       name = nombre+"_"+str(k+1)+str(i+1)
									  				        +str(t+1)+str(d+1)))
				i_list.append(t_list)
			k_list.append(i_list)
		variables.append(k_list)

	return variables

def crear_vars_clamshells(model, nombre):
	# retorna lista de variables con subindices[k][i][d]

	variables = []
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		k_list = []
		for i in range(CTDAD_MERCADOS):
			i_list = []
			for d in range(CTDAD_DIAS):
				i_list.append(model.addVar(lb=0,vtype=GRB.CONTINUOUS,
									   	   name = nombre+"_"+str(k+1)+str(i+1)
									  				        +str(d+1)))
			k_list.append(i_list)
		variables.append(k_list)

	return variables

def crear_vars_trabajadores(model):
	# retorna lista de variables con subindices[n][m][t][d]

	variables = []
	for n in range(CTDAD_TRABAJADORES):
		n_list = []
		for m in range(CTDAD_TIPOS_TRABAJADORES):
			m_list = []
			for t in range(CTDAD_TURNOS):
				t_list = []
				for d in range(CTDAD_DIAS):
					t_list.append(model.addVar(0.0, 1.0, 1.0, GRB.BINARY,
									           name=f"T_{n+1},{m+1},{t+1},{d+1}"))
				m_list.append(t_list)
			n_list.append(m_list)
		variables.append(n_list)

	return variables

def crear_vars_camaras(model):
	# Si se enciende la camara de frio para almacenar fruta el dia d
	F = []
	for d in range(CTDAD_DIAS):
		F.append(model.addVar(lb=0, vtype=GRB.BINARY,
						      name='F'+str(d+1)))
	return F


# RESTRICCIONES
def satisface_demanda(model, D):
	id_r = 1

	for i in range(CTDAD_MERCADOS):
		for d in range(1, CTDAD_DIAS):
			
			if (not (d+1)%7==0):
				restriccion = LinExpr()
				for k in range(CTDAD_TIPOS_CLAMSHELLS):
					restriccion += D[k][i][d]
				model.addConstr(restriccion>=QD[i][d],
								name=f'satisface_demanda_{id_r}')
				id_r+=1

def almacenaje_max(model, A, qa_mod):
	id_r=1
	for d in range(CTDAD_DIAS):
		
		restriccion = LinExpr()
		for k in range(CTDAD_TIPOS_CLAMSHELLS):
			for i in range(CTDAD_MERCADOS):
				restriccion+=A[k][i][d]
		model.addConstr(restriccion<=QA[qa_mod],
						name="almacenaje_max_"+str(id_r))
		id_r+=1

def inventario(model, D, A, C):
	inv_1 = 'a'
	inv_2 = 'b'
	inv_3 = 'c'
	inv_4 = 'd'
	inv_5 = 'e'

	#"""
	id_r = 1
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(CTDAD_MERCADOS):
			for d in range(1,CTDAD_DIAS):
			
				restriccion_left = D[k][i][d] + A[k][i][d]
			
				restriccion_right = A[k][i][d-1]
				for t in range(CTDAD_TURNOS):
					restriccion_right+=C[k][i][t][d]
				model.addConstr(restriccion_left == restriccion_right,
								name=f"Inventario_{inv_1}_{id_r}")
				id_r+=1

	#"""		
	#"""
	id_r = 1
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(CTDAD_MERCADOS):
			for d in range(1, CTDAD_DIAS):

				restriccion = LinExpr()
				for t in range(CTDAD_TURNOS):
					restriccion+=C[k][i][t][d]
				model.addConstr(D[k][i][d]<=restriccion+A[k][i][d-1],
								name=f'Inventario_{inv_2}_{id_r}')
				id_r+=1

	#"""	
	#"""
	id_r1 = 1
	id_r2 = 1
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(CTDAD_MERCADOS):
			for d in range(CTDAD_DIAS):
			
				if ((d+1)%7==0):
					model.addConstr(D[k][i][d]==0,
									name=f'Inventario_{inv_3}_{id_r1}')
					id_r1+=1

					for t in range(CTDAD_TURNOS):
						model.addConstr(C[k][i][t][d]==0,
										name=f'Inventario_{inv_4}_{id_r2}')
						id_r2+=1

	#"""
	#"""
	id_r = 1
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(CTDAD_MERCADOS):
			for d in range(CTDAD_DIAS):
						
				if ((d+1)%7==0 or (d+1)%7==6):
					model.addConstr(A[k][i][d]==0,
									name=f"Inventario_{inv_5}_{id_r}")
					id_r+=1
	#"""

def max_turnos_dia(model, T):
	id_r = 1

	for n in range(CTDAD_TRABAJADORES):
		for d in range(CTDAD_DIAS):
				
			restriccion = LinExpr()
			for m in range(CTDAD_TIPOS_TRABAJADORES):
				for t in range(CTDAD_TURNOS):
					restriccion+=T[n][m][t][d]
			model.addConstr(restriccion<=1, 
							name='Maximo_de_turnos_diarios_'+str(id_r))
			id_r += 1

def min_trabajadores(model, T, C, qt_mod):
	id_r_1 = 1
	id_r_2 = 1
	trab_1 = 'a'
	trab_2 = 'b'

	#"""
	for m in range(CTDAD_TIPOS_TRABAJADORES):
		for d in range(CTDAD_DIAS):
			for t in range(CTDAD_TURNOS):
				#"""
				if not ((d+1)%7==0):
					restriccion_1 = LinExpr()
					for n in range(CTDAD_TRABAJADORES):
						restriccion_1+=T[n][m][t][d]
					model.addConstr(restriccion_1>=QT_LIST[qt_mod][m],
									name=f'Min_trabajadores_{trab_1}_{id_r_1}')
					id_r_1+=1
				#"""
				#'''
				restriccion_2_left = LinExpr()
				for n in range(CTDAD_TRABAJADORES):
					restriccion_2_left+=T[n][m][t][d]

				restriccion_2_right = LinExpr()
				for k in range(CTDAD_TIPOS_CLAMSHELLS):
					for i in range(CTDAD_MERCADOS):
						restriccion_2_right+=C[k][i][t][d]*FM[m]
				model.addConstr(restriccion_2_left>=restriccion_2_right,
								name=f'Min_trabajadores_{trab_2}_{id_r_2}')
				id_r_2+=1	
				#'''

def max_produccion(model, C, qc_mod):
	id_r = 1

	for t in range(CTDAD_TURNOS):
		for d in range(CTDAD_DIAS):

			restriccion = LinExpr()
			for i in range(CTDAD_MERCADOS):
				for k in range(CTDAD_TIPOS_CLAMSHELLS):
					restriccion+=C[k][i][t][d]
			model.addConstr(restriccion <= QC[qc_mod],
							 name=f"Max_produccion_{id_r}")
			id_r+=1

def acceptable(model, C):
	id_r = 1
	acc = ['a', 'b', 'c', 'd']
	acc_values = [[0.1,0.25,0.45,0.05],
				  [0.2,0.4,0.6,0.15]]


	for t in range(CTDAD_TURNOS):
		for d in range(CTDAD_DIAS):
			
			restriccion_lr = LinExpr()
			for k in range(CTDAD_TIPOS_CLAMSHELLS):
				for i in range(CTDAD_MERCADOS):
					restriccion_lr+=C[k][i][t][d]

			for x in range(4):
				restriccion_m = LinExpr()

				for k in range(CTDAD_TIPOS_CLAMSHELLS):
					restriccion_m+=C[k][x][t][d]

				model.addConstr(acc_values[0][x]*restriccion_lr<=restriccion_m,
								name=f"Acceptabilidad_{acc[x]}{id_r}")
				id_r+=1

				model.addConstr(restriccion_m<=acc_values[1][x]*restriccion_lr,
								name=f"Acceptabilidad_{acc[x]}{id_r}")
				id_r+=1

def no_domingos(model, T):
	id_r = 1

	for n in range(CTDAD_TRABAJADORES):
		for m in range(CTDAD_TIPOS_TRABAJADORES):
			for t in range(CTDAD_TURNOS):
				for d in range(CTDAD_DIAS):
					if ((d+1)%7==0):
						model.addConstr(T[n][m][t][6]==0, 
										name='No_working_on_Sundays_'+str(id_r))
						id_r+=1

def prende_frigorifico(model, A, F, qa_mod):
	id_r = 1

	for d in range(CTDAD_DIAS):
		
		restriccion = LinExpr()
		for i in range(CTDAD_MERCADOS):
			for k in range(CTDAD_TIPOS_CLAMSHELLS):
				restriccion += A[k][i][d]

		model.addConstr(restriccion<=QA[qa_mod]*F[d],
						name="Se_prende_el_frigorifico_"+str(id_r))
		id_r+=1

def d_primer_dia(model, D):
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(CTDAD_MERCADOS):
			model.addConstr(D[k][i][0]==0)

def extra(model, D, C, A, T, F):
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(CTDAD_MERCADOS):
			for d in range(CTDAD_DIAS):
				model.addConstr(D[k][i][d]<=99999999)
				model.addConstr(A[k][i][d]<=999999999)
				for t in range(CTDAD_TURNOS):
					model.addConstr(C[k][i][t][d]<=999999999)
			

# FUNCION OBJETIVO
def funcion_objetivo(model, D, C, T, F, cf_mod, cck_mod, pc_mod):

	ganancias = LinExpr()
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(4):
			for d in range(8):
				ganancias+=D[k][i][d]*PC_LIST[pc_mod][k][i][d]

	costo_clamshells = LinExpr()
	costo_fruta = LinExpr()
	for k in range(CTDAD_TIPOS_CLAMSHELLS):
		for i in range(4):
			for t in range(2):
				for d in range(28):
					costo_clamshells+=C[k][i][t][d]*CCK_LIST[cck_mod][k]
					costo_fruta+=C[k][i][t][d]*CCD[d]

	costo_trabajadores = LinExpr()
	for n in range(54):
		for m in range(2):
			for t in range(2):
				for d in range(28):
					costo_trabajadores+=T[n][m][t][d]*CT[m]

	costo_frigorifico = LinExpr()
	for d in range(28):
		costo_frigorifico+=F[d]*CF[cf_mod]


	fo = ganancias-(costo_clamshells+costo_fruta+
					costo_trabajadores+costo_frigorifico)
	model.setObjective(fo, GRB.MAXIMIZE)

