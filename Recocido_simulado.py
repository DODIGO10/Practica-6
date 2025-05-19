import math
import random as rnd
import Interpolacion_Lineal as IL
import genera_nuevo as gd
#rnd.seed(5)

rangosdeServicios = gd.data()
def crea_solucion_vecina(solucion, keyIn):
    vector = solucion[:]
    index = rnd.randint(0, len(solucion)-1)
    nuevo_valor = rnd.randint(rangosdeServicios[keyIn][0], rangosdeServicios[keyIn][1])
    vector[index] = nuevo_valor
    return vector

def calcula_fo(solucion):
    vo = sum([i**2 for i in solucion])
    return vo

def crea_solucion(n):
    v = [rnd.randint(xmin, xmax) for i in range(n)]
    return v

def perturbacion(solucion, keyIn): #modificacion brusca de la solucion
    vector = solucion[:]

    index1 = rnd.randint(0, len(solucion) - 1)
    index2 = index1  ####
    while index2 == index1:
        index2 = rnd.randint(0, len(solucion) - 1)

    nuevo_valor1 = rnd.randint(xmin, xmax)
    nuevo_valor2 = rnd.randint(xmin, xmax)

    vector[index1] = nuevo_valor1
    vector[index2] = nuevo_valor2

    return vector


if __name__ == "__main__":
    data = gd.lectura()
    llaves = list(rangosdeServicios.keys())
    current_it = 30
    best_vos = [[] for i in range(len(data))]
    print("Inicia algoritmo:")
    for i in range(len(data)):
        current_it = 30
        while current_it > 0:
            #Seleccionar una solución inicial S;
            solucion_temporal = data[i]  #S0
            print("solucion temporal: ", solucion_temporal)
            best_solucion = solucion_temporal[:]  # copia de los valores
            best_vo = calcula_fo(best_solucion)

            better_solucion = solucion_temporal[:]
            better_vo = best_vo
            print("solucion vo inicial: ", best_vo)

            #Seleccionar una temperatura inicial Ti > 0;
            T = 10000

            #Seleccionar una función de reducción de la temperatura α;
            alfa = 0.88 #  [0.8 - 0.99]

            #Seleccionar un número de iteraciones N;
            max_it = 100
            it = 0

            #Seleccionar un criterio de parada;
            #-> alcanzar a revisar todas las iteraciones mrcadas
            #-> que la temperatura (T) llegue a cierto umbral

            while T > 350: #ciclo externo
                it = 0
                while it < max_it: #ciclo interno
                    solucion_temporal = crea_solucion_vecina(solucion_temporal, llaves[i])
                    vo_temporal = calcula_fo(solucion_temporal)

                    deltaF = vo_temporal - better_vo
                    if deltaF < 0:
                        better_vo = vo_temporal
                        better_solucion = solucion_temporal[:]
                        #print("nueva better solucion: ", solucion_temporal, end="    ")
                        #print("vo: ", vo_temporal)
                    else:
                        deltaDiv = round(deltaF / T, 2)
                        eps = round(math.e, 4)
                        c = math.pow(eps, deltaDiv)
                        t = rnd.random()  # 0 - 1
                        if t < c:
                            better_vo = vo_temporal
                            better_solucion = solucion_temporal[:]
                            #print("nueva better** solucion: ", solucion_temporal, end="    ")
                            #print("vo: ", vo_temporal)

                    #print("it", end="   ")
                    #print("solucion: ", solucion_temporal, end="    ")
                    #print("vo: ", vo_temporal)
                    it+=1

                if better_vo < best_vo:
                    best_vo = better_vo
                    best_solucion = better_solucion[:]
                    print("nueva BEST solucion: ", better_solucion, end="    ")
                    print("vo: ", best_vo)

                T = T * alfa


            print("mejor solucion: ", best_solucion)
            print("mejor vo: ", best_vo)
            best_vos[i].append(best_vo)
            current_it -= 1
    for i in range(len(data)):
        print(best_vos[i])
    iqrs = {
        "Temperatura": 0,
        "Humedad": 0,
        "Ruido": 0,
        "Int_luminosa": 0
    }
    for i in range(4):
        listIqr = list(iqrs.keys())[i]
        iqr = IL.interpolacion_Lineal(best_vos[i])
        iqrs[listIqr] = iqr
    gd.actualizar_csv(iqrs)
    #soft and hard constrainst