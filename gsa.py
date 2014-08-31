from __future__ import division
from scrapper import Scrapper
import random

class GSA():

    """Genetic Search Algorithm"""
    def __init__(self):
        self.chromosomeSize = 10
        self.population = list()
        self.generation = 0
        print "Hello World"        

    def SinglePointCrossover(self, A, B, r, Pc = random.random()):
        size = len(A)
        if r < Pc:
            return False, A, B
        else:
            point = random.randint(0, size-1)
            Aprime = A[:point] + B[point:]
            Bprime = B[:point] + A[point:]
            self.population.append(Aprime)
            self.population.append(Bprime)
            self.generation += 1
        return True, Aprime, Bprime

    def TwoPointCrossover(self, A, B, r, Pc=random.random()):
        if r < Pc:
            return False, A, B
        else:                
            point1 = random.randint(0, size-1)
            point2 = random.randint(0, size-1)
            Aprime = A[:point1] + B[point1:point2] + A[point2:]
            Bprime = B[:point1] + A[point1:point2] + B[point2:]
            self.population.append(Aprime)
            self.population.append(Bprime)
            self.generation += 1
        return True, Aprime, Bprime

    def UniformCrossover(self, A, B, r, Pc=random.random()):
        if r < Pc:
            Afit = CalculateFitness(A)
            Bfit = CalculateFitness(B)
            if Afit > Bfit:
                return False, A
            else:
                return False, B
        else:
            offspring = list()
            for i in range(self.chromosomeSize):
                choice = random.randint(0,1)
                if choice == 0:
                    offspring.append(A[i])
                else:
                    offspring.append(B[i])
            self.population.append(offspring)
            self.generation += 1
        return True, offspring

    def Mutation(self, chromosome, r, Pm = random.random()):
        if r < Pm:
            return False, chromosome
        else:
            mutation = random.sample(self.genes, 1)[0]
            pos = random.randint(0, (len(chromosome)-1))
            offspring = chromosome[:]
            offspring[pos] = mutation
            print r, Pm, mutation, pos, offspring, self.ChromosomeInPopulation(offspring)
            if not self.ChromosomeInPopulation(offspring):
                self.population.append(offspring)
                print self.population
            return True, offspring

    def RWSelection(self, wheel):
        """Strings that are fitter are assigned a larger slot and hence have a better chance of appearing in the new population."""
        raise NotImplemented

    def Recombination(self):
        """The process that determines which solutions are to be preserved and allowed to reproduce and which ones deserve to die out."""
        raise NotImplemented

    def CalculateFitness(self, chromosome, weights=[1]*10):
        sum = 0
        for index, gene in enumerate(chromosome):
            sum += weigths[i]*self.CalculateCachedLinkQuality(gene)
        return sum
            

    def InitialisePopulation(self):
        chromosome = random.sample(self.genes, self.chromosomeSize)
        if not self.ChromosomeInPopulation(chromosome):
            self.population.append(chromosome)
        return 0

    def ChromosomeInPopulation(self, chromosome):
        if chromosome in self.population:
            return True
        else:
            return False
    
    def Selection(self):
        raise NotImplemented

    def CalculateCachedLinkQuality(self):
        raise NotImplemented

    def NormalizeFeature(self, range):
        raise NotImplemented

    def Plot(self):
        raise NotImplemented

    def Display(self):
        raise NotImplemented

gsa = GSA()

sc = Scrapper(str(input("Enter search query: ")), 50)
urls = set(sc.getLinks())
urlDict = dict()
for index, url in enumerate(urls):
    urlDict[index] = url
gsa.genes = urlDict.keys()
featureDict = dict()

for key, value in urlDict.iteritems():
    featureDict[key] = sc.getFeatures(value)


"""gsa.InitialisePopulation()
ITERATIONS = 50
for i in range(ITERATIONS):
    chromosome = gsa.population[random.randint(0, len(gsa.population)-1)]
    r = random.random()
    check, offspring = gsa.Mutation(chromosome, r, Pm=0)
print gsa.population"""
    


