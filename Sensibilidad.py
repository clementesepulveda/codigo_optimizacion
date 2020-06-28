from Pack_ing import pack_opti

# iterar sobre ck_k, otros parametros, pc1_NEW/pc2_NEW, qt_m
iteracion = [[0,0,0,0,0,0],
			 [1,0,0,0,0,0],
			 [0,1,0,0,0,0],
			 [0,0,1,0,0,0],
			 [0,0,0,1,0,0],
			 [0,0,0,0,1,0],
			 [0,0,0,0,0,1],
			 ]


iter = 1
for i in iteracion:
	print(f"Operacion {iter}")
	pack_opti(*i, iter)
	iter+=1
