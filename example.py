import numpy
import random
import subprocess
import os


# Путь для папки проекта
path = "D:\\project"

# Пример класса, который описывает одну особь в популяции
class Individual:
    def __init__(self, chromosome, max_stress, fitness, max_disp):
        self.chromosome = chromosome
        self.max_stress = max_stress
        self.fitness = fitness
        self.max_disp = max_disp

# Реализация оператора выбора
def select():
    pass

# Реализация оператора мутации
def mutation():
    pass

# Функция для сортировки массива,состоящего из элементов Individual,по значению фитнес параметра
def sortindividual_fitness(ind):
    return ind.fitness

# Реализация оператора скрещивания
def crossover():
    pass

# Пример того как записывать файл макроса
def createMac(workdir,a,b):
    scriptCreateMac = open(workdir + r'\createMac.txt', 'w')
    scriptCreateMac.write(r"""
a ="""+str(a)+"""
b ="""+str(b)+"""
""")
    scriptCreateMac.close()

   frun = ansys.run('createMac', ansyspath, workdir)  # Запуск ANSYS с макросом

# Реализация генетического алгоритма с использованием операторов
def GeneticAlg():
    pass

