from scipy import special as sp
import random
import time
import itertools

NumMix = 2
PROB_MUTACION = 0.05
NumReinas = 8
POBLACION = 10


def fitness(ind):
  #puntuación es cero
  #para reiniciar la variable cada que se ejecute
  score = 0

  for row in range(NumReinas):
    #row hará esto según el número de reinas

    #aux (auxiliar) es una variable que servirá para guardar
    #lo que individuo tiene en su posición 0
    aux = ind[row]

    #other_row nos servirá para evaluar
    for other_row in range(NumReinas):

      #evaluando que las reinas no se emparejen
      if other_row == row:
        #continue hace que el for continue a su sig posición
        continue

      if ind[other_row] == aux:
        #si el individuo comparte posición con otra fila
        continue

      if other_row + ind[other_row] == row + aux:
        #si está en la misma posición y contiene el mismo valor
        continue

      if other_row - ind[other_row] == row - aux:
        continue
      #score aumenta si todos los pares de reinas no atacan
      score += 1

  #dividir por 2 ya que los pares de reinas son conmutativos
  return score / 2


def selection(population):

  parents = []

  #para el individuo de la población
  for ind in population:
    #selecciona los padrs con probabilidad de su puntuación física
    #usa la función de dar un valor random dependiendo el rango
    valor_random = random.randrange(sp.comb(NumReinas, 2) * 2)
    
    
    if valor_random < fitness(ind):
      parents.append(ind)
      

  return parents



def crossover(parents):

  offspring = []

  #aleatorios indices
  cross_points = random.sample(range(NumReinas), 1)

  #todas las permutaciones de los padres
  permutations = list(itertools.permutations(parents, NumMix))



  for perm in permutations:
    
    offsprings = []

    #indice de cruzamiento
    indice = 0

    #ejemplo, perm contiene ([6,4,4,7,7,6,2,0],[3,5,6,0,3,3,4,4])
    

    for parent_i, cross_point in enumerate(cross_points):


      #sublista de padres a cruzar
      parent_part = perm[parent_i][indice:cross_point] 

      
      offspring.append(parent_part)


      #aumenta el contador
      indice = cross_point
      

    #el ultimo padre
    last_parent = perm[-1]
    parent_part = last_parent[cross_point:]
    offspring.append(parent_part)

    #chain crea un iterador que devuelva elementos desde el primer iterable hasta que se termine
    offsprings.append(list(itertools.chain(*offspring)))


  return offsprings


def mutate(ind):
  for row in range(len(ind)):
    if random.random() < PROB_MUTACION:
      ind[row] = random.randrange(NumReinas)

  return ind


def Meta(population, show=True):

  #ind es variable, contiene cada individuo de la población
  for ind in population:
    #toma el fitness de la variable ind
    Fitness = fitness(ind)

    if show:
      print(f'{ind} Fitness: {Fitness}')

    #si puntuación es igual al coeficiente binomial de num reinas, 2
    #sc.com(reinas,2) devuelve 28, se busca que el score del individuo sea 28
    #para decir que ha encontrado solución, es decir, score de num reinas que no se atacan
    #debe ser 28, pues de un conjunto de 9 elementos, se pueden hacer 28 subconjuntos de 2 elementos
    
    if Fitness == sp.comb(NumReinas, 2):
      
      
      print('Solucion encontrada')
      return True

    print('Solucion no encontrada')
  return False


def evolution(population):
  #selecciona al individuo para convertirse en padre
  parents = selection(population)

  #combina para crear una nueva descendencia
  offsprings = crossover(parents)

  #mutacion
  #La función map () devuelve un objeto de mapa (que es un iterador) de los resultados después de aplicar la función dada a cada elemento de un iterable dado (lista, tupla, etc.)
  offsprings = list(map(mutate, offsprings))

  #muestra los individuos con mejor puntuación
  new_gen = offsprings

  
  for ind in population:
    new_gen.append(ind)

  new_gen = sorted(new_gen, key=lambda ind: fitness(ind), reverse=True)[:POBLACION]

  return new_gen


def generar_poblacion():
  #Será una lista de listas
  population = []

  for individuo in range(POBLACION):
    #lista aleatoria, ej: [4,2,7,6,0,5,2,1]
    new = [random.randrange(NumReinas) for idx in range(NumReinas)]

    #lo añade a una lista
    population.append(new)

  return population





#genera random poblacion, una lista de listas

generation = 0

#genera random poblacion, una lista de listas
population = generar_poblacion()

while not Meta(population):
  #si no encuentra solución a la primera generación, evoluciona
  population = evolution(population)
  generation += 1
