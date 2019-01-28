from conf import DEFAULT_COSMOS_RESOURCE_REGENERATION_RATE
from models import Cosmos
from operations import evaluate, mate, choose_partner, consume_resources


def main():
    cosmos = Cosmos()
    fitnesses = {}
    for i in range(10000):
        try:
            if i % 100 == 0:
                print(i)
            # Evaluate population
            for individual in cosmos.population:
                if individual not in fitnesses:
                    fitnesses[individual] = evaluate(cosmos.environment, individual)
            # Reduce population
            cosmos.population, cosmos.resources = consume_resources(cosmos)
            # todo : remove deads from fitness
            # Reproduce population
            new_generation = []
            for individual in cosmos.population:
                new_generation.append(mate(individual, choose_partner(individual, cosmos.population, fitnesses)))
            cosmos.population += new_generation
            cosmos.resources += DEFAULT_COSMOS_RESOURCE_REGENERATION_RATE
        except KeyboardInterrupt:
            break
    return cosmos


if __name__ == '__main__':
    result = main()
