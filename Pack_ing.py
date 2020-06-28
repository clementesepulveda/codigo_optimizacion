from gurobipy import GRB, Model
import funciones as fn
from plot import plot


def pack_opti(qa_mod, qc_mod, cf_mod, cck_mod, pc_mod, qt_mod, iter):

	# Se crea el modelo
	m = Model()


	# Clamshells despachados de tipo k a mercado i en el turno t del dia d
	D = fn.crear_vars_clamshells(m, 'D')

	# Clamshells producidos de tipo k a mercado i el turno t del dia d
	C = fn.crear_vars_clamshells_con_t(m, 'C')

	# Clamshells producidos de tipo k a mercado i el turno t del dia d
	A = fn.crear_vars_clamshells(m, 'A')

	# Si trabajador n de tipo m trabaja en el turno t del dia d
	T = fn.crear_vars_trabajadores(m)

	# Si se enciende la camara de frio para almacenar fruta el dia d
	F = fn.crear_vars_camaras(m)

	# Se actualiza el modelo
	m.update()

	# Se satisface la demanda
	fn.satisface_demanda(m, D)

	# Almacenaje max
	fn.almacenaje_max(m, A, qa_mod)
	
	# Restricciones de inventario
	fn.inventario(m, D, A, C)

	# Maximo de turnos diarios
	fn.max_turnos_dia(m, T)

	# Cantidad de trabajadores minimos
	fn.min_trabajadores(m, T, C, qt_mod)

	# Max produccion en cada turno
	fn.max_produccion(m, C, qc_mod)

	# Estandares aceptables por mercado
	fn.acceptable(m, C)

	# No se trabaja los domingos
	fn.no_domingos(m, T)

	# Se prende el frigorifico
	fn.prende_frigorifico(m, A, F, qa_mod)

	# El primer dia no se producen clamshells
	fn.d_primer_dia(m, D)


	# Funcion Objetivo
	fn.funcion_objetivo(m, D, C, T, F, cf_mod, cck_mod, pc_mod)

	m.optimize()

	m.printAttr("X")

	# Se hacen los graficos
	plot(m, iter)