import random
from itertools import zip_longest
from typing import Iterable, Tuple, Dict

import conf
from models import Individual, Gene, Constraint, Cosmos

Environment = Iterable[Constraint]
Population = Iterable[Individual]


def mutate(gene: Gene) -> Gene:
    items = [item for item in gene.value]
    possibilities = list(range(len(items))) + ['add']
    if len(items) >= 2:
        possibilities.append('remove')
    random_choice = random.choice(possibilities)
    if random_choice == 'add':
        items.append(random.choice(conf.GENE_ITEMS_POOL))
    elif random_choice == 'remove':
        items.pop(random.randint(0, len(items) - 1))
    else:
        items[random_choice] = random.choice(conf.GENE_ITEMS_POOL)
    return Gene(tuple(items))


def mutate_float(probability: float, original: float) -> float:
    if probability > random.random():
        return random.random()
    else:
        return original


def mate(individual1: Individual, individual2: Individual) -> Individual:
    mutation_probability = random.choice((individual1.mutation_probability, individual2.mutation_probability))
    genome = set()
    for genes in zip_longest(individual1.genome, individual2.genome):
        if None in genes:
            genes = [g for g in genes if g]
        gene: Gene = random.choice(genes)
        if random.random() <= mutation_probability:
            gene = mutate(gene)
        genome.add(gene)
    if random.random() < mutation_probability:
        genome.add(Gene())
    return Individual(
        mutate_float(mutation_probability, mutation_probability),
        random.choice((individual1.consumption_rate, individual2.consumption_rate)),
        genome,
    )


def evaluate(environment: Environment, individual: Individual) -> float:
    reward = 0
    for constraint in environment:
        if constraint.activation_genes.issubset(individual.genome):
            reward += constraint.reward
    return reward


def evaluate_attractiveness(subject: Individual, object_: Individual, fitness: float) -> float:
    return len(subject.genome.intersection(object_.genome)) * fitness


def choose_partner(individual: Individual, population: Population, fitnesses: Dict[Individual, float]):
    return max(population, key=lambda i: evaluate_attractiveness(individual, i, fitnesses.get(individual, 0)))


def consume_resources(cosmos: Cosmos) -> Tuple[Population, float]:
    survivors = []
    resources = cosmos.resources
    for individual in sorted(cosmos.population, key=lambda i: evaluate(cosmos.environment, i)):
        if resources >= individual.consumption_rate:
            resources -= individual.consumption_rate
            survivors.append(individual)
        else:
            break
    return survivors, resources


if __name__ == '__main__':
    i1 = Individual()
    i2 = Individual()
    i3 = mate(i1, i2)
    print(i1, i2, i3, sep='\n')
    env = [Constraint() for _ in range(10)]
    print(evaluate(env, i3))
