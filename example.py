import numpy
import networkx
import random
import subprocess
import os
import copy

MAX_STRESS = 180000000
MAX_DISP = 0.0111

GENES = 105  # Length of the chromosome
eps = 0.0001

path = "D:\\diipl\\python\\200 bar truss\\stats.txt"


class Individual:
    def __init__(self, chromosome, max_stress, fitness, max_disp):
        self.chromosome = chromosome
        self.max_stress = max_stress
        self.fitness = fitness
        self.max_disp = max_disp


def select(parent, offspring, mu):
    new_pop = parent + offspring
    new_pop2 = copy.deepcopy(new_pop)
    sorted_parent_pop = sorted(new_pop2, key=sortindividual_fitness)
    sorted_parent_pop1 = copy.deepcopy(sorted_parent_pop)
    new_pop1 = []
    j = 0
    print(len(sorted_parent_pop1))
    while len(new_pop1) < mu:
        if sorted_parent_pop1[j].max_stress < MAX_STRESS and sorted_parent_pop1[j].max_disp < MAX_DISP:
            new_pop1.append(sorted_parent_pop1[j])
        j = j + 1

    return new_pop1


def mutation(parent, gamma, param):
    parent1 = copy.deepcopy(parent)
    Xo = parent1

    rand = numpy.random.choice(numpy.arange(0, 2), p=[gamma, 1 - gamma])
    if rand == 1:
        for j in range(param):
            k = numpy.random.randint(0, GENES)
            if Xo[k] == 0.00000001:
                Xo[k] = 0.005
            else:
                Xo[k] = 0.00000001
        return Xo
    else:
        return Xo


# def mutation(parent, gamma):
#     Xo = [0.0] * GENES
#     Xp = parent
#     Z = [0] * GENES
#     l = 4
#     for g in range(l):
#         k = numpy.random.poisson(gamma, None)
#         if g == GENES - 1:
#             Z[g] = (k + 1) * abs(Xp[g] - Xp[g - 1])
#         else:
#             Z[g] = (k + 1) * abs(Xp[g] - Xp[g + 1])
#
#     for a in range(len(parent)):
#         Xo[a] = Xp[a] + Z[a]
#
#     return Xo


def sortindividual_fitness(ind):
    return ind.fitness


# Crossover: parent1,parent2,child1,child2:chromosome;1chrom,ncross,nmutation,jcross:integer; pcross,pmutation:real;
def recombination(parent_pop, index, popsize):
    sorted_parent_pop = sorted(parent_pop, key=sortindividual_fitness)
    sorted_parent_pop1 = copy.deepcopy(sorted_parent_pop)
    parent_pop1 = copy.deepcopy(parent_pop)
    x_wave = []
    b = numpy.random.randint(0, popsize)
    a = numpy.random.randint(0, popsize)
    for i in range(GENES):
        k = numpy.random.choice(numpy.arange(0, 2))
        #a = numpy.random.randint(0,popsize)
        if k == 0:
            x_wave.append(parent_pop1[a].chromosome[i])
        else:
            x_wave.append(parent_pop1[b].chromosome[i])

    x_wave1 = copy.deepcopy(x_wave)
    return x_wave1

def createMac(workdir,a,b):
    scriptCreateMac = open(workdir + r'\createMac.txt', 'w')
    scriptCreateMac.write(r"""
/VERIFY,OPTIMIZATION
/PREP7  
/TITLE, OPTIMIZATION, BEAM  
ET,1,BEAM189                         ! DEFINE ELEMENT TYPE  
KEYOPT,1,2,0
MP,EX,1,200E9                      ! DEFINE MATERIAL PROPERTIES 
MP,NUXY,1,0.3   
MP,DENS,1,8000  
!R,1,4  
SECT,1,BEAM,CSOLID
SECD,"""+str(a)+"""
SECT,6,BEAM,CSOLID
SECD,"""+str(b)+"""

N,1,0   
N,11,2 
FILL
E,1,3,2 
!EGEN,5,2,1
N,11,2 
N,21,4 
FILL
!E,11,13,12 
EGEN,10,2,1
*get,Ne,elem,0,count


*do,i,1,Ne,1
*if,i,LE,Ne/2,then
emodif,i,sec,1
*else
emodif,i,sec,6
*endif
*enddo
/eshape,1,0
eplot

mass = 0
*do,i,1,Ne,1
*get,elemm,elem,i,volu
mass = mass + elemm
*enddo
mass = mass* 8000

/sol
nsel,,loc,x,0
d,all,all,0
nsel,,loc,x,2
f,all,fy,-100
allsel,all

solve

/post1
*get,smax,secr,,s,eqv,max
*get,umax,node,21,u,y
*cfopen,res,txt
*vwrite, 's= ',smax, 'u= ',umax ,'v= ',mass
(a3,e10.4)
*cfclose 
""")
    scriptCreateMac.close()

   # frun = ansys.run('createMac', ansyspath, workdir)

