# Codigo para el Proyecto Semestral ICS1113-1 grupo 20

## Instrucciones
para correr el codigo, hay que correr Sensibilidad.py con python3.6+, teniendo matplotlib, gurobipynumpy instalado en el computador

## Explicacion de cada Archivo

- DATOS/ : contiene a los spreadsheets con todos los datos necesarios para hacer los calculos.
- data.py: se encarga de leer los datos dentro de la carpeta DATOS/ y se crean variables globales para ser usadas en los calculos.
- funciones.py : contiene las funciones que arman el modelo; restricciones, funcion objetivo, variables.
- Sensibilidad.py : en este archivo se corre Pack_ing.py varias veces, cada vez cambiando un valor distinto dentro de los parametros.
- plot.py : con las variables optimas encontrada en Pack_ing.py, se crean varios graficos.
- Pack_ing.py : se crea nuestro modelo gurobi y se encuentra el valor optimo.