from __future__ import division
from scrapper import Scrapper
import random

class GSA():

    """Genetic Search Algorithm"""
    def __init__(self):
        self.chromosomeSize = 10
        self.population = list()
        self.generation = 0
        self.bounceRate = dict()
        self.pageView = dict()
        self.time = dict()
        self.searchVisit = dict()
        self.linkIn = dict()
        self.genes = list()
        self.geneQuality = dict()
        self.fitness = dict()
        print "Hello World"        

    def SinglePointCrossover(self, A, B, r, Pc = random.random()):
        size = len(A)
        if r < Pc:
            return False, A, B
        else:
            point = random.randint(0, size-1)
            Aprime = A[:point] + B[point:]
            Bprime = B[:point] + A[point:]
            Aprime = self.OptimizeChromosome(Aprime)
            Bprime = self.OptimizeChromosome(Bprime)
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
            Aprime = self.OptimizeChromosome(Aprime)
            Bprime = self.OptimizeChromosome(Bprime)
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
            offspring = self.OptimizeChromosome(offspring)
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
            offspring = self.OptimizeChromosome(offspring)
            self.population.append(offspring)
            return True, offspring

    def RWSelection(self, wheel):
        """Strings that are fitter are assigned a larger slot and hence have a better chance of appearing in the new population."""
        raise NotImplemented

    def Recombination(self):
        """The process that determines which solutions are to be preserved and allowed to reproduce and which ones deserve to die out."""
        raise NotImplemented

    def CalculateFitness(self, chromosome, weight=[1]*10):
        sum = 0
        for index, gene in enumerate(chromosome):
            sum += weight[index]*self.CalculateCachedLinkQuality(gene)
        return sum
            

    def InitialisePopulation(self):
        for i in range(10):
            chromosome = self.OptimizeChromosome(random.sample(self.genes, self.chromosomeSize))
            if not self.ChromosomeInPopulation(chromosome):
                self.population.append(chromosome)

    def ChromosomeInPopulation(self, chromosome):
        if chromosome in self.population:
            return True
        else:
            return False
    
    def Selection(self):
        raise NotImplemented

    def CalculateCachedLinkQuality(self, gene, weight = [1]*5):
        if gene not in self.geneQuality.keys():
            quality = weight[0]*self.bounceRate[gene] + weight[1]*self.pageView[gene] + weight[2]*self.time[gene] + weight[3]*self.searchVisit[gene] + weight[4]*self.linkIn[gene]
            self.geneQuality[gene] = quality
            return quality
        else:
            return self.geneQuality[gene]

    def NormalizeFeature(self, feature):
        featureValues = feature.values()
        MAX = max(featureValues)
        MIN = min(featureValues)
        range = MAX - MIN
        mean = sum(featureValues)/len(featureValues)
        for key, value in feature.iteritems():
            feature[key] = (value-mean)/range
        return feature

    def OptimizeChromosome(self, chromosome):
        chromosomeQuality = dict()
        for gene in chromosome:
            chromosomeQuality[gene] = self.CalculateCachedLinkQuality(gene)
        return sorted(chromosomeQuality, key=chromosomeQuality.get, reverse = True)

    def Plot(self):
        raise NotImplemented

    def Display(self):
        raise NotImplemented

gsa = GSA()

sc = Scrapper(str(input("Enter search query: ")), 20)
urls = set(sc.getLinks())
urlDict = dict()
for index, url in enumerate(urls):
    urlDict[index] = url
gsa.genes = urlDict.keys()


for key, value in urlDict.iteritems():
    features = sc.getFeatures(value)
    gsa.bounceRate[key] = features[0]
    gsa.pageView[key] = features[1]
    gsa.time[key] = features[2]
    gsa.searchVisit[key] = features[3]
    gsa.linkIn[key] = features[4]

gsa.bounceRate = gsa.NormalizeFeature(gsa.bounceRate)
gsa.pageView = gsa.NormalizeFeature(gsa.pageView)
gsa.time = gsa.NormalizeFeature(gsa.time)
gsa.searchVisit = gsa.NormalizeFeature(gsa.searchVisit)
gsa.linkIn = gsa.NormalizeFeature(gsa.linkIn)


gsa.InitialisePopulation()


for i in range(50):
    print "Iteration: ", i+1

    gsa.fitness = dict()
    for pos, chromosome in enumerate(gsa.population):
        gsa.fitness[pos] = gsa.CalculateFitness(chromosome)

    chromosome = gsa.population[random.randint(0, len(gsa.population)-1)]
    r = random.random()
    check, offspring = gsa.Mutation(chromosome, r)
    if check:
        gsa.fitness[gsa.population.index(offspring)] = gsa.CalculateFitness(offspring)

    chromosomeA = gsa.population[random.randint(0, len(gsa.population)-1)]
    chromosomeB = gsa.population[random.randint(0, len(gsa.population)-1)]
    r = random.random()
    check, A, B = gsa.SinglePointCrossover(chromosomeA, chromosomeB, r)
    if check:
        gsa.fitness[gsa.population.index(A)] = gsa.CalculateFitness(A)
        gsa.fitness[gsa.population.index(B)] = gsa.CalculateFitness(B)
    index = sorted(gsa.fitness, key = gsa.fitness.get, reverse = True)[:10][:]
    pop=list()
    for item in index:
        pop.append(gsa.population[item])
    gsa.population = pop[:]

priorityGenes = gsa.population[0]
priorityUrls = list()
for gene in priorityGenes:
    priorityUrls.append(urlDict[gene])

for i in len(priorityUrls):
    print priorityUrls[i], ", Rank :", i+1