# mu lambda algorithm
def main(mu, lambda1):
    #os.remove(path)

    with open('D:\\optimiz\\study\\ansys\\res.txt','r') as f:
       data = f.readlines()
    print(float(data[0].split('=')[1]))

    old_pop = []
    #old_pop.append(Individual([1] * GENES, 0.0, 0.0, 0.0))
    for i in range(10):
        old_pop.append(Individual([round(random.uniform(0.01,1.00),2),round(random.uniform(0.01,1.00),2)],0.0,0.0,0.0))
        #print(old_pop[i].chromosome)
    chrom = random.choice(old_pop).chromosome
    a = chrom[0]
    b = chrom[1]
    createMac('D:\\оптимизацияя',a,b)
    new_pop = []
    offspring_pop = []
    index = 0

    # for i in range(mu):
    #     old_pop.append(Individual([1] * GENES, 0.0, 0.0, 0.0))
    #     offspring_pop.append(Individual([0] * GENES, 0.0, 0.0, 0.0))
    #
    # for j in range(mu):
    #     old_pop[j].chromosome[j] = 0.00000001
    #
    # f = open("chromosome.txt", "w+")
    # for z in range(len(old_pop)):
    #     for x in range(GENES):
    #         f.write("%.2f\t" % old_pop[z].chromosome[x])
    #     f.write('\n')
    # f.close()
    # subprocess.run('abaqus cae noGUI=scriptTruss.py', shell=True)
    #
    # mynumbers = []
    # with open('stress and weight.txt', 'r') as f:
    #     for line in f:
    #         mynumbers.append([float(n) for n in line.strip().split('\t')])
    # for pair1 in range(len(mynumbers)):
    #     x1, y1 = mynumbers[pair1][0], mynumbers[pair1][1]
    #     old_pop[pair1].max_stress = x1
    #     old_pop[pair1].fitness = y1
    #
    # gen = 0
    # maxgen = 500
    # gamma = 0.5
    #
    # y = []
    # y_wave = []
    #
    # for i in range(lambda1):
    #     y.append(Individual([0.0] * GENES, 0.0, 0.0, 0.0))
    #     y_wave.append(Individual([0.0] * GENES, 0.0, 0.0, 0.0))
    #
    # while True:
    #     for l in range(lambda1):
    #         y[l].chromosome = recombination(old_pop, l, mu)
    #         y_wave[l].chromosome = mutation(y[l].chromosome, gamma, 2)
    #
    #         offspring_pop[l].chromosome = y_wave[l].chromosome
    #         print("Offspring: ", offspring_pop[l].chromosome)
    #     # need open file and write y_wave[l] and after that recieve stress and weight
    #
    #     f = open("chromosome.txt", "w+")
    #
    #     for z in range(len(offspring_pop)):
    #         for x in range(GENES):
    #             f.write("%.8f\t" % offspring_pop[z].chromosome[x])
    #         f.write('\n')
    #     f.close()
    #
    #     with open("optimization process.txt", 'a+') as f2:
    #         for x in range(GENES):
    #             f2.write("%f\t" % old_pop[0].chromosome[x])
    #         f2.write('\n')
    #     f2.close()
    #
    #     subprocess.call('abaqus cae noGUI=scriptTruss.py', shell=True)
    #
    #     print("Before selection:")
    #     for h in range(len(old_pop)):
    #         print(old_pop[h].chromosome, '\t', old_pop[h].fitness)
    #
    #     iterat = 0
    #     mynumbers = []
    #     with open("stress and weight.txt", 'r') as f:
    #         for line in f:
    #             mynumbers.append([float(n) for n in line.strip().split('\t')])
    #     for pair in mynumbers:
    #         try:
    #             F_stress, F_weight, F_disp = pair[0], pair[1], pair[2]
    #             offspring_pop[iterat].max_stress = F_stress
    #             offspring_pop[iterat].fitness = F_weight
    #             offspring_pop[iterat].max_disp = F_disp
    #
    #             iterat = iterat + 1
    #         except IndexError:
    #             print("A line in the file doesn't have enough entries.")
    #     # ==========================================================================
    #     print("Before selection:")
    #     for h in range(len(old_pop)):
    #         print(old_pop[h].chromosome, '\t', old_pop[h].fitness)
    #
    #     old_pop_fitn = copy.deepcopy(old_pop[0].fitness)
    #     old_pop = select(old_pop, offspring_pop, mu)
    #     print("NEW::")
    #     for h in range(len(old_pop)):
    #         print(old_pop[h].fitness)
    #
    #     f = open("stats.txt", "a+")
    #     f.write('GEN-' + str(gen) + '\t')
    #     for i in range(len(old_pop)):
    #         for j in range(GENES):
    #             f.write("%.8f\t" % (old_pop[i].chromosome[j]))
    #
    #         f.write("\n%f\t%f\t%f" % (old_pop[i].max_stress, old_pop[i].fitness, old_pop[i].max_disp))
    #         f.write('\n')
    #
    #     f.close()
    #
    #     if abs(old_pop[0].fitness - old_pop_fitn) <= eps:
    #         index = index + 1
    #     else:
    #         index = 0
    #
    #     if gen >= maxgen or index >= 80:
    #         break
    #     gen = gen + 1


main(20, 20)
