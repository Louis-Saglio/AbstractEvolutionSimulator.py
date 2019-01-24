from dataclasses import dataclass, field
from random import randint, choices, uniform
from typing import Set, Tuple, Iterable, List

from conf import (
    GENE_SIZE_LIMITS,
    GENE_ITEMS_POOL,
    INDIVIDUAL_MUTATION_PROBABILITY_LIMITS,
    INDIVIDUAL_RESOURCE_CONSUMPTION_RATE_LIMITS,
    GENOME_SIZE_LIMITS,
    CONSTRAINT_GENES_NUMBER_LIMITS,
    CONSTRAINT_REWARD_LIMITS,
    DEFAULT_COSMOS_RESOURCES, DEFAULT_POPULATION_SIZE, DEFAULT_ENVIRONMENT_SIZE)


@dataclass(frozen=True)
class Gene:
    """
    Abstract :
        Un gene est une collection ordonnée de 1 à n item choisie dans un même ensemble
    Implementation:
        Un gene a une propriété value qui est un tuple de string
        dont les charactères sont choisis dans le tuple GENE_ITEMS_SET
    """
    value: Tuple[str, ...] = field(
        default_factory=lambda: tuple(choices(GENE_ITEMS_POOL, k=randint(*GENE_SIZE_LIMITS)))
    )


@dataclass(frozen=True)
class Individual:
    """
    Abstract:
        Un individu est défini par un ensemble immutable de genes,
        par une probabilité de mutation et par un taux de consommation de ressource
    """
    mutation_probability: float = field(
        default_factory=lambda: uniform(*INDIVIDUAL_MUTATION_PROBABILITY_LIMITS)
    )
    consumption_rate: float = field(
        default_factory=lambda: uniform(*INDIVIDUAL_RESOURCE_CONSUMPTION_RATE_LIMITS)
    )
    genome: Set[Gene] = field(
        default_factory=lambda: {Gene() for _ in range(randint(*GENOME_SIZE_LIMITS))},
    )

    def __hash__(self):
        return hash((self.mutation_probability, self.consumption_rate, id(self.genome)))


@dataclass(frozen=True)
class Constraint:
    """
    Abstract:
        Une contrainte est définie par un ensemble de genes et par une valeur de récompense
    """
    activation_genes: Set[Gene] = field(
        default_factory=lambda: {Gene() for _ in range(randint(*CONSTRAINT_GENES_NUMBER_LIMITS))}
    )
    reward: float = field(
        default_factory=lambda: uniform(*CONSTRAINT_REWARD_LIMITS)
    )


@dataclass(eq=False)
class Cosmos:
    population: List[Individual] = field(
        default_factory=lambda: [Individual() for _ in range(DEFAULT_POPULATION_SIZE)]
    )
    environment: Iterable[Constraint] = field(
        default_factory=lambda: [Constraint() for _ in range(DEFAULT_ENVIRONMENT_SIZE)]
    )
    resources: float = field(default=DEFAULT_COSMOS_RESOURCES)


if __name__ == '__main__':
    assert Gene(("a", "b")) == Gene(("a", "b"))
    print(Individual())
    for _ in range(30000):
        Individual()
